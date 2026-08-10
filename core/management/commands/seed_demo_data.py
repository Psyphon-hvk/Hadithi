from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from resources.models import Resource, ResourceCategory
from community.models import Assessment, AssessmentQuestion, Story
from wellness.models import BreathingExercise, MindfulnessSession
from events.models import Event


class Command(BaseCommand):
    help = "Seed the database with demo content for local development/demo purposes."

    def handle(self, *args, **options):
        # Demo admin user
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", email="admin@hadithi.local", password="hadithi-demo-2026")
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin' / password 'hadithi-demo-2026'"))

        demo_user, _ = User.objects.get_or_create(
            username="demo_nurse",
            defaults={"role": User.Role.NURSE, "facility_name": "Amref Health Africa", "county": "Nairobi"},
        )
        demo_user.set_password("hadithi-demo-2026")
        demo_user.save()

        # Resource categories & resources
        cat, _ = ResourceCategory.objects.get_or_create(name="Mental Wellbeing", slug="mental-wellbeing")
        Resource.objects.get_or_create(
            title="Managing Burnout as a Frontline Worker",
            slug="managing-burnout",
            defaults=dict(
                category=cat, resource_type=Resource.ResourceType.ARTICLE,
                summary="Practical strategies for recognising and managing burnout.",
                body="Burnout is common among frontline healthcare workers. This guide covers early warning "
                     "signs, self-care strategies, and when to seek support.",
                created_by=demo_user,
            ),
        )

        # Assessments
        phq9, _ = Assessment.objects.get_or_create(
            name="PHQ-9", assessment_type=Assessment.AssessmentType.PHQ9,
            defaults={"description": "A 9-question tool for screening depression symptoms."},
        )
        if not phq9.questions.exists():
            questions = [
                "Little interest or pleasure in doing things",
                "Feeling down, depressed, or hopeless",
                "Trouble falling or staying asleep, or sleeping too much",
                "Feeling tired or having little energy",
                "Poor appetite or overeating",
            ]
            for i, q in enumerate(questions, start=1):
                AssessmentQuestion.objects.create(assessment=phq9, order=i, text=q)

        # Story
        Story.objects.get_or_create(
            title="Finding strength after a difficult shift",
            slug="finding-strength",
            defaults=dict(
                author=demo_user, is_anonymous=True,
                body="After a particularly hard night shift, I realised I wasn't alone in how I felt...",
            ),
        )

        # Wellness toolkit
        BreathingExercise.objects.get_or_create(
            name="Box Breathing", defaults=dict(description="A calming 4-4-4 breathing technique.",
                                                 inhale_seconds=4, hold_seconds=4, exhale_seconds=4, cycles=5),
        )
        MindfulnessSession.objects.get_or_create(
            title="5-Minute Grounding", defaults=dict(description="A short grounding exercise.", duration_minutes=5),
        )

        # Event
        Event.objects.get_or_create(
            title="Peer Support Circle: Coping with Compassion Fatigue",
            defaults=dict(
                description="A guided webinar on recognising and coping with compassion fatigue.",
                event_type=Event.EventType.WEBINAR,
                start_time=timezone.now() + timedelta(days=7),
                location_or_link="https://meet.example.com/hadithi-peer-support",
            ),
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
