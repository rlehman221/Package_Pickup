"""ubotserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from botApis import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/CheckPrevData/(?P<userId>\w+)/$', views.CheckPrevDataAPi.as_view()),
    url(r'^api/GetFacebookUserId/(?P<userId>\w+)/(?P<first_name>\w+)/(?P<last_name>\w+)/$',
        views.FacebookUserAPi.as_view()),
    url(
        r'^api/GetUserDetails/(?P<userId>\w+)/(?P<to_first_name>.*)/(?P<to_last_name>.*)/(?P<to_mi>.*)/(?P<to_email_address>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<to_phone_number>.*)/(?P<to_ext>.*)/(?P<to_company_name>.*)/(?P<to_street_address>.*)/(?P<to_app_suite_other>.*)/(?P<to_city>.*)/(?P<to_state>.*)/(?P<to_zipCode>.*)/$',
        views.UserDetailsAPi.as_view()),

    url(r'^api/wait/', views.Loader.as_view()),
    url(
        r'^api/CheckAddressAV/(?P<userId>\w+)/(?P<to_first_name>.*)/(?P<to_last_name>.*)/(?P<to_mi>.*)/(?P<to_email_address>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<to_phone_number>.*)/(?P<to_ext>.*)/(?P<to_company_name>.*)/(?P<to_street_address>.*)/(?P<to_app_suite_other>.*)/(?P<to_city>.*)/(?P<to_state>.*)/(?P<to_zipCode>.*)/$',
        views.CheckAddressAV.as_view()),
    url(r'^api/DeleteUserInfo/(?P<userId>\w+)/$', views.DeleteUserInfo.as_view()),

    url(
        r'^api/ShippingMail/(?P<userId>.*)/(?P<shipping_to>.*)/$',
        views.ShippingAPi.as_view()),
    url(
        r'^api/AdditionalInfo/(?P<userId>.*)/(?P<additional_info>.*)/$',
        views.AdditionalInfoAPi.as_view()),
    url(
        r'^api/MailService/(?P<userId>.*)/(?P<mail_type>.*)/$',
        views.MailApi.as_view()),
    url(
        r'^api/PackageWeight/(?P<userId>.*)/(?P<weight>.*)/$',
        views.PackageWeightAPi.as_view()),
    url(
        r'^api/SchedulePickup/(?P<userId>.*)/$',
        views.SchedulePickupAPI.as_view()),
    url(
        r'^api/TEST/',
        views.TestUsps.as_view()),
    url(
        r'^api/ShippingBlocks/',
        views.ShippingBlocks.as_view()),

    url(
        r'^api/ShippingBlocksEdit/',
        views.ShippingBlocksEdit.as_view()),

    url(
        r'^api/PackageLocation/(?P<userId>.*)/$',
        views.PackageLocation.as_view()),

    url(r'^$', views.index, name='index'),
    url(r'^api/$', views.index, name='index'),

]

urlpatterns = format_suffix_patterns(urlpatterns)