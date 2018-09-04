

# Create your views here.

from __future__ import unicode_literals
from django.shortcuts import render
import django

from django.db import models

from django.shortcuts import render


import os
import datetime


def midasroot(request):
	time = datetime.datetime.now()

	request.session["fav_color"] = "blue"
	fav_color = request.session["fav_color"]

	try:
		currentuser = request.user
	except:
		currentuser = 'Not Signed In'

	context = {
		'time':time,
		'color':fav_color,
		'user':currentuser

	}

	return render(request, 'midasroot.html', 	context)


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('midasroot')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form,})

