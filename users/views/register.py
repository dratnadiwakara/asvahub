from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, HttpResponse

from users.forms import *


def register(response, ut):
    if response.method == "POST":
        usertype = response.POST['usertype']
        if usertype == 'admin':
            user_data_form = AdminForm(response.POST)
        elif usertype == 'investor':
            user_data_form = InvestorForm(response.POST)
        elif usertype == 'borrower':
            user_data_form = BorrowerForm(response.POST)
        else:
            return HttpResponse(status=404)

        if user_data_form.is_valid():
            user = user_data_form.save()
            group = Group.objects.get(name=str(response.POST['usertype']))
            user.groups.add(group)
            return redirect("/login")
    else:
        usertype = ut
        if usertype == 'admin':
            user_data_form = AdminForm()
        elif usertype == 'investor':
            user_data_form = InvestorForm()
        elif usertype == 'borrower':
            user_data_form = BorrowerForm()
        else:
            return HttpResponse(status=404)

    return render(response, "users/register.html", {"usertype": usertype, "user_data_form": user_data_form})
