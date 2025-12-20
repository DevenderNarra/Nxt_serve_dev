from rest_framework import serializers
from .models import User, Position, Candidate, Interview
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # add custom fields
        data['username'] = self.user.username
        data['role'] = self.user.role
        return data

class EmployerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'contact_number', 'company_name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            contact_number=validated_data.get('contact_number'),
            company_name=validated_data.get('company_name'),
            role='employer'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class InterviewerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'contact_number', 'company_name', 'state', 'city',
                  'experience', 'domain', 'resume_file', 'keywords', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            contact_number=validated_data.get('contact_number'),
            company_name=validated_data.get('company_name'),
            state=validated_data.get('state'),
            city=validated_data.get('city'),
            experience=validated_data.get('experience'),
            domain=validated_data.get('domain'),
            role='interviewer',
            keywords=validated_data.get('keywords', [])
        )
        resume_file = validated_data.get('resume_file')
        if resume_file:
            user.resume_file = resume_file
        user.set_password(validated_data['password'])
        user.save()
        return user

class InterviewSerializer(serializers.ModelSerializer):
    interview_id = serializers.IntegerField(source='id', read_only=True)
    posted_by = serializers.CharField(source='employer.username', read_only=True)
    job_title = serializers.CharField(source='position.job_title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'interview_id',
            'posted_by',
            'created_at',
            'job_title',
            'candidate_name',
            'preferred_timings',
            'status',
        ]