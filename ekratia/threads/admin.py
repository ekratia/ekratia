from django.contrib import admin
from ekratia.threads.models import Thread, Comment

# Register Thread models in the admin
admin.site.register(Thread)
admin.site.register(Comment)
