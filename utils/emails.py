from django.core.mail import send_mail


def send_registration_otp_mail(otp, email):
    send_mail(
        "Registration OTP for Planora",
        f"Your OTP is {otp}",
        "your-email@gmail.com",
        [email],
        fail_silently=False,
    )
