import os
import uuid
import argparse
import logging
import re
import time
import json

import boto3
from botocore.exceptions import ClientError




# def upload_file(bucket_name,local_path, local_file_name):
#     root_ext_pair = os.path.splitext(local_file_name)
#     object_name = root_ext_pair[0] + str(uuid.uuid4()) + root_ext_pair[1] # S3バケット内で唯一のオブジェクト名になるようにランダム文字列（UUID）を挿入しておく
#     upload_file_path = os.path.join(local_path, local_file_name)

#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(upload_file_path, bucket_name, object_name)
#     except ClientError as e:
#         print(e)
#         return None
    
#     print("\nUploading " + local_file_name +" to S3 as object:\n\t" + object_name)
#     return object_name 

# def start_transcription_job(bucket_name, object_name, language_code):
#     job_name = re.sub(r'[^a-zA-Z0-9._-]', '', object_name)[:199] # Transcribeのフォーマット制約に合わせる（最大200文字。利用可能文字は英大文字小文字、数字、ピリオド、アンダーバー、ハイフン）
#     media_file_url = 's3://' + bucket_name + '/' + object_name

#     client = boto3.client('transcribe')
#     response = client.start_transcription_job(
#         TranscriptionJobName=job_name,
#         LanguageCode=language_code,
#         Media={
#         'MediaFileUri': media_file_url
#         },
#         OutputBucketName=bucket_name
#     )

#     print("\nTranscription start")
#     return job_name

def get_transcription_file_url(job_name):
    client = boto3.client("transcribe")
    response = client.get_transcription_job(
        TranscriptionJobName=job_name
    )
    file_url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

    print("\nFile URL:\n\t" + file_url)
    return file_url

def get_transcription_status(job_name):
    client = boto3.client("transcribe")
    response = client.get_transcription_job(
        TranscriptionJobName=job_name
    )
    status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    print("Transcription status:\t" + status)
    return status


def get_transcription_file_url(job_name):
    client = boto3.client("transcribe")
    response = client.get_transcription_job(
        TranscriptionJobName=job_name
    )
    print("result")
    file_url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

    print("\nFile URL:\n\t" + file_url)
    return file_url

def download_file(bucket_name, object_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, object_name, object_name)
    print("\nDownloading S3 object:\n\t" + object_name)

def get_transcript_from_file(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        df = json.load(f)

    transcript = ""
    for result in df["results"]["transcripts"]:
            transcript += result["transcript"] + "\n"
    
    print("\nTranscription result:\n" + transcript)
    return transcript

def delete_json_file(file_name):

    os.remove(file_name)

def parse_speech(file_name:str)->str:
    bucket_name = "transcribe-test-baba"
    locale ="ja-JP"

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-f", "--file", type=argparse.FileType("r", encoding="UTF-8"), required=True)
    # parser.add_argument("-l", "--locale", help="e.g. \"en-US\" or \"ja-JP\"", required=True)
    # args = parser.parse_args()


    # STEP1: ローカルにある音声ファイルをS3にアップロード
    base_dir_pair = os.path.split(file_name)
    local_path = base_dir_pair[0]
    local_file_name = base_dir_pair[1]

    object_name = upload_file(bucket_name,local_path, local_file_name)

    job_name = start_transcription_job(bucket_name, object_name, locale)

    status = ""
    while status not in ["COMPLETED", "FAILED"]: # 処理が完了したら状態が"COMPLETED"、失敗したら"FAILED"になるからそれまでループ
        status = get_transcription_status(job_name) # 処理状態を取得
        time.sleep(3)

    file_url = get_transcription_file_url(job_name)

    result_object_name = file_url[file_url.find(bucket_name) + len(bucket_name) + 1:]
    download_file(bucket_name, result_object_name)
    transcipt= get_transcript_from_file(result_object_name)

    delete_json_file(result_object_name)
    return transcipt

class jobAws():



    def __init__(self,bucket_name,locale) -> None:
        self._bucket_name = bucket_name
        self._locale = locale


    def upload_file(self,local_path, local_file_name):

        # base_dir_pair = os.path.split(file_name)
        # local_path = base_dir_pair[0]
        # local_file_name = base_dir_pair[1]

        root_ext_pair = os.path.splitext(local_file_name)


        self.object_name = root_ext_pair[0] + str(uuid.uuid4()) + root_ext_pair[1] # S3バケット内で唯一のオブジェクト名になるようにランダム文字列（UUID）を挿入しておく
        upload_file_path = os.path.join(local_path, local_file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        print(upload_file_path)

        try:
            response = s3_client.upload_file(upload_file_path, self._bucket_name, self.object_name)
        except ClientError as e:
            print(e)
            return None
        
        print("\nUploading " + local_file_name +" to S3 as object:\n\t" + self.object_name)


    def start_transcription_job(self):
        job_name = re.sub(r'[^a-zA-Z0-9._-]', '', self.object_name)[:199] # Transcribeのフォーマット制約に合わせる（最大200文字。利用可能文字は英大文字小文字、数字、ピリオド、アンダーバー、ハイフン）
        media_file_url = 's3://' + self._bucket_name + '/' + self.object_name

        client = boto3.client('transcribe')

        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode = self._locale,
            Media={
            'MediaFileUri': media_file_url
            },
            OutputBucketName = self._bucket_name
        )

        print("\nTranscription start")
        return job_name







if __name__ == "__main__":
    bucket_name = "transcribe-test-baba"
    locale ="ja-JP"
    

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=argparse.FileType("r", encoding="UTF-8"), required=True)
    parser.add_argument("-l", "--locale", help="e.g. \"en-US\" or \"ja-JP\"", required=True)
    args = parser.parse_args()
    file_name = args.file.name
    locale = args.locale

    # STEP1: ローカルにある音声ファイルをS3にアップロード
    base_dir_pair = os.path.split(file_name)
    local_path = base_dir_pair[0]
    local_file_name = base_dir_pair[1]
    
    job_aws = jobAws(bucket_name,locale)

    job_aws.upload_file(local_path, local_file_name)
    job_name = job_aws.start_transcription_job()


    status = ""
    while status not in ["COMPLETED", "FAILED"]: # 処理が完了したら状態が"COMPLETED"、失敗したら"FAILED"になるからそれまでループ
        status = get_transcription_status(job_name) # 処理状態を取得
        time.sleep(3)

    file_url = get_transcription_file_url(job_name)

    result_object_name = file_url[file_url.find(bucket_name) + len(bucket_name) + 1:]
    download_file(bucket_name, result_object_name) # ここでダウンロード
    get_transcript_from_file(result_object_name)

    delete_json_file(result_object_name)