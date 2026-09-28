from django import forms

from .models import ContactMessage, Order


class CheckoutForm(forms.ModelForm):
    """
    Customer information + payment method selection.

    Note: card fields (cardholder name, card number, expiry, CVV) are
    intentionally NOT part of this form or the Order model. They exist
    only as UI in the checkout template. When a real payment gateway
    is integrated, card entry should be replaced entirely by that
    gateway's hosted/tokenized checkout - card numbers and CVV must
    never be submitted to or stored by this Django app.
    """

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "email",
            "phone",
            "age",
            "gender",
            "main_goal",
            "training_experience",
            "training_location",
            "notes",
            "payment_method",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"placeholder": "Full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+20 1xx xxx xxxx", "autocomplete": "tel"}),
            "age": forms.NumberInput(attrs={"placeholder": "Age", "min": 14, "max": 90}),
            "main_goal": forms.TextInput(attrs={"placeholder": "e.g. Fat loss, muscle gain, general fitness"}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Anything the coach should know (optional)"}),
        }

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 14 or age > 90:
            raise forms.ValidationError("Please enter a valid age.")
        return age


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+20 1xx xxx xxxx (optional)", "autocomplete": "tel"}),
            "message": forms.Textarea(attrs={"rows": 6, "placeholder": "How can the coach help you?"}),
        }
