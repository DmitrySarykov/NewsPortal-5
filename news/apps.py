from django.apps import AppConfig

class NewsConfig(AppConfig):
    name = 'news'
    verbose_name = 'База данных'

    def ready(self):
        import news.signals