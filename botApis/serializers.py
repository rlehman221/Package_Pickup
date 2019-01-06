from rest_framework import serializers
from models import FacebookUser
from models import UserDetail


class FbUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = FacebookUser
        fields = ('fb_unique_id', 'first_name', 'last_name')
