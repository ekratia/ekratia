from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView


from .models import Thread, Comment
# Create your views here.

class ThreadListView(ListView):
    model = Thread

class ThreadCreate(CreateView):
    model = Thread
    fields = ['title','description']
    success_url = '/thread/success'
