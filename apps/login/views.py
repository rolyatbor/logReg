# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def register(request):
    if request.method == 'POST':
        newUser = User.objects.add_user(request.POST)
        if newUser['status']:
            request.session['first'] = newUser['user'].first
            request.session['word'] = "Registered"
            return redirect('success:index')

        else:
            for error in newUser['errors']:
                messages.error(request, error)
            return redirect('user:index')
    
    else:
        return redirect('user:index')

def login(request):
    if request.method == 'POST':
        user = User.objects.check_user(request.POST)
        if user['status']:
            request.session['first'] = user['user'].first
            request.session['word'] = "Logged In"
            return redirect('success:index')
        else:
            messages.error(request, user['errors'])
            return redirect('user:index')
    else:
        return redirect('user:index')


def logout(request):
    if request.method == 'POST':
        request.session.clear()
    return redirect('user:index')