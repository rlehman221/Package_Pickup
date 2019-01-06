# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

# from django.shortcuts import render
import urllib
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FacebookUser
from .models import UserDetail
from .models import Shipping
from .models import MailService
from .models import PackageWeight
from .models import SuccessfulPickup
from .serializers import FbUsersSerializers
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import time
import datetime
import requests
from bs4 import BeautifulSoup
from SOAPpy import WSDL
from SOAPpy import SOAPProxy
import json
from helpers import UsStates


# FrontEnd View
def index(request):
    return render(request, 'index.html')


# FrontEnd view for api url
def indexApi(request):
    return render(request, 'index.html')


# Save new Facebook users unique id
# url --> http://34.212.2.126:8000/api/fbusers/{{messenger user id}}/
class FacebookUserAPi(APIView):
    def get(self, request, userId, first_name, last_name):

        first_name = urllib.unquote_plus(first_name)
        last_name = urllib.unquote_plus(last_name)
        try:
            fuser = FacebookUser.objects.get(fb_unique_id=userId)
            return HttpResponse('')

        except ObjectDoesNotExist:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            SaveFacebookUsers = FacebookUser(fb_unique_id=userId, first_name=first_name, last_name=last_name,
                                             created_date_time=st)
            SaveFacebookUsers.save()
            fuser = FacebookUser.objects.get(fb_unique_id=userId)
            # serializer = FbUsersSerializers(fuser, many=True)

            return HttpResponse('')


# Get user details and save it
# http://34.212.2.126:8000/api/GetUserDetails/{{messenger user id}}/{{pickup_address_first_name}}/{{pickup_address_last_name}}/none/{{pickup_address_email}}/{{pickup_phone_number}}/0/none/{{pickup_address_street}}/0/{{pickup_address_city}}/{{pickup_address_state}}/{{pickup_address_zipcode}}/
class UserDetailsAPi(APIView):
    def get(self, request, userId, to_first_name, to_last_name, to_mi, to_email_address, to_phone_number, to_ext,
            to_company_name, to_street_address, to_app_suite_other, to_city, to_state, to_zipCode):

        userId = urllib.unquote_plus(userId)
        to_first_name = urllib.unquote_plus(to_first_name)
        to_last_name = urllib.unquote_plus(to_last_name)
        to_mi = urllib.unquote_plus(to_mi)
        to_email_address = urllib.unquote_plus(to_email_address)
        to_phone_number = urllib.unquote_plus(to_phone_number)
        to_ext = urllib.unquote_plus(to_ext)
        to_company_name = urllib.unquote_plus(to_company_name)
        to_street_address = urllib.unquote_plus(to_street_address)
        to_app_suite_other = urllib.unquote_plus(to_app_suite_other)
        to_city = urllib.unquote_plus(to_city)
        to_state = urllib.unquote_plus(to_state)
        to_zipCode = urllib.unquote_plus(to_zipCode)

        try:
            check_first = UserDetail.objects.get(fb_unique_id=userId)
            if_first = check_first.is_first
            if if_first == 0:
                pass
            else:
                try:
                    delete_user_id = UserDetail.objects.get(fb_unique_id=userId)
                    delete_user_id.delete()
                except ObjectDoesNotExist:
                    pass
        except ObjectDoesNotExist:
            pass

        try:
            fuser = UserDetail.objects.get(fb_unique_id=userId)
            return HttpResponse('{"messages": [ {"text": " "}]}')

        except ObjectDoesNotExist:
            saveAddressData = UserDetail(fb_unique_id=userId, first_name=to_first_name,
                                         last_name=to_last_name, MI=to_mi, email_address=to_email_address,
                                         phone_number=to_phone_number,
                                         ext=to_ext, company_name=to_company_name, street_address=to_street_address,
                                         apt_suite_other=to_app_suite_other, city=to_city, state=to_state,
                                         zip=to_zipCode,
                                         is_business=1)

        saveAddressData.save()
        return HttpResponse('{"messages": [ {"text": " "}]}')


