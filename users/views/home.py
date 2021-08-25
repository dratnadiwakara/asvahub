from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render
from users.utils import *


@login_required(login_url="/login/")
def home(request):
    if(is_investor(request.user)):
        return render(request, "users/index.html", {})
    if(is_borrower(request.user)):
        return render(request, "users/index-borrower.html", {})
