from django.core.signals import request_finished
from django.db.models.signals import post_save, post_delete

from ekratia.delegates.models import Delegate


# Callback functions
def my_callback(sender, **kwargs):
    print("Request finished!")


def process_model_saved(sender, instance, **kwargs):
    if sender == Delegate:
        print "Delgate created"
        instance.user.compute_pagerank()


def process_model_deleted(sender, instance, **kwargs):
    if sender == Delegate:
        print "Delgate deleted"
        instance.user.compute_pagerank()


# Signals
request_finished.connect(my_callback)
post_save.connect(process_model_saved)
post_delete.connect(process_model_deleted)
