import uuid

from django.core.validators import MinValueValidator
from django.db import models


class CoachingPlan(models.Model):
    """
    A purchasable coaching package (e.g. 3 / 6 / 12 months).

    Everything shown on the pricing section - price, discount,
    features, badge - lives here so it can be edited from Django
    Admin without touching a template.
    """

    name = models.CharField(
        max_length=100,
        help_text="e.g. '3 Months', '6 Months', '12 Months'",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Used in the checkout URL, e.g. '3-months'.",
    )
    duration_months = models.PositiveSmallIntegerField()

    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short one-line description shown under the plan name.",
    )

    # One feature per line in the admin form -> one bullet per line on site.
    features = models.TextField(
        help_text="One feature per line. These render as a bullet list on the pricing card."
    )

    badge = models.CharField(
        max_length=40,
        blank=True,
        help_text="e.g. STARTER, BEST VALUE, BEST COMMITMENT",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Visually highlight this plan as the recommended option.",
    )

    active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers display first."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "duration_months"]

    def __str__(self):
        return self.name

    @property
    def feature_list(self):
        """Return the features textarea split into a clean list of lines."""
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    @property
    def savings(self):
        return self.original_price - self.discounted_price


class Order(models.Model):
    """
    A coaching application / checkout submission.

    payment_status starts at PENDING and must only ever be moved to
    PAID by a verified callback/webhook from a real payment gateway -
    never set automatically by the checkout form itself.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentMethod(models.TextChoices):
        CARD = "CARD", "Card Payment"
        FAWRY = "FAWRY", "Fawry"
        VODAFONE_CASH = "VODAFONE_CASH", "Vodafone Cash"
        INSTAPAY = "INSTAPAY", "InstaPay"

    class TrainingLocation(models.TextChoices):
        HOME = "HOME", "Home"
        GYM = "GYM", "Gym"
        BOTH = "BOTH", "Both"

    class Experience(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    plan = models.ForeignKey(
        CoachingPlan, on_delete=models.PROTECT, related_name="orders"
    )

    # Customer information
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    main_goal = models.CharField(max_length=255)
    training_experience = models.CharField(max_length=20, choices=Experience.choices)
    training_location = models.CharField(max_length=10, choices=TrainingLocation.choices)
    notes = models.TextField(blank=True)

    # Order / payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="EGP")
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name} ({self.plan.name})"


class Transformation(models.Model):
    """
    A real client before/after transformation, editable from Django
    Admin. Images are optional - the homepage renders an elegant
    placeholder for any that are missing, so this section is always
    safe to display even before real photos are uploaded.
    """

    client_label = models.CharField(
        max_length=100,
        help_text="e.g. 'Ahmed, 28' or 'Client A' - never a fabricated name.",
    )
    before_image = models.ImageField(upload_to="transformations/", blank=True)
    after_image = models.ImageField(upload_to="transformations/", blank=True)

    goal = models.CharField(max_length=150, blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. '12 Weeks'.")
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short, factual result description.",
    )
    testimonial = models.TextField(
        blank=True,
        help_text="A real client quote. Leave blank until a real one is provided.",
    )

    featured = models.BooleanField(
        default=False,
        help_text="Show as the large featured transformation with the before/after slider.",
    )
    active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers display first."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.client_label


class ContactMessage(models.Model):
    """
    A message submitted through the public Contact page. Purely a
    record for the coach to read and reply to by email/phone - there's
    no automated reply or notification system here on purpose, to keep
    the project simple. Check Django Admin for new messages.
    """

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"
