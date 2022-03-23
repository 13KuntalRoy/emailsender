#crete emailserializer
from email import message
from rest_framework import serializers
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

