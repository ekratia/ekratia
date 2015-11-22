from ekratia.delegates.models import Delegate
from ekratia.referendums.models import Referendum, ReferendumUserVote


def db_clear_votes():
    Delegate.objects.all().delete()
    ReferendumUserVote.objects.all().delete()


def db_clear_users():
    from ekratia.users.models import User
    User.objects.all().delete()


def db_clear_referendums():
    Referendum.objects.all().delete()


def db_clear_all():
    db_clear_votes()
    db_clear_referendums()
    db_clear_users()


def change_picture_size(url, width=70, height=70):
    """
    Change the facebook url to use a thumbnail
    """
    return url.split('?')[0] + u'?width=%i&height=%i' % (width, height)
