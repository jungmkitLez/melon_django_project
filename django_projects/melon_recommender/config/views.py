from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'base.html'


