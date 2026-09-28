from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, ContactForm
from .models import CoachingPlan, Order, Transformation


def home(request):
    plans = CoachingPlan.objects.filter(active=True)

    transformations = Transformation.objects.filter(active=True)
    featured_transformation = transformations.filter(featured=True).first()
    other_transformations = transformations.exclude(
        pk=featured_transformation.pk
    ) if featured_transformation else transformations

    return render(
        request,
        "coaching/home.html",
        {
            "plans": plans,
            "featured_transformation": featured_transformation,
            "other_transformations": other_transformations,
        },
    )


def sitemap(request):
    plans = CoachingPlan.objects.filter(active=True)
    return render(
        request, "sitemap.xml", {"plans": plans}, content_type="application/xml"
    )


def checkout(request, slug):
    plan = get_object_or_404(CoachingPlan, slug=slug, active=True)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.plan = plan
            order.amount = plan.discounted_price
            order.currency = "EGP"
            # payment_status defaults to PENDING and must stay that way
            # here - it can only move to PAID via a verified gateway
            # callback/webhook, never inside this view.
            order.save()
            return redirect("coaching:confirmation", order_id=order.order_id)
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = CheckoutForm()

    return render(
        request,
        "coaching/checkout.html",
        {"plan": plan, "form": form},
    )


def confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, "coaching/confirmation.html", {"order": order})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks - your message has been sent. The coach will get back to you soon.",
            )
            return redirect("coaching:contact")
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ContactForm()

    return render(request, "coaching/contact.html", {"form": form})


def privacy_policy(request):
    return render(request, "coaching/privacy_policy.html")


def refund_policy(request):
    return render(request, "coaching/refund_policy.html")


def terms_and_conditions(request):
    return render(request, "coaching/terms.html")
