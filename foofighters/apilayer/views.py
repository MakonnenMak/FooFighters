import json
import requests

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



@method_decorator(csrf_exempt, name='dispatch')
def getData(self, re_id):
    url = "http://localhost:8000/models/receipt/" + str(re_id)
    try:
        response= requests.get(url)
        return JsonResponse({'status': response.status_code, 'data': response.json()})

    except Exception as e:
        return self.STATUS_FAIL, json.dumps(
            {'Status': 'Failed to process request.[ %s ]' % (str(e))})

@method_decorator(csrf_exempt, name='dispatch')
def getallreceipts(self, email):
    url = "http://localhost:8000/models/receipt/all"
    try:
        response= requests.get(url)
        parse = response.json()
        resultlist = []
        for i in parse['receipt']:
            x = json.dumps(i['fields']['totlist'])
            t = x[2:len(x)-2]
            f = t.split(', ')
            for j in f:
                if (j == email):
                    resultlist.append(i['fields'])
                    break
        return JsonResponse({'status': response.status_code, 'data': resultlist})

    except Exception as e:
        return self.STATUS_FAIL, json.dumps(
            {'Status': 'Failed to process request.[ %s ]' % (str(e))})

@method_decorator(csrf_exempt, name='dispatch')
def sendData(request, email):
    response = request.POST
    datatosend = {
        'name': response['name'],
        'info': response['info'],
        'dic': response['dic'],
        'completed': response['completed'],
        'notcompletedlist': response['notcompletedlist'],
        'completedlist:': "",
        'totlist': response['totlist'],
        'venmo_id': response['venmo_id'],
        'src': response['src'],
    }
    r = requests.post("http://localhost:8000/models/receipt/create", data = datatosend)
    return JsonResponse({'data': r.json()})