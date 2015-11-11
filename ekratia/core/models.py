from django.db.models.signals import post_save, post_delete

from ekratia.delegates.models import Delegate
from ekratia.users.models import User

import logging
logger = logging.getLogger('ekratia')


# Callback functions
def process_model_saved(sender, instance, **kwargs):
    if sender == Delegate:
        logger.debug('Delegate Saved signal by : %s' % instance.user.username)
        logger.debug('Delegate added : %s' % instance.delegate.username)
        instance.delegate.compute_pagerank()
    if sender == User:
        instance.update_votes()


def process_model_deleted(sender, instance, **kwargs):
    logger.debug('process_model_deleted')
    if sender == Delegate:
        logger.debug(
            'Delegate Deleted signal by : %s' % instance.user.username)
        logger.debug('Delegate deleted : %s' % instance.delegate.username)
        instance.user.compute_pagerank()
        instance.delegate.compute_pagerank()

# Signals
post_save.connect(process_model_saved)
post_delete.connect(process_model_deleted)
