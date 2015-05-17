from django.shortcuts import render
from django.views.generic import ListView
from .models import Thread

from django import forms


from django.views.generic.edit import CreateView, UpdateView, DeleteView

class ThreadListView(ListView):
    model = Thread

class ThreadCreate(CreateView):
    model = Thread
    fields = ['title','description']
    success_url = '/thread/success'