# Check if User have previous data
# http://34.212.2.126:8000/api/CheckPrevData/{{messenger user id}}
class CheckPrevDataAPi(APIView):
    def get(self, request, userId):

        try:
            fuser = UserDetail.objects.get(fb_unique_id=userId)
            # return HttpResponse(str(fuser))
            UserDetail.objects.filter(fb_unique_id=userId).update(is_first=1)

            # Return this response if Previous Information Found
            return HttpResponse(
                '{ "messages": [ { "text":  "{{ first name }} do you want to use your previous pickup information?", "quick_replies": [ { "title":"Yes", "block_names":["mail_main"] } , { "title":"No", "block_names":["PickupBusinessAddress"] } ] } ] }')

        except ObjectDoesNotExist:

            return HttpResponse('')


# Delete Previous info from the UserDetail TABLE
class DeleteUserInfo(APIView):
    def get(self, request, userId):
        delete_user_id = UserDetail.objects.get(fb_unique_id=userId)
        delete_user_id.delete()
        # data = UserDetail.objects.get(fb_unique_id=userId)
        return HttpResponse('')


# Make Loading Spinner
class Loader(APIView):
    @staticmethod
    def get(request):
        return HttpResponse(
            '{ "messages": [  { "attachment": { "type": "image", "payload": { "url": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/1f430a36197347.57135ca19bbf5.gif"} } } ] }')


# @Php server api for checking pickup availability
def checkcarrierpickupavailability(address, city, state, zipCode):
    check_carrier_pickup_availability = "http://34.212.2.126/CheckCarrierPickupAvailability.php"

    payload = (('Address', address), ('City', city), ('State', state), ('Zip', zipCode))
    req = requests.get(url=check_carrier_pickup_availability, params=urllib.urlencode(payload))

    n = json.dumps(req.json())
    o = json.loads(n)
    if o['response'] == 'ok':
        return 'ok'
    else:
        return 'error'


# Check Address Availability api
class CheckAddressAV(APIView):
    def get(self, request, userId, to_first_name, to_last_name, to_mi, to_email_address, to_phone_number, to_ext,
            to_company_name, to_street_address, to_app_suite_other, to_city, to_state, to_zipCode):

        userId = urllib.unquote_plus(userId)
        to_first_name = urllib.unquote_plus(to_first_name)
        to_last_name = urllib.unquote_plus(to_last_name)
        to_mi = urllib.unquote_plus(to_mi)
        to_email_address = urllib.unquote_plus(to_email_address)
        to_phone_number = urllib.unquote_plus(to_phone_number)
        to_ext = urllib.unquote_plus(to_ext)
        to_company_name = urllib.unquote_plus(to_company_name)
        to_street_address = urllib.unquote_plus(to_street_address)
        to_app_suite_other = urllib.unquote_plus(to_app_suite_other)
        to_city = urllib.unquote_plus(to_city)
        to_state = urllib.unquote_plus(to_state)
        to_zipCode = urllib.unquote_plus(to_zipCode)

        abb = UsStates.abbreviations(to_state)
        if abb:
            check_response = checkcarrierpickupavailability(to_street_address, to_city, abb, to_zipCode)
            pass
        else:
            # Response if user entered wrong State name
            return HttpResponse(
                '{"messages": [ {"text": "It seems you entered wrong state name"}]}'
            )

        if check_response != 'ok':
            # Response if Pickup address not available
            return HttpResponse(


                '{ "messages": [ { "text":  "you can try again but the information you have entered isn’t available for the address you have entered", "quick_replies": [ { "title":"Re-Try", "block_names":["PickupAddress"] } ] } ] }'
            )
        else:
            # Custom attributes for bot
            return HttpResponse('{ "set_attributes": { "addressFound": "found", "step": "2" } }')


# Save Shipping Data
class ShippingAPi(APIView):
    def get(self, request, userId, shipping_to):

        try:
            check_first = Shipping.objects.get(fb_unique_id=userId)
            if_first = check_first.fb_unique_id
            if if_first == '':
                pass
            else:
                try:
                    delete_data = Shipping.objects.get(fb_unique_id=userId)
                    delete_data.delete()
                except ObjectDoesNotExist:
                    pass
        except ObjectDoesNotExist:
            pass

        save_shipping = ''
        if shipping_to == 'm':
            save_shipping = Shipping(fb_unique_id=userId, in_at_mailbox=1)
        elif shipping_to == 'p':
            save_shipping = Shipping(fb_unique_id=userId, on_the_porch=1)
        elif shipping_to == 'fd':
            save_shipping = Shipping(fb_unique_id=userId, front_door=1)
        elif shipping_to == 'bd':
            save_shipping = Shipping(fb_unique_id=userId, back_door=1)
        elif shipping_to == 'sd':
            save_shipping = Shipping(fb_unique_id=userId, side_door=1)
        else:
            save_shipping = Shipping(fb_unique_id=userId, front_door=1)

        save_shipping.save()

        return HttpResponse('{"messages": [ {"text": " "}]}')
        # return HttpResponse(userId + '' + shipping_to)


