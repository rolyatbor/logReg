# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if 'first' not in request.session:
        return redirect('user:index')
    return render(request, 'success/index.html')