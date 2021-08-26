from django.db.models import fields
from rest_framework import serializers
from .models import DepositInquiry


class DepositInquirySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DepositInquiry
        fields = ('inquirer_email','deposit_amount','deposit_term')