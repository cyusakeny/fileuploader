import json
import jwt

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from User.models import Profile
from fileuploader.settings import SECRET_KEY
from .forms import FileForm, RenameForm
from .models import File


# Create your views here.
def Files(request):
    files = File.objects.all()
    return HttpResponse(files)


def GetFile(request, pk):
    file = File.objects.get(name=pk)
    return HttpResponse(file.id)


@csrf_exempt
def AddFile(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf-8'))
        token = request.headers['authorization']
        token = token.split(" ", 1)[1]
        payload = jwt.decode(token, SECRET_KEY, algorithm=['HS256'])
        form = FileForm(response)
        if form.is_valid():
            file = File()
            owner = Profile.objects.filter(email=payload['email']).first()
            file.name = response["name"]
            file.size = response["size"]
            file.owner = owner
            file.save()
            return HttpResponse(file)
        else:
            return HttpResponse("Form is invalid")


@csrf_exempt
def UpdateFile(request):
    if request.method == 'PUT':
        token = request.headers['authorization']
        token = token.split(" ", 1)[1]
        payload = jwt.decode(token, SECRET_KEY, algorithm=['HS256'])
        response = json.loads(request.body.decode('utf-8'))
        form = RenameForm(response)
        owner = Profile.objects.filter(email=payload['email']).first()
        if form.is_valid():
            file = File.object.filter()
            return HttpResponse('File saved')
        else:
            return HttpResponse('Not saved')


@csrf_exempt
def DeleteFile(request):
    if request.method == 'DELETE':
        return HttpResponse("Delete")
