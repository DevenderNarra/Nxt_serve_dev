from django.urls import path
from django.views.generic import TemplateView
from .views import PositionCreateView, PositionDetailView, CandidateCreateView, test_position, test_candidate, test_jd, GenerateJDPreviewView, GenerateJDFileView,EmployerSignupView, InterviewerSignupView,test_employer_signup, test_interviwer_signup, LoginView , InterviewListView

urlpatterns = [
    path('employer-signup/', EmployerSignupView.as_view(), name='signup-employer'),
    path('interviewer-signup/', InterviewerSignupView.as_view(), name='signup-interviewer'),
    path('login/', LoginView.as_view(), name='login'),

    # Test templates
    path('test/employer-signup/', test_employer_signup, name='test-employer-signup'),
    path('test/interviewer-signup/', test_interviwer_signup, name='test-interviewer-signup'),
    # Position APIs
    path('positions/', PositionCreateView.as_view(), name='create-position'),
    path('positions/<int:pk>/details/', PositionDetailView.as_view(), name='position-details'),

    # Candidate APIs
    path('candidates/', CandidateCreateView.as_view(), name='add-candidate'),
    path('test/position/', test_position, name='test-position'),
path('test/candidate/', test_candidate, name='test-candidate'),
path('test/jd/', test_jd, name='test-jd'),
# path('generate-jd/', GenerateJDView.as_view(), name='generate_jd'),
# path('generate-jd-preview/', GenerateJDPreviewView.as_view(), name='generate_jd_preview'),
path('generate-jd-preview/', GenerateJDPreviewView.as_view(), name='generate-jd-preview'),
path('generate-jd-file/', GenerateJDFileView.as_view(), name='generate_jd_file'),
path('interviews/', InterviewListView.as_view(), name='interview-list'),
]
