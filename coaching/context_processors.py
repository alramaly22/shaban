CONTACT = {
    "phone": "01012362225",
    "phone_intl": "+201012362225",
    "whatsapp": "201012362225",
    "email": "shbanfysl14@gmail.com",
    "address": "الجزار - كفر داوي بجوار مركز السادات - المنوفيه",
}


def contact_details(request):
    """Makes {{ CONTACT.phone }}, {{ CONTACT.email }}, {{ CONTACT.address }} available in every template."""
    return {"CONTACT": CONTACT}
