from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from .models import PostCategory, User
 
 
@receiver(m2m_changed, sender=PostCategory)
def send_post(sender, instance, action, **kwargs):
    if action=="post_add":
        categories = instance.category.all()
        users = User.objects.filter(category__in = categories).exclude(email='').distinct()
        site = Site.objects.get_current()

        for user in users:
            msg = EmailMultiAlternatives(
                subject=instance.title,
                to=[user.email], 
            )
            html_content = render_to_string('post.html',{'post':instance,'user':user,'site':site})
            msg.attach_alternative(html_content, "text/html")
            msg.send()
