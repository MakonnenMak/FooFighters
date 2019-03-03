import json
import requests
import base64

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders


import argparse
from enum import Enum
import io

import os
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw



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
    imgst = response['img-url']
    temp = imgst.split(',')
    imgstring = temp[1]
    
    imgdata = base64.b64decode(imgstring)
    x = os.getcwd()
    filename = x + '/apilayer/static/apilayer/receipt.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    
    with open(filename, "rb") as image:
        x = image.read()
        b = bytearray(x)

    classifier = predict(b)
    if(classifier == "negative"):
        return JsonResponse({"Status": "That picture is not a receipt!"})
    
    retout = receiptdetect(filename)
    listofitems = getresultimage(retout)
    dic={}
    notcompletelist = []
    for i in listofitems:
        for j in range(0, len(i)):
            if(j == 0):
                notcompletelist.append(i[0])
                dic[i[j]] = ""
            if(j == 1):
                dic[i[j-1]] = i[j]
    datatosend = {
        'name': email,
        'info': "",
        'dic': dic,
        'completed': "False",
        'notcompletedlist': response['recipients'],
        'completedlist:': "",
        'totlist': response['recipients'],
        'venmo_id': response['venmo_id'],
        'src': filename,
    }
    
    r = requests.post("http://localhost:8000/models/receipt/create", data = datatosend)
    return JsonResponse({'data': r.json()})

def predict(b):
    pred_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/2a06e04e-b624-42a3-8a8f-421522c966dc/image?iterationId=5894cad8-b55f-4f54-b62e-46f01ab5adc6"
    pred_key = "a677bbd662d14e72b96709296c5afe26"
    content_type = "application/octet-stream"
    data = b
    headers = {"Prediction-key": pred_key, "Content-Type": content_type}
    r = requests.post(pred_url, data=data, headers=headers)
    return json.loads(r.content)['predictions'][0]['tagName']


def food_extract(line):
    foods=[]
    line=line.split(' ')
    if ('B' in line) or ('T' in line) or ('1b' in line) or ('lb' in line):
        foods.append(line)
    return foods

#def maybe_food(line):
#    food = wn.synset('food.n.02')
#    nltk_fod_list=list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
#
#    line=line.split(' ')
#    maybe_foods=[]
#    for i in range (0,len(line)):
#        if line[i].lower() in nltk_fod_list:
#            if len(line[i])>2:
#                if '\n' not in line[i]:
#                    maybe_foods.append(line)
#    return maybe_foods


def cleaner(line):  
    line=line[0]
    food=""
    cost=""
    skip=[]
    for i in range(0,len(line)):
        if line[i].isalpha():
            food+=(line[i].lower()+" ")
    
    for i in range (0,len(line)):
        if line[i]=='.':
            price_point=i
    
    for i in range (0,len(line)):
        if i==(price_point-1) and line[i].isdigit():
            cost+=line[i] 
        if i==(price_point):
            cost+=line[i]
        if i==(price_point+1) and line[i].isdigit():
            cost+=line[i]     
        #Kind of hardcoded 
        if i==(price_point+2) and line[i].isdigit():
            cost+=line[i]
    

    return [food,cost] 

def getresultimage(pipelist):
    newlist = []
    tempstring=""
    for i in pipelist:
        temp = i.decode("utf-8")
        newlist.append(temp)
    init_food_list=[]
    maybe_list=[]
    for line in newlist:
        if(len(food_extract(line))!=0):
            init_food_list.append(food_extract(line))
        #else:
        #    if(len(maybe_food(line))!=0):
        #        maybe_list.append(maybe_food(line))

    food_list=[]
    for food in init_food_list:
        food_list.append(cleaner(food))
    foods=[]
    for i in food_list:
        if i[0]!='lb ':
            foods.append(i)
    res = []
    for i in foods:
        i[0] = i[0].strip()
        i[0] = i[0][:-2]
    return foods
            
class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image


def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []
    words_list= []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    #print(document.text)

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
                        words_list.append(word)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    #print(words_list)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds, words_list
    #return words_list

def get_word(word):
    string_word=""
    for symbol in word.symbols:
        string_word+=symbol.text.encode("utf-8")
    return string_word

def render_doc_text(filein):
    image = Image.open(filein)
    bounds, page_list = get_document_bounds(filein, FeatureType.PAGE)
    draw_boxes(image, bounds, 'blue')
    bounds, para_list = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds, words_list = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    #if fileout is not 0:
    #    image.save(fileout)
    #else:
    #    image.show()
    return words_list


def receiptdetect(imgtodetect):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('detect_file', help='The image for text detection.')
    # parser.add_argument('-out_file', help='Optional output file', default=0)
    # args = parser.parse_args()

    words_list = render_doc_text(imgtodetect)
    #words_list = get_document_bounds(args.detect_file, args.out_file)
    # print(words_list)
    # print("--------------------------------------------")
    words_list.sort(key=lambda word:word.bounding_box.vertices[0].y)
    #words_list.sort(key=lambda word:word.bounding_box.vertices[0].x)

    receipt_line = []
    prev_word = words_list[0]
    cur_line = []


    #print(words_list)
    for word in words_list:
        #means it's a new line, stored separately

        #print("Distance: "+str(abs(word.bounding_box.vertices[1].y - prev_word.bounding_box.vertices[0].y)))
        #print(get_word(word))
        if (abs(word.bounding_box.vertices[1].y - prev_word.bounding_box.vertices[0].y) > 47):
            #print(abs(word.bounding_box.vertices[1].y - prev_word.bounding_box.vertices[0].y))
            #print(get_word(word))
            ##sort the current line
            cur_line.sort(key=lambda word:word.bounding_box.vertices[0].x)

            ##append the current line to the receipt
            receipt_line.append(cur_line)

            ##clear out the current line
            cur_line = [word]
            prev_word = word

        else:
            cur_line.append(word)
            #receipt_line[-1][-1].append(word)

    #print(receipt_line)

    words_in_row_list = []
    string_word= ""
    outputlist = []
    #going through each row in the main list
    for i in range (0, len(receipt_line)):
        #going through each word in the main list
        for word in range (0, len(receipt_line[i])):
            #print(receipt_line[i][word])
            for symbol in receipt_line[i][word].symbols:
                string_word += symbol.text
                #row_list.append(symbol.text)
                #print(symbol.text)
            words_in_row_list.append(string_word.encode('utf-8').strip())
            string_word = ""
        final_string = b" ".join((words_in_row_list))
        # final_string = ' '.join(words_in_row_list)
        outputlist.append(final_string)
        words_in_row_list = []

        # print(words_in_row_list[i])


        #print(receipt_line[i][0].symbols)
        #char_list = [line.text for line in [symbol.text for symbol in receipt_line[i].symbols]]
        #print(''.join(list(char_list)).encode('utf-8').strip())



        #print(word.bounding_box.vertices[0].y)

    return outputlist

