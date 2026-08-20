from urllib.parse import urlencode
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

# Configurable Learning platform URL (defaults to localhost:8009 in development)
LEARNING_PLATFORM_URL = getattr(settings, 'LEARNING_PLATFORM_URL', 'http://127.0.0.1:8009/')


@ensure_csrf_cookie
def gateway_home(request: HttpRequest) -> HttpResponse:
    """Landing page for edukom.ng connecting Edukom HR and Edukom Learning."""
    context = {
        'learning_url': LEARNING_PLATFORM_URL,
    }
    return render(request, 'core/gateway.html', context)


@ensure_csrf_cookie
def hr_home(request: HttpRequest) -> HttpResponse:
    """Main Edukom HR landing page with all 01-04 sections and content on one page."""
    context = {
        'learning_url': LEARNING_PLATFORM_URL,
    }
    return render(request, 'core/index.html', context)


def learning_redirect(request: HttpRequest) -> HttpResponse:
    """Direct navigation route to Edukom Learning Platform."""
    return redirect(LEARNING_PLATFORM_URL)


def contact(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return redirect('home')

    form = ContactForm(request.POST) if 'ContactForm' in globals() else None
    
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip() or 'New Contact Form Submission'
    message = request.POST.get('message', '').strip()
    honeypot = request.POST.get('website', '')

    if honeypot or not name or not email or not message:
        query = urlencode({'sent': 1 if honeypot else 0})
        return HttpResponseRedirect(f"{reverse('home')}?{query}#contact")

    body_html = (
        f"<p><strong>Name:</strong> {name}</p>"
        f"<p><strong>Email:</strong> {email}</p>"
        f"<p><strong>Message:</strong><br>{message}</p>"
    )
    body_text = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    try:
        send_mail(
            subject,
            body_text,
            settings.DEFAULT_FROM_EMAIL,
            [getattr(settings, 'CONTACT_TO_EMAIL', settings.DEFAULT_FROM_EMAIL)],
            html_message=body_html,
            fail_silently=False,
        )
        query = urlencode({'sent': 1})
    except Exception:
        query = urlencode({'sent': 0})

    return HttpResponseRedirect(f"{reverse('home')}?{query}#contact")
