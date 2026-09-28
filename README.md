# Captain Shaban — Online Coaching Website

A Django website for Captain Shaban Faisal Tharwat's online fitness coaching
business: marketing pages, coaching plans, and a checkout prototype that
creates a pending order for the coach to follow up on.

## Tech stack

Plain Django + Django templates + vanilla CSS/JS. No frontend framework,
no build step. Everything runs with `python manage.py runserver`.

## Project layout

```
manage.py
requirements.txt        Django + Pillow (Pillow is needed for ImageField)
config/                Django project settings, root urls
coaching/               The one app: models, views, forms, admin, urls
  management/commands/seed_plans.py            creates the 3/6/12 month sample plans
  management/commands/seed_transformations.py  creates 3 placeholder transformations
templates/
  base.html
  robots.txt
  sitemap.xml
  coaching/            home, checkout, confirmation pages
static/
  css/style.css
  js/main.js            mobile menu, checkout payment panel, before/after slider
  images/               coach photos - see "Adding real photos" below
media/                  transformation before/after photos, uploaded via Admin
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_plans              # creates the 3 sample coaching plans
python manage.py seed_transformations    # creates 3 placeholder transformations
python manage.py createsuperuser
python manage.py runserver
```

Visit:
- `http://127.0.0.1:8000/` — homepage
- `http://127.0.0.1:8000/admin/` — Django admin (plans, orders, transformations)

## Adding real coach photos

Four different photos are used across the homepage. Drop them in
`static/images/` with these exact names:

| File | Where it appears |
|---|---|
| `coach-hero.jpg` | Hero section (main photo) |
| `coach-about.jpg` | "Meet Your Coach" section |
| `coach-training.jpg` | "How It Works" section |
| `coach-cta.jpg` | Final "Ready to Start?" section (background) |

Every one of these is optional — if a file is missing, that section
renders a clean placeholder instead of breaking. See
`static/images/README.txt` for sizing notes.

## Real Transformations section

Client before/after transformations are a `Transformation` model,
fully editable from Django Admin under **Coaching → Transformations**
(images are uploaded there, not placed as static files). Each entry has
`client_label`, `before_image`, `after_image`, `goal`, `duration`,
`description`, `testimonial`, `featured` and `active`.

- The entry marked **featured** renders large, with a draggable
  before/after comparison slider (vanilla JS, no dependencies).
- All other active entries render as a grid of smaller cards.
- Any transformation missing one or both images still displays cleanly
  with a labeled placeholder — nothing breaks.
- `seed_transformations` only creates its 3 placeholders once; it won't
  duplicate them if you run it again after adding real ones.
- The 3 seeded entries come with generic on-brand placeholder graphics
  (a dumbbell/figure/stopwatch icon on the dark grid background, labeled
  "Before"/"After") from `coaching/seed_assets/` - not real client
  photos. Replace `before_image`/`after_image` on each entry with real
  photos whenever you have them, following the workflow below.

### Updating transformation photos (on Vercel)

Vercel's filesystem is read-only at runtime, so uploading a photo
through Admin **on the live site will fail** with a "Read-only file
system" error - there's nowhere for Vercel to write the file to. Do it
from your own machine instead, then push the result to GitHub. This
applies equally to `seed_transformations` (step 2 below can be that
command instead of a manual Admin upload) and to any photo you upload
by hand:

```bash
# 1. Point your local Django at the SAME production database Vercel uses,
#    so the record you create matches what will be live - not your local
#    SQLite copy.
export DATABASE_URL="<the postgresql:// string from Neon>"   # PowerShell: $env:DATABASE_URL="..."

# 2. Run locally and upload through Admin as normal.
python manage.py runserver
# -> http://127.0.0.1:8000/admin/ -> Coaching -> Transformations -> upload photos, Save

# 3. The files just landed in your local media/ folder. Commit and push them -
#    media/ is tracked in this repo on purpose (see .gitignore) specifically
#    so Vercel's deployment bundle includes them.
git add media/
git commit -m "Add real transformation photos"
git push
```

Vercel redeploys automatically on push, and the photos will be part of
that deployment's files - served by the `media/<path:path>` route in
`config/urls.py`, which works regardless of `DEBUG`. The database
record (created in step 2, already pointing at the real Neon DB) and
the file (pushed in step 3) end up in sync without any extra service.

This is a deliberate trade-off to avoid adding an external storage
dependency (Cloudinary, S3, etc.): it works well for a small, fairly
static set of photos that change occasionally through you, the
developer - not for end users uploading their own content. If that
ever changes, external storage is the right next step.

## Editing pricing / plans

