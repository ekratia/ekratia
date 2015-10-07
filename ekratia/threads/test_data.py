from .models import Thread, Comment
from datetime import datetime
import random


def random_date():
    return datetime(2015, 9, random.randint(1, 16),
                    random.randint(0, 23), random.randint(0, 60))

t = Thread.objects.create(title='Thread title', user_id=1,
                          description="Lorem ipsum dolor sit amet")
c = Comment.add_root(content="Comment", thread_id=t.id, user_id=1)
c1 = c.add_child(content="Comment 1", user_id=1)
c2 = c.add_child(content="Comment 2", user_id=1)
c1a = c1.add_child(content="Comment 1a", user_id=1)
c1b = c1.add_child(content="Comment 1b", user_id=1)
c2a = c2.add_child(content="Comment 2a", user_id=1)
c2a1 = c2a.add_child(content="Comment 2a1", user_id=1)
c2a1 = c2a.add_child(content="Comment 2a1", user_id=1)

x = c.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)
x = x.add_child(content="Many children", user_id=1)

for c in Comment.objects.all():
    c.date = random_date()
    c.save()
