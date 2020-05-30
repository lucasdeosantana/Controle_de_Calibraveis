from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class CdcConfig(AppConfig):
    name = 'CdC'

        
@receiver(post_migrate)
def my_callback(sender, **kwargs):
    if(sender.name=='CdC'):
        from .signal import populate_models
        populate_models()

        
    