from ekratia.conversations.models import Thread
from ekratia.referendums.models import Referendum

from django_email import EmailTemplate

import logging
logger = logging.getLogger('ekratia')


def notify_comment_node(request, node, object_type):
    """
    Method to create new comment for the current Thread
    """
    root = node.get_root()

    # Find Referendum or Conversation
    object = None

    if object_type == 'referendum':
        try:
            object = Referendum.objects.get(comment=root)
            object_type = 'referendum'
        except Referendum.DoesNotExist:
            object = None
    elif object_type == 'conversation':
        try:
            object = Thread.objects.get(comment=root)
            object_type = 'conversation'
        except Thread.DoesNotExist:
            object = None

    if not object:
        return False
    # Count and save comments of the object
    # TODO: count and update comments
    object.count_comments()
    # Send message to parent comment user
    try:
        mail = EmailTemplate("comment_node")
        mail.context = {'comment': request.data,
                        'user': request.user,
                        'request': request,
                        'you': node.user,
                        'object': object,
                        'object_type': object_type
                        }
        mail.set_subject('%s replied your comment on %s'
                         % (request.user.get_full_name_or_username,
                            object.title))

        if request.user != node.user:
            mail.send_to_user(node.user)

    except ValueError, e:
        logger.error("Could not send email %s" % e)

    # Send message to owner
    try:
        mail = EmailTemplate("comment_root")
        mail.context = {'comment': request.data,
                        'user': request.user,
                        'request': request,
                        'you': root.user,
                        'object': object,
                        'object_type': object_type
                        }
        mail.set_subject('%s has a new comment' % object.title)
        if request.user != root.user and node.user != root.user:
            mail.send_to_user(root.user)

    except ValueError, e:
        logger.error("Could not send email %s" % e)
