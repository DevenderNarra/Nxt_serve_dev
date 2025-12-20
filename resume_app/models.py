from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('interviewer', 'Interviewer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    # Interviewer-specific fields
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    experience = models.FloatField(blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)
    resume_file = models.FileField(upload_to='interviewer_resumes/', blank=True, null=True)
    keywords = models.JSONField(default=list, blank=True)  # list of skills/keywords

    def __str__(self):
        return f"{self.username} ({self.role})"

# ---------------- Position Model ----------------
class Position(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='positions',
        limit_choices_to={'role': 'employer'},
        null=True,    # allow null temporarily
        blank=True    # allow blank in forms # ensures only employers can own positions
    )
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
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidates',
        limit_choices_to={'role': 'employer'},
        null=True,    # allow null temporarily
        blank=True    # allow blank in forms
    )
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


class Interview(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interviews_posted',
        limit_choices_to={'role': 'employer'}
    )
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, related_name='interviews')
    position = models.ForeignKey('Position', on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='interviews_taken',
        null=True, blank=True,
        limit_choices_to={'role': 'interviewer'}
    )

    preferred_timings = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview #{self.id} - {self.candidate.name} ({self.status})"
