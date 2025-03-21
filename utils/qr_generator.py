import qrcode
from io import BytesIO
from django.http import HttpResponse

def generate_qr(event_url):
    qr = qrcode.make(event_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

def serve_qr(request, event_id):
    event_url = f"https://yourfrontend.com/events/{event_id}"
    qr_code = generate_qr(event_url)
    return HttpResponse(qr_code, content_type="image/png")
