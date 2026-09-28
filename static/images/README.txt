Coach photos expected by the templates (all optional - the site
falls back to a clean placeholder for any that are missing):

  static/images/coach-hero.jpg      - Hero section (main/strongest photo)
  static/images/coach-about.jpg     - "Meet Your Coach" section
  static/images/coach-training.jpg  - "How It Works" section
  static/images/coach-cta.jpg       - Final "Ready to Start?" section

Use four DIFFERENT photos, not the same one repeated. Portrait
orientation works best for coach-hero.jpg, coach-about.jpg and
coach-training.jpg (roughly 4:5 or 3:4). coach-cta.jpg is used as a
wide background image behind the final call-to-action, so a landscape
or vertical shot both work - it's shown at reduced opacity under a
dark gradient.

If you want to change these paths, update the four {% static %} tags
in templates/coaching/home.html.

Real client transformation photos (before/after) are NOT static files -
they're uploaded through Django Admin under Coaching > Transformations,
and are stored under media/transformations/.
