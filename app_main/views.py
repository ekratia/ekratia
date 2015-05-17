from django.shortcuts import render
from django.views.generic import ListView, View
from .models import Thread, Delegate, Voter
from django.contrib.auth.decorators import login_required
from django import forms


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

class ThreadListView(ListView):
    model = Thread

class ThreadCreate(CreateView):
    model = Thread
    fields = ['title','description']
    success_url = '/thread/success'


class DelegateView(TemplateView):

	def get_context_data(self, **kwargs):
		context = super(DelegateView, self).get_context_data(**kwargs)
		context['delegates'] = Delegate.delegates(self.request.user)
		context['promminentVoters'] = Voter.mostPromminentVoters(10)
		return context

	def get_queryset(self):
		pass