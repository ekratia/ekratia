from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView

from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .models import Thread, Comment
# Create your views here.

class ThreadListView(ListView):
    model = Thread
    template_name='threads/list.html'

class ThreadCreateView(CreateView):
    model = Thread
    template_name='threads/create.html'
    fields = ['title','description']

    def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS,  _('New thread created'))
    	
		return super(ThreadCreateView, self).form_valid(form)  
    
class ThreadDetailView(DetailView):
    model = Thread
    template_name = "threads/detail.html"

