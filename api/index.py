"""
Vercel serverless entry point.

Vercel's Python runtime looks for a WSGI-compatible `app` (or `handler`)
callable in this file and routes every request to it - see vercel.json,
which sends all paths here. This just exposes the normal Django WSGI
application; nothing Django-specific lives in this file.
"""

import os
import sys
from pathlib import Path

# Make the project root importable (this file lives in /api).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
