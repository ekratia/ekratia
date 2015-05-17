from django.contrib import admin

# Register your models here.

from django.db.models import get_models, get_app


for model in get_models(get_app('app_main')):
	admin.site.register(model)