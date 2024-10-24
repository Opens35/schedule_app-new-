from django.shortcuts import render
from .models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm

class SignupView(CreateView):
    template_name = "accounts/signup.html"
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("event_create")