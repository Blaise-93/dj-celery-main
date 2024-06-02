from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import FormView, CreateView
from .forms import ReviewForm
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

from .models import Review


def review(request, *args, **kwargs):
    form = ReviewForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ReviewForm(request.POST)
       
        if form.is_valid():
            print('form is valid')
            review = Review()

            review.name = form.cleaned_data['name']
            review.email = form.cleaned_data['email']
            review.review = form.cleaned_data['review']
            review.save()
            
            form.send_email()
            messages.info(request, 'We got your message')
            return redirect('task1:review')
   
    return render(request,  'task1/review.html', context)


def files(file):
    """ A helper function to upload and read individual file when sending emails to
    the user. """
    with open(file, "r") as f:
        data = f.read()
        return data
