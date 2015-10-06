from .models import Thread, Comment

t = Thread.objects.create(title='Thread title', user_id=1, description="Lorem ipsum dolor sit amet")
c = Comment.add_root(content="Comment", thread_id=t.id, user_id=1)
c1 = c.add_child(content="Comment 1", user_id=1)
c2 = c.add_child(content="Comment 2", user_id=1)
c1a = c1.add_child(content="Comment 1a", user_id=1)
c1b = c1.add_child(content="Comment 1b", user_id=1)
c2a = c2.add_child(content="Comment 2a", user_id=1)
