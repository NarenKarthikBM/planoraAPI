from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now, timedelta

from events.models import (
    Event,  # Adjust the import based on your models (check this!!)
    EventNotificationConfig,
)
from planoraAPI.settings import env

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="name@gmail.com")

# def send_registration_otp_mail(otp, email):
#     send_mail(
#         "Complete Your Signup - Verify Your Email Now",
#         f"Your OTP is {otp}",
#         "your-email@gmail.com",
#         [email],
#         fail_silently=False,
#     )


def send_verification_email(user, otp):
    subject = "Complete Your Signup - Verify Your Email Now"

    context = {
        "user_name": user.name,
        "otp_code": otp,
    }

    html_content = render_to_string(
        "templates/email_templates/otp_email_template.html", context
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


def send_event_reminder_mail(event, recipient_list):
    subject = f"📅 Reminder: {event.name} - Happening Soon!"

    # Prepare context for the email template
    context = {
        "attendee_name": "[Attendee Name]",  # Replace dynamically
        "event_name": event.name,
        "event_date": event.start_datetime.date(),
        "event_time": event.start_datetime.time(),
        "location": event.location,
        "event_link": f"https://yourwebsite.com/events/{event.id}",
    }

    html_content = render_to_string(
        "templates/email_templates/reminder_email.template.html", context
    )  # Load template
    text_content = strip_tags(html_content)  # Plain text fallback

    email = EmailMultiAlternatives(
        subject, text_content, EMAIL_HOST_USER, recipient_list
    )
    email.attach_alternative(html_content, "text/html")  # Attach HTML version
    email.send()


def send_thank_you_mail(event, recipient_list):
    subject = f"🎉 Thank You for Attending {event.name}!"

    context = {
        "attendee_name": "[Attendee Name]",  # Dynamically replace with actual name
        "event_name": event.name,
        "feedback_form_link": f"https://yourwebsite.com/feedback/{event.id}",
    }

    html_content = render_to_string(
        "templates/email_templates/thankyou_email_template.html", context
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, EMAIL_HOST_USER, [recipient_list]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_welcome_mail(user):
    subject = "You're In! Start Your Journey with Planora"

    context = {
        "user_name": user.name,
        "dashboard_link": "https://yourwebsite.com/dashboard",
    }

    html_content = render_to_string(
        "templates/email_templates/welcome_email_template.html", context
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()


def scan_and_send_event_reminders():
    """Scans for upcoming events in the next 24 hours and sends reminder emails if not already sent."""
    upcoming_events = Event.objects.filter(
        start_datetime__gte=now(),
        start_datetime__lte=now() + timedelta(hours=24),
        notification_config__reminder_mail_sent=False,  # Only events where email hasn't been sent
    )

    for event in upcoming_events:
        recipient_list = list(
            event.attendees.values_list("email", flat=True)
        )  # Get all attendees' emails

        if recipient_list:  # Ensure there are recipients
            send_event_reminder_mail(event, recipient_list)

            # Update mail_sent status to True
            EventNotificationConfig.objects.filter(event=event).update(mail_sent=True)


def send_event_cancellation_mail(event, recipient_list):
    subject = f"🚨 Important: {event.name} Has Been Canceled"

    # Prepare email context
    context = {
        "attendee_name": "[Attendee Name]",  # Replace dynamically
        "event_name": event.name,
        "event_link": "https://yourwebsite.com/events",
    }

    html_content = render_to_string(
        "event_cancellation_email_template.html", context
    )  # Load template
    text_content = strip_tags(html_content)  # Plain text fallback

    email = EmailMultiAlternatives(
        subject, text_content, "your@email.com", recipient_list
    )
    email.attach_alternative(html_content, "text/html")  # Attach HTML version
    email.send()


def send_event_update_mail(event, recipient_list):
    subject = f"📢 Important Update: {event.name} Rescheduled!"

    # Prepare email context
    context = {
        "attendee_name": "[Attendee Name]",  # Replace dynamically
        "event_name": event.name,
        "event_date": event.start_datetime.date(),
        "start_time": event.start_datetime.time(),
        "end_time": event.end_datetime.time(),
        "location": event.location,
        "event_link": f"https://yourwebsite.com/events/{event.id}",
    }

    html_content = render_to_string(
        "templates/email_templates/modification_email_template.html", context
    )  # Load template
    text_content = strip_tags(html_content)  # Plain text fallback

    email = EmailMultiAlternatives(
        subject, text_content, "your@email.com", recipient_list
    )
    email.attach_alternative(html_content, "text/html")  # Attach HTML version
    email.send()
