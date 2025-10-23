import boto3
import json
import google.generativeai as genai
from pdfminer.high_level import extract_text
from docx import Document
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Resume
from django.shortcuts import render

def index(request):
    return render(request, 'resume_app/index.html')


# ------------ S3 Upload Function ------------
def upload_to_s3(file_obj, file_name):
    """
    Uploads a file to AWS S3 and returns the public URL.
    """
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    s3.upload_fileobj(file_obj, settings.AWS_STORAGE_BUCKET_NAME, file_name)
    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_name}"
    return url


# ------------ Extract Text from Resume ------------
def extract_text_from_resume(file_obj, file_name):
    """
    Reads .pdf or .docx file and returns raw text.
    """
    text = ""
    if file_name.endswith('.pdf'):
        text = extract_text(file_obj)
    elif file_name.endswith('.docx'):
        doc = Document(file_obj)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
    return text


# ------------ Use Gemini LLM to Extract Structured Data ------------
def extract_with_llm(resume_text):
    """
    Uses Google Gemini API to parse resume text and extract
    name, email, phone, skills, and experience in JSON format.
    """
    # Configure Gemini API
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Optional: print available models
    models = list(genai.list_models())
    print("Available models:")
    for m in models:
        print(m.name)

    # Use a valid model
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    prompt = f"""
    You are a resume parsing AI. From the given resume text, extract structured information.

    Return JSON with these exact keys:
    - name
    - email
    - phone
    - skills (list)
    - experience

    Resume text:
    {resume_text}
    """

    # Pass prompt as positional argument (not keyword)
    response = model.generate_content(prompt)
    result_text = response.text.strip()

    # Attempt to parse JSON from Gemini's response
    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        # fallback if Gemini returns extra text
        try:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_part = result_text[json_start:json_end]
            data = json.loads(json_part)
        except Exception:
            data = {
                "name": "",
                "email": "",
                "phone": "",
                "skills": [],
                "experience": ""
            }

    return data


# ------------ API View for Uploading and Parsing Resume ------------
class ResumeUploadView(APIView):
    """
    API endpoint for uploading resumes, storing in S3, parsing via Gemini, and saving data.
    """

    def post(self, request):
        file = request.FILES.get('resume')
        if not file:
            return Response({"error": "No resume file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ✅ Read file once into bytes
            file_bytes = file.read()

            # ✅ Create new BytesIO objects wherever needed (since each read consumes the stream)
            from io import BytesIO

            # Step 1: Upload to S3
            s3_url = upload_to_s3(BytesIO(file_bytes), file.name)

            # Step 2: Extract text
            resume_text = extract_text_from_resume(BytesIO(file_bytes), file.name)

            # Step 3: Parse with Gemini / LLM
            extracted_data = extract_with_llm(resume_text)

            # Step 4: Add S3 URL
            extracted_data['s3_url'] = s3_url

            # Step 5: Save to DB
            resume = Resume.objects.create(
                name=extracted_data.get('name', ''),
                email=extracted_data.get('email', ''),
                phone=extracted_data.get('phone', ''),
                skills=", ".join(extracted_data.get('skills', []))
                if isinstance(extracted_data.get('skills'), list)
                else extracted_data.get('skills', ''),
                experience=extracted_data.get('experience', ''),
                s3_url=s3_url
            )

            # Step 6: Return Response
            return Response({
                "id": resume.id,
                "name": resume.name,
                "email": resume.email,
                "phone": resume.phone,
                "skills": resume.skills,
                "experience": resume.experience,
                "s3_url": resume.s3_url
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
