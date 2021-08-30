from django.db.models import fields
from rest_framework import serializers
from .models import *


class DepositOfferSerializer(serializers.ModelSerializer):
    lender_name = serializers.ReadOnlyField(source = 'lender.legal_name')
    lender_id = serializers.ReadOnlyField(source = 'lender.id')
    class Meta:
        model = DepositOffer
        fields = ['offered_rate','offered_date','lender_name','lender_id']

class DepositInquirySerializer(serializers.ModelSerializer):
    depositoffers = DepositOfferSerializer(many=True, read_only=True)
    class Meta:
        model = DepositInquiry
        fields = ('id','inquirer_email','deposit_amount','deposit_term','inquiry_date','depositoffers')


##############
class TrackAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackApp
        fields = ['order', 'title', 'duration']

class AlbumAppSerializer(serializers.ModelSerializer):
    trackapps = TrackAppSerializer(many=True, read_only=True)
    class Meta:
        model = AlbumApp
        fields = ['album_name', 'artist', 'trackapps']