"""scm_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import home
from hub.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'depositinquiry', DepositInquiryViewSet)

hub_urlpatterns = [
    path("lease-applications/", add_lease_application_view, name="new lease application"),
    path("view-lease-applications/", view_lease_application_view, name="view lease applications"),
    path("deposit-inquiries/", all_deposit_inquiries, name="view deposit inquiries"),
    path("submit-offer/<int:application_id>/",submit_offer_view,name="submit offer"),
    path("deposit-rates/",submit_deposit_rates_view,name="deposit rates"),
    path("deposit-inquiry-standard/",deposit_inquiry_view,name="deposit inquiry"),
    path("deposit-rate-request/",post_deposit_inquiries_view,name="deposit inquiry api"),
]


urlpatterns = [
    path("", home, name="home"),

    path('admin/', admin.site.urls),

    path('users/', include("users.urls")),

    path('', include("django.contrib.auth.urls")),

    path("hub/", include(hub_urlpatterns)),

    path('apis/', include(router.urls)),
    path('apis/view-deposit-inquiries/<str:email>/',DepositInquiryList.as_view()),
    #path('apis/view-deposit-offers/<str:email>/',DepositInquiryOffersList.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
