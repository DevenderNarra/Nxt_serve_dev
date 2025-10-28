from django.urls import path
from .views import PositionCreateView, PositionDetailView, CandidateCreateView, test_position, test_candidate, test_jd, GenerateJDPreviewView, GenerateJDFileView

urlpatterns = [
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
]
