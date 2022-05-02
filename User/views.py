import json

import datetime
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from fileuploader.settings import SECRET_KEY
from .UserSeriliazer import ProfileSerializer, UserSignupSerializer, \
    ResetPasswordEmailSerializer, ResetPasswordSerializer
from .models import Profile
from .utils import LazyEncoder
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserProfiles(ListAPIView):
    serializer_class = Profile

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        return HttpResponse(profiles)


class UserProfile(ListAPIView):
    serializer_class = Profile

    def get_object(self):
        profile = Profile.objects.filter(id=self.kwargs['pk'])
        data = serialize('json', profile, cls=LazyEncoder)
        return JsonResponse(data, safe=False, status=201)


class LoginPage(CreateAPIView):
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse("User doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user:
            payload = {
                'id': user.id,
                'email': user.email,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            return JsonResponse(token, safe=False, status=200)
        else:
            return JsonResponse({'Message': "User name or password not found"}, safe=False)


class SignUp(CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        try:
            user = User.objects.get(email=email)
            return HttpResponse("User already exists")
        except:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                            last_name=lastname)
            return HttpResponse(user)


def Search(request):
    data = ''
    if request.GET.get('search'):
        data = request.GET.get('search')
        profiles = Profile.objects.filter(
            Q(name__icontains=data) | Q(username__icontains=data)
        )
        return HttpResponse(profiles)
    else:
        return HttpResponse('Input data')


class ResetPassword(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        user = User.objects.filter(email=email).first()
        if user:
            generator = PasswordResetTokenGenerator()
            token = generator.make_token(user)
            return JsonResponse(token, safe=False)
        else:
            return JsonResponse({'Message': "User not found"}, safe=False)


class ResetPasswordConfirm(UpdateAPIView):
    serializer_class = ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        token = request.headers['token']
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(email=data['email']).first()
        generator = PasswordResetTokenGenerator()
        if generator.check_token(user=user, token=token):
            user.set_password(data['password'])
            if user.check_password(data['password']):
                user.save()
                return JsonResponse({'message': 'Password successfully reset'}, safe=False)
            else:
                return JsonResponse({'message': 'Password not reset'}, safe=False)
        else:
            return JsonResponse({'message': "User doesn't exist"}, safe=False)
