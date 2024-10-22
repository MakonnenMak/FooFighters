import json

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, Paygroup, Receipt
from django.contrib.auth.models import User

@method_decorator(csrf_exempt, name='dispatch')
def getAll(request):
    allreceipts = Receipt.objects.all()
    data = serializers.serialize('json', allreceipts)
    json_receipt = json.loads(data)
    return JsonResponse({'receipt': json_receipt})

@method_decorator(csrf_exempt, name='dispatch')
def getReceipt(request, receipt_id):
    try:
        receipt = Receipt.objects.filter(pk=receipt_id)
        data = serializers.serialize('json', receipt)
        json_receipt = json.loads(data)
        return JsonResponse({'receipt': json_receipt[0]['fields'], 'id': json_receipt[0]['pk']})
    except:
        return JsonResponse({"Status": "Couldn't find that receipt id: %d." % (receipt_id)}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
def createReceipt(request):
    data = request.POST
    emailname = data['name']
    information = data['info']
    diction = data['dic']
    venmo = data['venmo_id']
    nclist = data['notcompletedlist']
    tlist = data['totlist']
    imgsrc = data['src']
    print(imgsrc)
    r = Receipt(info=information, dic=diction, name =emailname, venmo_id=venmo, notcompletedlist=nclist, totlist=tlist, src=imgsrc)
    r.save()
    pkid = r.id
    try:
        receipt = Receipt.objects.filter(pk=pkid)
        data = serializers.serialize('json', receipt)
        json_receipt = json.loads(data)
        return JsonResponse({'receipt': json_receipt[0]['fields'], 'id': json_receipt[0]['pk']})
    except:
        return JsonResponse({"Status": "Couldn't find that receipt id: %d." % (pkid)}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
def updateReceipt(request, receipt_id):
    try:
        receipt = Receipt.objects.get(pk=receipt_id)
        data = request.POST
        emailname = data['name']
        information = data['info']
        diction = data['dic']
        complete = data['completed']
        venmo = data['venmo_id']
        nclist = data['notcompletedlist']
        clist = data['completedlist']
        tlist = data['totlist']
        imgsrc = data['src']
        receipt.info = information
        receipt.dic = diction
        receipt.completed = complete
        receipt.name = emailname
        receipt.venmo_id = venmo
        receipt.notcompletedlist = nclist
        receipt.completedlist = clist
        receipt.totlist = tlist
        receipt.src = imgsrc
        receipt.save()
        receipt = Receipt.objects.filter(pk=receipt_id)
        data = serializers.serialize('json', receipt)
        json_receipt = json.loads(data)
        return JsonResponse({'receipt': json_receipt[0]['fields'], 'id': json_receipt[0]['pk']})
    except:
        return JsonResponse({"Status": "Couldn't find that receipt id: %d." % (receipt_id)}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
def deleteReceipt(request, receipt_id):
    try:
        Receipt.objects.filter(pk=receipt_id).delete()
        return JsonResponse({"Status": "Deleted Successfully!"})
    except:
        return JsonResponse({"Status": "Couldn't find that receipt id: %d." % (receipt_id)}, status=404)

# @method_decorator(csrf_exempt, name='dispatch')
# def getProfile(request, profile_id):
#     try:
#         users = User.objects.get(pk=profile_id)
#         profile = Profile.objects.filter(user=users)
#         dicuser = {}
#         dicuser['username'] = users.get_username()
#         dicuser['email'] = users.email
#         dicuser['password'] = users.password
#         dicuser['fullname'] = users.get_full_name()
#         data = serializers.serialize('json', profile)
#         json_profile = json.loads(data)
#         return JsonResponse({'profile': json_profile[0]['fields'], 'id': json_profile[0]['pk'], 'users': dicuser})
#     except:
#         return JsonResponse({"Status": "Couldn't find that receipt id: %d." % (profile_id)}, status=404)

# @method_decorator(csrf_exempt, name='dispatch')
# def createProfile(request):
#     data = request.POST
#     name = data['username']
#     password = data['password']
#     firstname = data['first_name']
#     lastname = data['last_name']
#     email = data['email']
#     venmo = data['venmo_name']
#     accumulate = data['accumulated']
#     u = User.objects.create_user(username = name, password=password, first_name = firstname, last_name = lastname, email = email)
#     p = Profile()
#     p.venmo_name = venmo
#     p.accumulated = accumulate
#     p.user = u
#     p.save()
#     pkid = p.pk
#     try:
#         users = User.objects.get(pk=u.pk)
#         profile = Profile.objects.filter(user=users)
#         dicuser = {}
#         dicuser['username'] = users.get_username()
#         dicuser['email'] = users.email
#         dicuser['password'] = users.password
#         dicuser['fullname'] = users.get_full_name()
#         data = serializers.serialize('json', profile)
#         json_profile = json.loads(data)
#         return JsonResponse({'profile': json_profile[0]['fields'], 'id': json_profile[0]['pk'], 'user': dicuser})
#     except:
#         return JsonResponse({"Status": "Couldn't find that profile id: %d." % (pkid)}, status=404)

# @method_decorator(csrf_exempt, name='dispatch')
# def updateProfile(request, profile_id):
#     try:
#         users = User.objects.get(pk=profile_id)
#         data = request.POST
#         name = data['username']
#         password = data['password']
#         firstname = data['first_name']
#         lastname = data['last_name']
#         email = data['email']
#         venmo = data['venmo_name']
#         accumulate = data['accumulated']
#         users.username = name
#         users.password = password
#         users.email = email
#         users.first_name = firstname
#         users.last_name = lastname
#         users.save()
#         dicuser = {}
#         dicuser['username'] = users.get_username()
#         dicuser['email'] = users.email
#         dicuser['password'] = users.password
#         dicuser['fullname'] = users.get_full_name()
#         profile = Profile.objects.get(user=users)
#         profile.venmo_name = venmo
#         profile.accumulated = accumulate
#         profile.user = users
#         profile.save()
#         newprof = Profile.objects.filter(user=users)
#         data = serializers.serialize('json', newprof)
#         json_profile = json.loads(data)
#         return JsonResponse({'profile': json_profile[0]['fields'], 'id': json_profile[0]['pk'], 'user': dicuser})
#     except:
#         return JsonResponse({"Status": "Couldn't find that profile id: %d." % (profile_id)}, status=404)

# @method_decorator(csrf_exempt, name='dispatch')
# def deleteProfile(request, profile_id):
#     try:
#         u = User.objects.get(pk=profile_id)
#         Profile.objects.filter(user=u).delete()
#         return JsonResponse({"Status": "Deleted Successfully!"})
#     except:
#         return JsonResponse({"Status": "Couldn't find that profile id: %d." % (profile_id)}, status=404)