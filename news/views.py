from django.shortcuts import render
from .models import Recipient,Mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def register_receipient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        if name and email:
            recipient = Recipient(name=name, email=email)
            recipient.save()
            return render(request, 'register_success.html', {'name': name, 'email': email})
        else:
            return render(request, 'register.html', {'error': 'Please provide both name and email.'})
        return render(request, 'register_success.html', {'name': name, 'email': email})
    return render(request, 'register.html')


def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        cta_text = request.POST.get('cta_text')
        cta = request.POST.get('cta')

        recipients = Recipient.objects.values_list('email', flat=True)

        # Save mail to DB
        Mail.objects.create(subject=subject, body=body, cta_text=cta_text, cta=cta)

        # Render HTML content
        html_content = render_to_string('email_template.html', {
            'subject': subject,
            'body': body,
            'cta_text': cta_text,
            'cta': cta
        })
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],
            bcc=list(recipients)
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return render(request, 'send_success.html', {
            'subject': subject,
            'body': body,
            'cta_text': cta_text,
            'cta': cta
        })
    return render(request, 'send_newsletter.html')