Everything about a plan (name, duration, prices, features, badge, whether
it's active, and its position) is a `CoachingPlan` row, editable from
Django Admin — no template edits needed. Feature bullets are one per line
in the "Features" field.

## Checkout / payments — important

The checkout page is a **payment UI prototype**. It does not process real
money:

- No card number or CVV is ever submitted to this app (see
  `coaching/forms.py` — `CheckoutForm` deliberately excludes those fields).
  The card fields shown on the checkout page are disabled placeholders.
- Every submitted order is created with `payment_status = PENDING`.
- Nothing in this codebase ever sets an order to `PAID` automatically.
  That must only happen from a **verified callback/webhook** once a real
  Egyptian payment gateway (Fawry, Vodafone Cash, InstaPay, card
  processor, etc.) is integrated.

Before going live, replace the card panel in
`templates/coaching/checkout.html` with your chosen gateway's hosted or
tokenized checkout, and add a webhook view that updates `Order.payment_status`
based on the gateway's verified response.

## Orders

Each submission creates an `Order` with a UUID `order_id`, the customer's
details, the selected plan, and a `payment_status` of `PENDING`. View and
manage orders from Django Admin under **Coaching → Orders**.

## Contact page

`/contact/` shows contact details (currently placeholders - edit
`templates/coaching/contact.html` to add a real email/phone) plus a
form. Submissions are saved as `ContactMessage` rows, viewable and
markable as read from Django Admin under **Coaching → Contact
messages**. There's no automatic email notification - check Admin
for new messages.

## Privacy Policy page

`/privacy-policy/` is a plain-language starting template covering what
the site collects (checkout + contact form data) and how it's used.
Edit `templates/coaching/privacy_policy.html` directly - it's plain
HTML, no model behind it. **Have this reviewed by a lawyer before
relying on it for a real business**; it's a reasonable starting point,
not legal advice.

## Database

SQLite for local development (`db.sqlite3`). To move to PostgreSQL, only
the `DATABASES` setting in `config/settings.py` needs to change.

## Deploying to Vercel

Vercel runs Python as **serverless functions** — there's no persistent
disk, so SQLite can't be used in production. This project is wired for
that with an external Postgres database via `DATABASE_URL`. Locally,
it's not required — it keeps using SQLite automatically when the
variable is unset.

**Important:** you can't upload transformation photos through Admin
*on the live Vercel site* — its filesystem is read-only at runtime.
Uploads are done locally instead and pushed to GitHub; see "Updating
transformation photos (on Vercel)" above for the exact steps. Coach
photos in `static/images/` are unaffected either way (they're bundled
with the code, not uploaded).

**1. Create a Postgres database** — e.g. [Neon](https://neon.tech) (free
tier). Copy its connection string (starts with `postgresql://`).

**2. Push this project to GitHub**, then in Vercel: **Add New Project**
→ import the repo. Vercel will detect `vercel.json` automatically.

**3. Set Environment Variables** in Vercel (Project → Settings →
Environment Variables) — see `.env.example` for the full list:
`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`.

**4. Deploy.** Vercel installs `requirements.txt` and deploys `api/index.py`
as the entry point for every request (see `vercel.json`). Static files
(CSS/JS/images, including Django admin's own CSS) are served directly
by WhiteNoise from the files already in the repo — no `collectstatic`
build step needed, which keeps this reliable on Vercel's Python builder.

**5. Run migrations against the production database.** Vercel has no
shell to SSH into, so do this from your own machine, pointed at the
same Postgres database:

```bash
# in the project folder, with your venv active
export DATABASE_URL="<the same postgresql:// string you put in Vercel>"   # PowerShell: $env:DATABASE_URL="..."
python manage.py migrate
python manage.py seed_plans
python manage.py seed_transformations
python manage.py createsuperuser
```

After that, `https://<your-project>.vercel.app/` and `/admin/` are live
against the real database.

**Redeploying after code changes:** just push to GitHub — Vercel
redeploys automatically. Only re-run `migrate` manually when you've
added new migrations.

## Before deploying (general checklist)

- Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False` as environment variables.
- Set `DJANGO_ALLOWED_HOSTS` (and `DJANGO_CSRF_TRUSTED_ORIGINS`) to your real domain.
- Static files are served by WhiteNoise straight from the repo (no `collectstatic` needed on Vercel; still fine to run for other hosts).
- Use a real database (`DATABASE_URL`) — required on Vercel, optional elsewhere.
- Transformation photos are uploaded locally and pushed via `git` (`media/` is tracked) — not uploaded through the live Admin (see above).
- Replace the checkout's card panel with a real payment gateway.
