from django.core.mail import send_mail


def send_registration_otp_mail():
    send_mail(
        "Registration OTP",
        "Your OTP is 123456",
        "your-email@gmail.com",
        ["recipient@example.com"],  # To
        fail_silently=False,
    )