# Save Additional Instructions
class AdditionalInfoAPi(APIView):
    def get(self, request, userId, additional_info):

        additional_info = urllib.unquote_plus(additional_info)

        try:
            Shipping.objects.filter(fb_unique_id=userId).update(additional_instructions=additional_info)
        except ObjectDoesNotExist:
            pass

        return HttpResponse('{"messages": [ {"text": " "}]}')


# Save Mail Data
class MailApi(APIView):
    def get(self, request, userId, mail_type):

        try:
            check_first = MailService.objects.get(fb_unique_id=userId)
            if_first = check_first.fb_unique_id
            if if_first == '':
                pass
            else:
                try:
                    delete_data = MailService.objects.get(fb_unique_id=userId)
                    delete_data.delete()
                except ObjectDoesNotExist:
                    pass
        except ObjectDoesNotExist:
            pass
        save_mail = ''
        if mail_type == 'pme':
            save_mail = MailService(fb_unique_id=userId, priority_mail_service=1)
        elif mail_type == 'pm':
            save_mail = MailService(fb_unique_id=userId, priority_mail=1)
        elif mail_type == 'fc':
            save_mail = MailService(fb_unique_id=userId, first_class_package_service=1)
        else:
            save_mail = MailService(fb_unique_id=userId, priority_mail=1)
        pass

        save_mail.save()

        return HttpResponse('{"messages": [ {"text": " "}]}')


# save Package Weight
class PackageWeightAPi(APIView):
    def get(self, request, userId, weight):

        weight = float(weight)
        if weight < 1:
            # Response if user enter weight less than 1
            return HttpResponse(

                '{ "messages": [ { "text":  "{{ first name }} It seems you entered invalid weight the weight must be greater than 0 ", "quick_replies": [ { "title":"re-enter the weight", "block_names":["estimated weight for the package"] }  ] } ] }'

            )
        else:
            try:
                check_first = PackageWeight.objects.get(fb_unique_id=userId)
                if_first = check_first.fb_unique_id
                if if_first == '':
                    pass
                else:
                    try:
                        delete_data = PackageWeight.objects.get(fb_unique_id=userId)
                        delete_data.delete()
                    except ObjectDoesNotExist:
                        pass
            except ObjectDoesNotExist:
                pass

            try:
                save_weight = PackageWeight(fb_unique_id=userId, package_weight=weight)
                save_weight.save()
            except ObjectDoesNotExist:
                pass

            return HttpResponse('{"messages": [ {"text": " "}]}')


# Convert pickup location into api format @note porch not available in stamps.com api so we used knock on door or ring bell
def pickup_location(userId):
    shipping_data = Shipping.objects.get(fb_unique_id=userId)
    if shipping_data.in_at_mailbox != 0:
        parcel_location = 'InOrAtMailbox'
    elif shipping_data.on_the_porch != 0:
        parcel_location = 'KnockOnDoorOrRingBell'
    elif shipping_data.front_door != 0:
        parcel_location = 'FrontDoor'
    elif shipping_data.back_door != 0:
        parcel_location = 'BackDoor'
    elif shipping_data.side_door != 0:
        parcel_location = 'SideDoor'
    else:
        parcel_location = 'KnockOnDoorOrRingBell'
    return parcel_location


