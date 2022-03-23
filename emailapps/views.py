import json
from urllib import response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from emailapps.serializers import EmailSerializer
from users.models import User

# crate html email class views
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
import jwt
from rest_framework.exceptions import AuthenticationFailed

from users.serializers import UserSerializer


@api_view(['POST'])

def send_email(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms="HS256")
    except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    serializers_class = EmailSerializer(data=request.data)
    serializers_class.is_valid(raise_exception=True)
    email = serializers_class.validated_data['email']
    to_email = email
    subject = 'Test Email'
    html_template = 'email.html'
    message = render_to_string(html_template,context={"user": serializer.data.get('username')})
    text_content = strip_tags(message)
    msg=EmailMultiAlternatives(subject, text_content, to=[to_email])
    msg.attach_alternative(message, "text/html")
    msg.send()
    # send_mail(
    #         subject,
    #         message,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[to_email],
    #         fail_silently=True,
    #     )
    return Response(serializer.data.get('username'), status=200)
