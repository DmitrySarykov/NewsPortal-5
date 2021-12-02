import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


from datetime import date, timedelta 
from news.models import Category, Post,User
 
logger = logging.getLogger(__name__)

# Рассылка еженедельных новостей 
def week_news():
    print('Новости за неделю')
    today = date.today()
    last_week = today - timedelta(days=7)
    site = Site.objects.get_current()
    categories = Category.objects.exclude(subscribers=None)
    # Отправляем новости по каждой категории всем её подписчикам
    for category in categories:
        list_email = category.subscribers.exclude(email='').values_list('email',flat=True)
        if list_email :
            news=Post.objects.filter(date__range=[last_week,today],category=category).order_by('date')
            msg = EmailMultiAlternatives(
                subject=f'{category.name}. Новости за неделю.',
                to=list_email, 
            )
            html_content = render_to_string('news_week.html',{'news_list':news,'site':site})
            msg.attach_alternative(html_content, "text/html")
            msg.send()

 
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            week_news,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  
            id="week_news",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'week_news'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")