import json
import jwt
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User.models import Profile
from fileuploader.settings import SECRET_KEY
from .forms import FileForm, RenameForm
from .models import File, SharedFile
from .utils import LazyEncoder


# Create your views here.
def Files(request):
    token = request.headers['authorization']
    token = token.split(" ", 1)[1]
    payload = jwt.decode(token, SECRET_KEY, algorithm=['HS256'])
    owner = Profile.objects.filter(email=payload['email']).first()
    files = File.objects.filter(owner=owner)
    data = serialize('json', files, cls=LazyEncoder)
    return JsonResponse(data, safe=False, status=200)


def GetFile(request, pk):
    file = File.objects.get(id=pk)
    data = serialize('json', file, cls=LazyEncoder)
    return JsonResponse(data, safe=False, status=200)


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
            file.extension = response["extension"]
            file.owner = owner
            file.save()
            filedata = File.objects.filter(id=file.id)
            data = serialize('json', filedata, cls=LazyEncoder)

            return JsonResponse(data, safe=False, status=201)
        else:
            return HttpResponse("Form is invalid")


@csrf_exempt
def UpdateFile(request, pk):
    if request.method == 'PUT':
        response = json.loads(request.body.decode('utf-8'))
        form = RenameForm(response)
        if form.is_valid():
            file = File.object.filter(id=pk).first()
            file.name = response['name']
            file.save()
            return JsonResponse({"Message": "File updated"}, safe=False, status=200)
        else:
            return JsonResponse({"Message": "Invalid form"}, safe=False, status=404)


@csrf_exempt
def DeleteFile(request, pk):
    if request.method == 'DELETE':
        file = File.object.filter(id=pk).first()
        file.delete()
        return JsonResponse({'Message': "File deleted"}, safe=False, status=200)


@csrf_exempt
def ShareFile(request, pk):
    if request.method == 'POST':
        file = File.objects.filter(id=pk).first()
        sharedfile = SharedFile()
        sharedfile.File = file
        to = Profile.objects.get(email=json.loads(request.body.decode('utf-8'))['to'])
        sharedfile.to = to
        sharedfile.save()
        sharedfiledata = SharedFile.objects.filter(id=sharedfile.id)
        data = serialize('json', sharedfiledata, cls=LazyEncoder)
        return JsonResponse(data, safe=False, status=201)
