from django.http import response
from django.shortcuts import render, redirect
from numpy import NaN
from hub.forms import DepositFilterForm, Lease_application_main_form,Lease_contract_offer_form
from hub.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from users.utils import *
import pandas as pd
from rest_framework import viewsets,generics
from .serializers import *
import requests
from django.db.models import Count,Max

@login_required(login_url="/login/")
@user_passes_test(lambda user: is_investor(user), login_url='/error/403', redirect_field_name=None)
def add_lease_application_view(request):
    if request.method == "POST":
        form = Lease_application_main_form(request.POST)
        form.instance.applicant = request.user
        if form.is_valid():
            #### show warning that the current application expires.
            existing_applications = LeaseApplication.objects.filter(application_expired=False).filter(nic_number=form.instance.nic_number)
            existing_applications.update(application_expired=True)
            form.save()
            return redirect("/hub/lease-applications/")
    else:
        most_recent_lease_application = LeaseApplication.objects.filter(
            applicant=request.user).filter(application_expired=False).order_by('-application_date')
        expired_lease_applications = LeaseApplication.objects.filter(
            applicant=request.user).filter(application_expired=True).order_by('-application_date')
        if (most_recent_lease_application.count() > 0 or expired_lease_applications.count() > 0) and 'newapp' not in request.GET:
            context = {
                "most_recent_lease_application": most_recent_lease_application[0],
                "expired_lease_applications": expired_lease_applications,
            }
            return render(request, "hub/lease-application/lease-applications-view.html", context)
        else:
            most_recent_lease_application = LeaseApplication.objects.filter(
                applicant=request.user).filter(application_expired=False).order_by('-application_date')
            form = Lease_application_main_form()
            context = {
                "form": form,
                "most_recent_lease_application": most_recent_lease_application,
            }
            return render(request, "hub/lease-application/lease-application-new.html", context)


@login_required(login_url="/login/")
@user_passes_test(lambda user: is_borrower(user), login_url='/error/403', redirect_field_name=None)
def view_lease_application_view(request):
    applications_with_offers = LeaseContractOffer.objects.filter(lender=request.user).filter(LeaseApplication__application_expired=False).values_list('LeaseApplication',flat=True).distinct() 
    lease_applications = LeaseApplication.objects.filter(application_expired=False).exclude(id__in=applications_with_offers)
    existing_offers = LeaseContractOffer.objects.filter(LeaseApplication__application_expired=False).filter(lender=request.user)

    context = {
        "lease_applications": lease_applications,
        "existing_offers": existing_offers,
    }
    return render(request, "hub/lease-application/lender/view-lease-applications.html", context)


@login_required(login_url="/login/")
@user_passes_test(lambda user: is_borrower(user), login_url='/error/403', redirect_field_name=None)
def submit_offer_view(request,application_id):
    if request.method == "POST":
        form = Lease_contract_offer_form(request.POST)
        form.instance.lender = request.user
        form.instance.LeaseApplication = LeaseApplication.objects.get(id=request.POST['application_id'])
        #print(form.errors)
        if form.is_valid():
            form.save()
            return redirect("/hub/view-lease-applications/")
    else:
        application = LeaseApplication.objects.get(id=application_id)
        form = Lease_contract_offer_form()
        context = {
            "form": form,
            "lease_application":application,
        }
        return render(request,"hub/lease-application/lender/submit-offer.html",context)


@login_required(login_url="/login/")
@user_passes_test(lambda user: is_borrower(user), login_url='/error/403', redirect_field_name=None)
def submit_deposit_rates_view(request):
    if request.method == "POST":
        deposit_rates = pd.read_csv(request.FILES['deposit_rates_file'])
        for index, row in deposit_rates.iterrows():
            DepositRate.objects.filter(lender=request.user).filter(product__id=row['id']).delete()
            dp = DepositRate(lender=request.user,product=DepositProduct.objects.get(id=row['id']),
            interest_rate=row['interest_rate'])
            dp.save()

    rates = DepositRate.objects.filter(lender=request.user)
    context = {
        "rates": rates,
    }
    return render(request,"hub/deposit/deposit-rates.html",context)

