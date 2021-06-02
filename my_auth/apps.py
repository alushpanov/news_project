from django.apps import AppConfig


class MyAuthConfig(AppConfig):
    name = 'my_auth'

    def ready(self):
        import my_auth.signals
