from io import open_code
from django.db import models
from django.db.models.fields.related import ForeignKey
from users.models import User
from django.db.models.deletion import CASCADE, PROTECT
import django.utils.timezone

class LeaseApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=PROTECT)
    application_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    applicant_legal_first_name = models.CharField(max_length=200)
    applicant_legal_last_name = models.CharField(max_length=200)
    applicant_date_of_birth = models.DateField()
    nic_number = models.CharField(max_length=12)
    monthly_income = models.FloatField(default=0)
    monthly_expenditure = models.FloatField(default=0)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.PositiveIntegerField()
    vehicle_mileage = models.PositiveIntegerField()
    vehicle_price = models.FloatField()
    requiested_loan_amount = models.PositiveIntegerField()
    preffered_term = models.PositiveIntegerField(null=True,blank=True)
    date_loan_required = models.DateField()
    first_year_max_rental = models.PositiveIntegerField(null=True,blank=True)
    has_valuation = models.BooleanField(default=False)
    vehicle_valuation = models.FloatField(null=True,blank=True)
    has_co_applicant = models.BooleanField(default=False)
    co_applicant_first_name = models.CharField(max_length=200,null=True,blank=True)
    co_applicant_last_name = models.CharField(max_length=200,null=True,blank=True)
    co_applicant_nic_number = models.CharField(max_length=12,null=True,blank=True)
    co_applicant_monthly_income = models.FloatField(default=0,null=True,blank=True)
    has_guarantor = models.BooleanField(default=False)
    guarantor_first_name = models.CharField(max_length=200,null=True,blank=True)
    guarantor_last_name = models.CharField(max_length=200,null=True,blank=True)
    guarantor_nic_number = models.CharField(max_length=12,null=True,blank=True)
    application_expired = models.BooleanField(default=False)
    comments = models.TextField(null=True,blank=True)


class LeaseContractOffer(models.Model):
    LeaseApplication = models.ForeignKey(LeaseApplication,on_delete=CASCADE)
    lender = models.ForeignKey(User,on_delete=CASCADE,limit_choices_to={'groups__name': 'borrower'})
    loan_amount = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    loan_term = models.PositiveIntegerField()
    monthly_rental = models.FloatField(null=True)
    documentation_fees = models.FloatField()
    other_fees = models.FloatField(default=0)
    stamp_duty = models.FloatField()
    fees_included_in_loan_amount = models.BooleanField(default=False)
    penalty_interest_rate = models.FloatField()
    penalty_interest_after = models.PositiveIntegerField()
    prepayment_rebate = models.FloatField(null=True,blank=True)
    first_payment_in = models.CharField(max_length=20,choices=(("Immediate","Immediate"),("In a month","In a month")))
    structured_lease = models.BooleanField(default=False)
    comments = models.TextField(null=True,blank=True)

class StructuredLeasePayments(models.Model):
    LeaseContractOffer = models.ForeignKey(LeaseContractOffer,on_delete=CASCADE)
    starting_month = models.PositiveIntegerField()
    ending_month = models.PositiveIntegerField()
    rental_amount = models.FloatField()


class DepositProduct(models.Model):
    term = models.PositiveIntegerField(choices=((1,1),(3,3),(6,6),(12,12),(15,15),(18,18),(24,24),(36,36),(48,48),(60,60)))
    rate_type = models.CharField(max_length=20,choices=(("Normal","Normal"),("Senior Citizen","Senior Citizen")))
    interest_payment = models.CharField(max_length=20,choices=(("Monthly","Monthly"),("Maturity","Maturity")))

    def __str__(self):
        return str(self.term) + " month - "\
               + str(self.rate_type) + \
               " - interest at " + str(self.interest_payment)

class DepositRate(models.Model):
    class Meta:
        unique_together = (('lender', 'product'),)
    lender = models.ForeignKey(User,on_delete=CASCADE,limit_choices_to={'groups__name': 'borrower'})
    product = models.ForeignKey(DepositProduct,on_delete=CASCADE)
    interest_rate = models.FloatField(null=True,blank=True)
    last_updated = models.DateTimeField(default=django.utils.timezone.now)


class DepositInquiry(models.Model):
    inquirer_email = models.EmailField()
    deposit_amount = models.PositiveIntegerField()
    deposit_term = models.PositiveIntegerField()