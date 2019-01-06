# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import FacebookUser
from .models import UserDetail
from .models import Shipping
from .models import MailService
from .models import PackageWeight
from .models import SuccessfulPickup
# Register your models here.
admin.site.register(FacebookUser)
admin.site.register(UserDetail)
admin.site.register(Shipping)
admin.site.register(MailService)
admin.site.register(PackageWeight)
admin.site.register(SuccessfulPickup)
