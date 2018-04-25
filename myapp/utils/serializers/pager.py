# -*- coding:UTF-8 -*-

from rest_framework import serializers

from myapp import models


class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'






