from django.shortcuts import render
from django.views.generic import ListView
from .models import Thread

class ThreadListView(ListView):
    model = Thread
