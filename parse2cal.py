


from os import mkdir, write
from posix import RTLD_NODELETE
import parse_speech as parser
import json,time, uuid
from datetime import datetime, date,timedelta
from dateutil.parser import isoparse
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce
from icalendar import Calendar, Event


def luis_connect(transcript) ->dict:
    # authoringKey = '5160ceef65ce4367ad00a9d0f9053e98'
    # authoringEndpoint = 'https://australiaeast.api.cognitive.microsoft.com/'
    predictionKey = '4a98893a12f44f2e8ba2a545d008724f'
    predictionEndpoint = 'https://australiaeast.api.cognitive.microsoft.com/'

    runtimeCredentials = CognitiveServicesCredentials(predictionKey)
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)

    predictionRequest = { "query" : transcript }

    app_id = "238b987f-a1b4-46f8-aa8a-319abaeeadb4"

    predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
    print("Top intent: {}".format(predictionResponse.prediction.top_intent))
    print("Sentiment: {}".format (predictionResponse.prediction.sentiment))
    print("Intents: ")

    for intent in predictionResponse.prediction.intents:
        print("\t{}".format (json.dumps (intent)))
    print("Entities: {}".format (predictionResponse.prediction.entities))
    return predictionResponse.prediction.entities

def parse_date(entities): 
    if( 'date' in entities):
        entities_date = entities['date'][0]
        # dates = [ '今日','明日','明後日']
        year=''
        month=''
        day=''


        if( entities_date == '今日' ):
            parsed_date = datetime.now()

        elif(entities_date == '明日' ):
            parsed_date = datetime.now() +timedelta(days=1,minutes=0)
        elif(entities_date == '明後日'):
            parsed_date = datetime.now() + timedelta(days=2,minutes=0)
        else:
            parsed_date = datetime.now()


    # todo
    # 漢数字->数字
    # 数字を抽出


    
    # if('time' in entities):
    #     if()

    # else:
    #     #

    return parsed_date


def parse_action(entities):
    action =''

    if( 'name' in entities):
        action = action + entities['name'][0]+'と'
    if( 'action' in entities):
        action = action + entities['action'][0]
    
    return action 
        


def write_ics_file(path,entities)->int:

    
    with open(path,'w') as fp:
        fp.write('BEGIN:VCALENDAR\n')
        fp.write(' VERSION:2.0\n')
        fp.write(' PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n')
        fp.write(' BEGIN:VEVENT\n')
        
        start_date = parse_date(entities)
        print(str(start_date))
        start = '19970714T170000Z'
        end = '19970714T170000Z'

        
        fp.write(f'DTSTART: { start }\n')
        fp.write(f' DTEND:{ end }\n')
        action = parse_action(entities)

        fp.write(f'SUMMERY:{ action }\n')
        fp.write(' END:VEVENT\n')
        fp.write('END:VCALENDAR\n')

    fp.close()

    return 1
    


def parse2cal(file_name)->str:

    # transcript = parser.parse_speech(file_name)
    transcript ='明後日３時にしゅんしゅんと水族館にいきます'
    entities = luis_connect(transcript)
    
    path = './temp.ics'
    bin = write_ics_file(path,entities)

    if ( bin < 0 ):
        print('failed to write ics file')
        return None
    
    






    

if __name__ == "__main__":
    parse2cal("mei.m4a")