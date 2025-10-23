from django.urls import path
from .views import ResumeUploadView,index

urlpatterns = [
    path('', index, name='home'),
    path('upload_resume/', ResumeUploadView.as_view(), name='upload_resume'),
]
