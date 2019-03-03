import json

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, Group, Receipt

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
    information = data['info']
    diction = data['dic']
    complete = data['completed']
    r = Receipt(info=information, dic=diction, completed=complete)
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
        information = data['info']
        diction = data['dic']
        complete = data['completed']
        receipt.info = information
        receipt.dic = diction
        receipt.completed = complete
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
