import json

import datetime
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fileuploader.settings import SECRET_KEY as seckey
from .models import Profile
from .utils import LazyEncoder


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
        payload = {
            'id': user.id,
            'email': user.email,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, seckey, algorithm='HS256').decode('utf-8')
        return HttpResponse(token)


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