# Final
# Schedule Pickup. Use saved data using userID @note userId if facebook unique id
# http://34.212.2.126:8000/api/SchedulePickup/{{messenger user id}}/
class SchedulePickupAPI(APIView):
    def get(self, request, userId):

        try:
            UserData = UserDetail.objects.get(fb_unique_id=userId)
            first_name = UserData.first_name
            last_name = UserData.last_name
            phone = UserData.phone_number
            phone = phone[:10]

            address = UserData.street_address
            city = UserData.city
            state = UserData.state
            zipCode = UserData.zip
        except ObjectDoesNotExist:
            # Response if any required information is missing
            return HttpResponse(
                '{ "messages": [ { "text":  "{{ first name }} it seems some of your basic information is missing Please enter your pickup information", "quick_replies": [ { "title":"Pickup information", "block_names":["PickupAddress"] } , { "title":"No", "block_names":["Default answer"] } ] } ] }'
            )
            pass
        try:
            weightData = PackageWeight.objects.get(fb_unique_id=userId)
            mail_type = MailService.objects.get(fb_unique_id=userId)

            first_class_pieces = mail_type.first_class_package_service
            express_mail_pieces = mail_type.priority_mail_service
            priority_mail_pieces = mail_type.priority_mail

            weight_pounds = weightData.package_weight
        except ObjectDoesNotExist:
            # Response if MAil (Shipment type) information is missing
            return HttpResponse(
                '{ "messages": [ { "text":  "{{ first name }} it seems you did not enter your mail information ", "quick_replies": [ { "title":"Mail information", "block_names":["mail_main"] } , { "title":"No", "block_names":["Default answer"] } ] } ] }'
            )

        try:
            shippingData = Shipping.objects.get(fb_unique_id=userId)

            pickupLocation = pickup_location(userId)
            additional_instructions = shippingData.additional_instructions
        except ObjectDoesNotExist:
            # Response if shipment location is missing
            return HttpResponse(
                '{ "messages": [ { "text":  "{{ first name }} it seems you did not enter shipment information ", "quick_replies": [ { "title":"Shipment information", "block_names":["Shipping"] } , { "title":"No", "block_names":["Default answer"] } ] } ] }'
            )

        weight_pounds = float(weight_pounds)
        if weight_pounds < 1:
            # Response if weight is less than 1
            return HttpResponse(

                '{ "messages": [ { "text":  "{{ first name }} It seems you entered invalid weight the weight must be greater than 0 ", "quick_replies": [ { "title":"re-enter the weight", "block_names":["estimated weight for the package"] }  ] } ] }'

            )

        # Everything good sp far let make final call to schedule
        # Call to php server api
        schedule_carrier_pickup_availability = "http://34.212.2.126/ScheduleCarrierPickup.php"

        abb = UsStates.abbreviations(state)

        if abb:
            payload = (('FirstName', first_name), ('LastName', last_name), ('PhoneNumber', phone), ('Address', address),
                       ('City', city), ('State', abb), ('Zip', zipCode), ('first_class_pieces', first_class_pieces),
                       ('express_mail_pieces', express_mail_pieces), ('priority_mail_pieces', priority_mail_pieces),
                       ('additional_instructions', additional_instructions), ('weight_pounds', weight_pounds),
                       ('pickupLocation', pickupLocation))
            pass
        else:
            # Response if State name is wrong
            return HttpResponse(
                '{"messages": [ {"text": "It seems you entered wrong state name"}]}'
            )

        req = requests.get(url=schedule_carrier_pickup_availability, params=urllib.urlencode(payload))

        # BreakPoint for testing
        # return HttpResponse(req)
        # exit()

        n = json.dumps(req.json())
        o = json.loads(n)

        if o['response'] == 'ok':
            pickup_date = o['PickupDate']
            pickup_day = o['PickUpDayOfWeek']
            confirmation_number = o['ConfirmationNumber']
            from datetime import datetime
            # convert date into db format
            date = datetime.strptime(pickup_date, '%m/%d/%Y').strftime('%Y-%m-%d')

            successful_pickup = SuccessfulPickup(fb_unique_id=userId, pickup_date=date,
                                                 pickup_day_of_week=pickup_day, confirmation_number=confirmation_number,
                                                 is_success=1)

            successful_pickup.save()

            # Response if pickup successful created
            return HttpResponse(
                '{"messages": [ {"text": "Pickup successful scheduled. Pickup Date ' + pickup_date + 'Your '
                                                                                                     'confirmation '
                                                                                                     'number is ' +
                confirmation_number + ' see you on ' + pickup_day + ' "}]}')
        else:
            # Response if api give any unknown error
            return HttpResponse(
                 '{ "messages": [ { "text":  "You can try again but the information you have entered isn’t available for the address you have entered", "quick_replies": [ { "title":"Re-Try", "block_names":["PickupAddress"] } ] } ] }'
            )


