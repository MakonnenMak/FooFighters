# Basic Text Parser for Kroger Receipt
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn


def food_extract(line):
    foods=[]
    line=line.split(' ')
    if ('B\n' in line) or ('T\n' in line) or ('1b\n' in line) or ('lb\n' in line):
        foods.append(line)

    return foods

def maybe_food(line):
    food = wn.synset('food.n.02')
    nltk_fod_list=list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

    line=line.split(' ')
    maybe_foods=[]
    for i in range (0,len(line)):
        if line[i].lower() in nltk_fod_list:
            if len(line[i])>2:
                if '\n' not in line[i]:
                    maybe_foods.append(line)
    return maybe_foods


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
#def maybe_cleaner(line):
#
#
with open('results2.txt') as f:
    lines=f.readlines()
    
    init_food_list=[]
    maybe_list=[]
    for line in lines:
        if(len(food_extract(line))!=0):
            init_food_list.append(food_extract(line))

        else:
            if(len(maybe_food(line))!=0):
                maybe_list.append(maybe_food(line))

    food_list=[]
    for food in init_food_list:
        food_list.append(cleaner(food))
    foods=[]
    for i in food_list:
        if i[0]!='lb ':
            foods.append(i)


    print(foods) 
            

