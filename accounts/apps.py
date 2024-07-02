from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
