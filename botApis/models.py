# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.
# Users Facebook Data
class FacebookUser(models.Model):
    fb_unique_id = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_date_time = models.DateTimeField('date Created', default=timezone.now)

    def __str__(self):
        return self.fb_unique_id


# Users Details
class UserDetail(models.Model):

    fb_unique_id = models.IntegerField()
    first_name = models.CharField(max_length=100, blank=True, null=True)
    MI = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    ext = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    apt_suite_other = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    is_business = models.IntegerField(blank=True, null=True)
    av = models.CharField(max_length=10, blank=True, null=True)
    is_first = models.IntegerField(default=0)
    created_date_time = models.DateTimeField('date Created', default=timezone.now)
    update_date_time = models.DateTimeField('date Updated', default=timezone.now)

    def __str__(self):
        return str(self.email_address)


class Shipping(models.Model):
    fb_unique_id = models.IntegerField()
    in_at_mailbox = models.IntegerField(default=0)
    on_the_porch = models.IntegerField(default=0)
    front_door = models.IntegerField(default=0)
    back_door = models.IntegerField(default=0)
    side_door = models.IntegerField(default=0)
    additional_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.fb_unique_id)


class MailService(models.Model):
    fb_unique_id = models.IntegerField()
    priority_mail_service = models.IntegerField(default=0)
    priority_mail = models.IntegerField(default=0)
    first_class_package_service = models.IntegerField(default=0)

    def __str__(self):
        return str(self.fb_unique_id)


class PackageWeight(models.Model):
    fb_unique_id = models.IntegerField()
    package_weight = models.CharField(default=0, max_length=200)

    def __str__(self):
        return str(self.fb_unique_id)


class SuccessfulPickup(models.Model):
    fb_unique_id = models.IntegerField()
    pickup_date = models.DateField(default=timezone.now)
    pickup_day_of_week = models.TextField(default=0)
    response = models.TextField(default=0)
    confirmation_number = models.TextField(default=0)
    is_success = models.IntegerField(default=0)
    created_date_time = models.DateTimeField('date Created', default=timezone.now)

    def __str__(self):
        return str(self.confirmation_number)
