from ekratia.delegates.models import Delegate
from ekratia.referendums.models import Referendum, ReferendumUserVote
from ekratia.users.models import User


def db_clear_votes():
    Delegate.objects.all().delete()
    ReferendumUserVote.objects.all().delete()


def db_clear_users():
    User.objects.all().delete()


def db_clear_referendums():
    Referendum.objects.all().delete()


def db_clear_all():
    db_clear_votes()
    db_clear_referendums()
    db_clear_users()