# Shipping Blocks
class ShippingBlocks(APIView):
    def get(self, request):
        # Response -> Show shipping locations to the user
        return HttpResponse(

            '{ "messages": [ { "text":  "Where should we look for your shipment?", "quick_replies": [ { "title":"In/at mailbox", "block_names":["In/at mailbox"] },{ "title":"On the porch", "block_names":["on the porch"] },{ "title":"Front door", "block_names":["front door"] },{ "title":"Back door", "block_names":["back door"] },{ "title":"Side door", "block_names":["side door"] } ] } ] }'

        )


# Shipping block in edit mode
class ShippingBlocksEdit(APIView):
    def get(self, request):
        # Response -> Show shipping locations to the user @note this is only in edit mode
        return HttpResponse(

            '{ "messages": [ { "text":  "Where should we look for your shipment?", "quick_replies": [ { "title":"In/at mailbox", "block_names":["In_at_mailbox_edit"] },{ "title":"On the porch", "block_names":["on_the_porch_edit"] },{ "title":"Front door", "block_names":["front_door_edit"] },{ "title":"Back door", "block_names":["back_door_edit"] },{ "title":"Side door", "block_names":["side_door_edit"] } ] } ] }'

        )


# Show package location and shipment type in the confirmation block
class PackageLocation(APIView):
    def get(self, request, userId):
        location = pickup_location(userId)
        if location == 'KnockOnDoorOrRingBell':
            location = 'On the Porch'
        elif location == 'InOrAtMailbox':
            location = 'In/AtMailbox'

        shipment_type = MailService.objects.get(fb_unique_id=userId)
        if shipment_type.priority_mail_service == 1:
            shipment_type = 'Priority Mail service'
        elif shipment_type.priority_mail == 1:
            shipment_type = 'Priority Mail'
        elif shipment_type.first_class_package_service == 1:
            shipment_type = 'First class package service'

        # Set Attributes
        return HttpResponse(
            '{ "set_attributes": { "PackageLocation": "' + location + '", "ShipmentType": "' + shipment_type + '" } }'
        )


# TEST CLASSES *******************************************************************
# Just for testing
class TestUsps(APIView):
    def get(self, request):
        pass

        # return HttpResponse(
        #
        #     '{ "messages": [ { "text":  "Where should we look for your shipment?", "quick_replies": [ { "title":"In/at mailbox", "block_names":["In/at mailbox"] },{ "title":"On the porch", "block_names":["on the porch"] },{ "title":"Front door", "block_names":["front door"] },{ "title":"Back door", "block_names":["back door"] },{ "title":"Side door", "block_names":["side door"] } ] } ] }'
        #
        # )
        # return HttpResponse('{"messages": [ {"text": "Something went wrong... Please check your address again"}]}')
        # first_name = "sam"
        # last_name = "Beg"
        # phone = "5555555555"
        #
        # address = "1990 Grand Ave"
        # city = "El Segundo"
        # state = "CA"
        # zipCode = "90245"
        #
        # first_class_pieces = 0
        # express_mail_pieces = 1
        # priority_mail_pieces = 0
        # other_pieces = 0
        # weight_pounds = 30
        # pickupLocation = "FrontDoor"
        #
        # schedule_carrier_pickup_availability = "http://34.212.2.126/ScheduleCarrierPickup.php"
        #
        # payload = (('FirstName', first_name), ('LastName', last_name), ('PhoneNumber', phone), ('Address', address),
        #            ('City', city), ('State', state), ('Zip', zipCode), ('first_class_pieces', first_class_pieces),
        #            ('express_mail_pieces', express_mail_pieces), ('priority_mail_pieces', priority_mail_pieces),
        #            ('other_pieces', other_pieces), ('weight_pounds', weight_pounds), ('pickupLocation', pickupLocation))
        # req = requests.get(url=schedule_carrier_pickup_availability, params=urllib.urlencode(payload))

    pass
