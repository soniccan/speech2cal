
#Todo 出てきた文章を解析して
#・予定の内容
#・時間(s)
#・繰返しがあるのかないのか
#　をとりだす。
#method　mecab?機械学習？

from os import write
from posix import RTLD_NODELETE
import parse_speech as parser
import json,time, uuid

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

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

def parse_date(date,time): 
    if(date == None or time == None):
        print('Not found  entitiy of date or time')
        return
    dates = { '今日','明日','明後日'}

    

def write_ics_file(path,entities)->int:

    fp = open(path,'w')

    fp.write('BEGIN:VCALENDAR')
    fp.write(' VERSION:2.0')
    fp.write(' PRODID:-//hacksw/handcal//NONSGML v1.0//EN')
    fp.write(' BEGIN:VEVENT')
    
    start_date = parse_date(entities['date'],entities['time'])
    start = '19970714T170000Z'
    end = '19970714T170000Z'


    fp.write(f'DTSTART: { start }')
    fp.write(f' DTEND:{ end }')

    action =entities['action']
    fp.write(f'SUMMERY:{ action }')
    fp.write(' END:VEVENT')
    fp.write('END:VCALENDAR')

    fp.close()

    return 1
    


def parse2cal(file_name)->str:

    # transcript = parser.parse_speech(filename')
    transcript ='今日3時にゲームセンター'
    entities = luis_connect(transcript)
    
    path = './temp.ics'
    bin = write_ics_file(path,entities)

    if ( bin < 0 ):
        print('failed to write ics file')
        return None
    
    






    

if __name__ == "__main__":
    parse2cal("temp.mp3")