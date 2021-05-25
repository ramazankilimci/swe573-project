from django.apps import AppConfig


class MediclesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medicles'

'''
    def ready(self):
        from medicles import updater
        updater.start()
'''     