from django.db import models
from django.utils import timezone

# ---------------- Position Model ----------------
class Position(models.Model):
    job_title = models.CharField(max_length=255, default="Unknown")
    domain = models.CharField(max_length=255, default="Unknown")
    exp_from = models.IntegerField(default=0)
    exp_to = models.IntegerField(default=0)
    job_description_file = models.FileField(upload_to='job_descriptions/', blank=True, null=True)
    mandatory_skills = models.JSONField(default=list)  # list of mandatory skills
    optional_skills = models.JSONField(default=list)   # list of optional skills
    interview_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.job_title


# ---------------- Candidate Model ----------------
class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    domain = models.CharField(max_length=255, default="Unknown")
    mandatory_skills = models.JSONField(default=list)
    optional_skills = models.JSONField(default=list)
    jd_file = models.FileField(upload_to='candidate_jd/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    name = models.CharField(max_length=255, default="Unknown")
    email = models.EmailField(default="example@example.com")
    contact = models.CharField(max_length=20, default="")
    experience = models.FloatField(default=0)
    preferred_timings = models.CharField(max_length=255, blank=True, null=True)
    interview_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
