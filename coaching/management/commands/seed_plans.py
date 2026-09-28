from django.core.management.base import BaseCommand

from coaching.models import CoachingPlan

PLANS = [
    {
        "name": "3 Months",
        "slug": "3-months",
        "duration_months": 3,
        "original_price": 5400,
        "discounted_price": 4500,
        "description": "Get started with a structured coaching foundation.",
        "badge": "STARTER",
        "is_featured": False,
        "order": 1,
        "features": "\n".join(
            [
                "Personalized Training Program",
                "Personalized Nutrition Guidance",
                "Weekly Check-ins",
                "Progress Tracking",
                "Program Adjustments",
                "Direct Coach Support",
            ]
        ),
    },
    {
        "name": "6 Months",
        "slug": "6-months",
        "duration_months": 6,
        "original_price": 10800,
        "discounted_price": 8000,
        "description": "The most popular option for steady, lasting progress.",
        "badge": "BEST VALUE",
        "is_featured": True,
        "order": 2,
        "features": "\n".join(
            [
                "Everything in 3 Months",
                "Longer-term progression strategy",
                "More progress reviews",
                "Continued plan optimization",
                "Stronger accountability",
            ]
        ),
    },
    {
        "name": "12 Months",
        "slug": "12-months",
        "duration_months": 12,
        "original_price": 21600,
        "discounted_price": 14000,
        "description": "Full-year coaching for a complete transformation.",
        "badge": "BEST COMMITMENT",
        "is_featured": False,
        "order": 3,
        "features": "\n".join(
            [
                "Everything in 6 Months",
                "Long-term transformation strategy",
                "Continuous progression",
                "Extended accountability",
                "Long-term coaching support",
                "Ongoing plan optimization",
            ]
        ),
    },
]


class Command(BaseCommand):
    help = "Creates or updates the sample 3/6/12 month coaching plans."

    def handle(self, *args, **options):
        for data in PLANS:
            plan, created = CoachingPlan.objects.update_or_create(
                slug=data["slug"], defaults=data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} plan: {plan.name}"))
