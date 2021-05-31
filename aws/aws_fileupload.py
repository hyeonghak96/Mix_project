import boto3
import os 
import glob

class Settings:
    def __init__(self):
        self.input_path = "/home/pi/Desktop/picture/"
        self.files = glob.glob(os.path.join(self.input_path,'*'))
        self.stored_names = list(map(lambda x: x.split("/")[5], files))
        self.my_bucket = "hyeonghakbucket"
        self.s3 = boto3.client(
            's3',  # 사용할 서비스 이름, ec2이면 'ec2', s3이면 's3', dynamodb이면 'dynamodb'
            aws_access_key_id="AKIA27VRBCJZH7CEXQZM", # 액세스 ID
            aws_secret_access_key="62DOftgv9nJfGE0R93dnT5Yk6NRHAu+f0cw21wqA") # 비밀 엑세스 키

def file_upload():
    settings = Settings()
    for file,name in zip(settings.files, settings.stored_names):
        print(settings.file, name)
        settings.s3.upload_file(file, settings.my_bucket, name)

