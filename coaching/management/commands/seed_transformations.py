import os

from django.core.files import File
from django.core.management.base import BaseCommand

from coaching.models import Transformation

# Images shipped with the app (not real client photos) - clean, on-brand
# placeholder graphics so the section shows real image tiles out of the
# box. Replace them with real before/after photos from Django Admin
# whenever they're available; nothing about this command is required
# once real content exists.
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "seed_assets")

TRANSFORMATIONS = [
    {
        "client_label": "Client, to be added",
        "goal": "To be added",
        "duration": "To be added",
        "description": "A real result description will be added here once a client transformation is shared.",
        "testimonial": "",
        "featured": True,
        "display_order": 1,
        "image_pair": "transformation-1",
    },
    {
        "client_label": "Client, to be added",
        "goal": "To be added",
        "duration": "To be added",
        "description": "A real result description will be added here once a client transformation is shared.",
        "testimonial": "",
        "featured": False,
        "display_order": 2,
        "image_pair": "transformation-2",
    },
    {
        "client_label": "Client, to be added",
        "goal": "To be added",
        "duration": "To be added",
        "description": "A real result description will be added here once a client transformation is shared.",
        "testimonial": "",
        "featured": False,
        "display_order": 3,
        "image_pair": "transformation-3",
    },
]


class Command(BaseCommand):
    help = (
        "Creates placeholder transformation entries with placeholder "
        "before/after graphics, ready to be replaced with real client photos."
    )

    def handle(self, *args, **options):
        if Transformation.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Transformation entries already exist - skipping seed to avoid duplicates."
                )
            )
            return

        for data in TRANSFORMATIONS:
            data = dict(data)
            image_pair = data.pop("image_pair")
            t = Transformation(**data)
            t.save()

            before_path = os.path.join(ASSETS_DIR, f"{image_pair}-before.jpg")
            after_path = os.path.join(ASSETS_DIR, f"{image_pair}-after.jpg")

            if os.path.exists(before_path):
                with open(before_path, "rb") as f:
                    t.before_image.save(f"{image_pair}-before.jpg", File(f), save=False)
            if os.path.exists(after_path):
                with open(after_path, "rb") as f:
                    t.after_image.save(f"{image_pair}-after.jpg", File(f), save=False)
            t.save()

            self.stdout.write(self.style.SUCCESS(f"Created placeholder transformation: {t.client_label}"))
