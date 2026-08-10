from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with healthcare-cadre role support."""

    class Role(models.TextChoices):
        NURSE = "nurse", "Nurse"
        DOCTOR = "doctor", "Doctor"
        CLINICAL_OFFICER = "clinical_officer", "Clinical Officer"
        COMMUNITY_HEALTH_WORKER = "chw", "Community Health Worker"
        LAB_TECHNICIAN = "lab_technician", "Lab Technician"
        PHARMACIST = "pharmacist", "Pharmacist"
        ADMIN = "admin", "Administrator"
        OTHER = "other", "Other"

    role = models.CharField(max_length=32, choices=Role.choices, default=Role.OTHER)
    facility_name = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_profile_public = models.BooleanField(default=False)
    date_joined_platform = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name() or self.username
