from django.db.models.signals import post_save, post_delete

from ekratia.delegates.models import Delegate
from ekratia.users.models import User


# Callback functions
def process_model_saved(sender, instance, **kwargs):
    if sender == Delegate:
        instance.user.compute_pagerank()
    if sender == User:
        instance.update_votes()


def process_model_deleted(sender, instance, **kwargs):
    if sender == Delegate:
        instance.user.compute_pagerank()


# Signals
post_save.connect(process_model_saved)
post_delete.connect(process_model_deleted)