@login_required(login_url="/login/")
@user_passes_test(lambda user: is_investor(user), login_url='/error/403', redirect_field_name=None)
def deposit_inquiry_view(request):
    rate_offers = None
    if request.POST:
        form = DepositFilterForm(request.POST)
        dp = DepositProduct.objects.filter(term=request.POST['term'],rate_type=request.POST['rate_type'],interest_payment=request.POST['interest_payment'])
        if dp.count()==1:
            rate_offers = DepositRate.objects.filter(product=dp[0])
    else:
        form = DepositFilterForm()

    context={
        "form":form,
        "rate_offers":rate_offers,
    }
    
    return render(request,"hub/deposit/deposit-inquiry.html",context)

class DepositInquiryViewSet(viewsets.ModelViewSet):
    queryset = DepositInquiry.objects.all()
    serializer_class = DepositInquirySerializer

class DepositInquiryList(generics.ListAPIView):
    serializer_class = DepositInquirySerializer
    def get_queryset(self):
        inquirer_email = self.kwargs['email']
        return  DepositInquiry.objects.filter(inquirer_email=inquirer_email)

@login_required(login_url="/login/")  
@user_passes_test(is_investor)  
def post_deposit_inquiries_view(request):
    if request.POST and 'post_data' in request.POST:
        r = requests.post('http://127.0.0.1:8000/apis/depositinquiry/', data={'inquirer_email': request.user.email, 'deposit_amount': request.POST['deposit_amount'],'deposit_term':request.POST['deposit_term']})
        response = r.json() #https://stackoverflow.com/questions/48012447/django-transforming-form-data-to-rest-api-post-request
        #### how to send the status code back

    if request.POST and 'delete_data' in request.POST:
        print(request.POST['inquiry_id'])
        r = requests.delete('http://127.0.0.1:8000/apis/depositinquiry/'+request.POST['inquiry_id']+'/')
        print(r.json)

    response = requests.get('http://127.0.0.1:8000/apis/view-deposit-inquiries/'+request.user.email+'/')
    inquiries = response.json()
    context = {
        "inquiries":inquiries
    }
    return render(request,"hub/deposit/deposit-rate-request.html",context)



@login_required(login_url="/login/")  
@user_passes_test(is_borrower)
def all_deposit_inquiries(request):

    if request.POST:
        di = DepositInquiry.objects.get(id=request.POST['deposit_inq_id'])
        try:
            do = DepositOffer.objects.filter(depositinquiry=di,lender=request.user)[0]
        except:
            do = None
        if di is not None and float(request.POST['offered_rate'])>0:
            if do is not None:
                do.offered_rate =float(request.POST['offered_rate'])
            else:
                do = DepositOffer(depositinquiry=di,lender=request.user,offered_rate =float(request.POST['offered_rate']))
            do.save()

    #response = requests.get('http://127.0.0.1:8000/apis/depositinquiry/')
    #inqueries = response.json()
    inquiries = pd.DataFrame(DepositInquiry.objects.all().values('id','deposit_amount','deposit_term','inquiry_date'))
    offer_summary = pd.DataFrame(DepositOffer.objects.values('depositinquiry__id').annotate(max_rate=Max('offered_rate'),no_offers=Count('offered_rate')))
    my_offer = pd.DataFrame(DepositOffer.objects.filter(lender__email='borrower@gmail.com').values('depositinquiry__id').annotate(my_max_offer=Max('offered_rate')))

    if len(my_offer.index) == 0 and len(offer_summary.index) > 0:
        offer_summary['my_max_offer'] = None
        offer_summary = offer_summary.rename(columns={"depositinquiry__id":"id"})
        inquiries = inquiries.merge(offer_summary, on='id',how='left')
    elif len(my_offer.index) > 0 and len(offer_summary.index) > 0:
        offer_summary = offer_summary.merge(my_offer,on="depositinquiry__id",how="left")
        offer_summary = offer_summary.rename(columns={"depositinquiry__id":"id"})
        inquiries = inquiries.merge(offer_summary, on='id',how='left')
    else:
        inquiries['max_rate'] = None
        inquiries['no_offers'] = None
        inquiries['my_max_offer'] = None
    
    
    context = {
        "inquiries":inquiries.to_dict(orient="records")
    }
    return render(request,"hub/deposit/deposit-inquiries.html",context)
