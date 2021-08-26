from django import forms
from .models import *


class DepositFilterForm(forms.Form):
    term = forms.ModelChoiceField(queryset=DepositProduct.objects.all().values_list('term',flat=True).distinct())
    rate_type = forms.ModelChoiceField(queryset=DepositProduct.objects.all().values_list('rate_type',flat=True).distinct())
    interest_payment = forms.ModelChoiceField(queryset=DepositProduct.objects.all().values_list('interest_payment',flat=True).distinct())


class DateInput(forms.DateInput):
    input_type = 'date'


class Lease_application_main_form(forms.ModelForm):
    class Meta:
        model = LeaseApplication
        fields = ['applicant_legal_first_name','applicant_legal_last_name','applicant_date_of_birth',
        'nic_number','monthly_income','monthly_expenditure',
        'vehicle_make','vehicle_model','vehicle_year','vehicle_mileage',
        'vehicle_price','requiested_loan_amount','has_valuation','vehicle_valuation',
        'has_co_applicant','has_guarantor','preffered_term','first_year_max_rental',
        'co_applicant_first_name','co_applicant_last_name',
        'co_applicant_nic_number','co_applicant_monthly_income',
        'guarantor_first_name','guarantor_last_name','guarantor_nic_number',
        'date_loan_required','comments']
        widgets = {'applicant_date_of_birth': DateInput(), 'date_loan_required':DateInput()}


class Lease_contract_offer_form(forms.ModelForm):
    class Meta:
        model = LeaseContractOffer
        exclude = ['LeaseApplication','lender']