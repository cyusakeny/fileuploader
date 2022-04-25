import json

import datetime
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fileuploader.settings import SECRET_KEY
from .models import Profile
from .utils import LazyEncoder
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def UserProfiles(request):
    profiles = Profile.objects.all()
    return HttpResponse(profiles)


def UserProfile(request, pk):
    profile = Profile.objects.filter(id=pk)
    data = serialize('json', profile, cls=LazyEncoder)
    return JsonResponse(data, safe=False)


@csrf_exempt
def LoginPage(request):
    if request.method == 'POST':
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


@csrf_exempt
def SignUp(request):
    if request.method == 'POST':
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


@csrf_exempt
def ResetPassword(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        user = User.objects.filter(email=email).first()
        if user:
            generator = PasswordResetTokenGenerator()
            token = generator.make_token(user)
            return JsonResponse(token, safe=False)
        else:
            return JsonResponse({'Message': "User not found"}, safe=False)


@csrf_exempt
def ResetPasswordConfirm(request):
    if request.method == 'POST':
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
