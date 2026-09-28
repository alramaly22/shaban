from django.contrib import admin

from .models import CoachingPlan, ContactMessage, Order, Transformation


@admin.register(CoachingPlan)
class CoachingPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "duration_months",
        "original_price",
        "discounted_price",
        "badge",
        "is_featured",
        "active",
        "order",
    )
    list_editable = ("active", "order", "is_featured")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order",)


@admin.register(Transformation)
class TransformationAdmin(admin.ModelAdmin):
    list_display = (
        "client_label",
        "goal",
        "duration",
        "featured",
        "active",
        "display_order",
    )
    list_editable = ("featured", "active", "display_order")
    ordering = ("display_order",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "customer_name",
        "plan",
        "amount",
        "currency",
        "payment_method",
        "payment_status",
        "created_at",
    )
    list_filter = ("payment_status", "payment_method", "plan")
    search_fields = ("customer_name", "email", "phone", "order_id")
    readonly_fields = ("order_id", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
