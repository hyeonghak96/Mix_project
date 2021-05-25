import boto3
import os 
import glob

input_path = "/home/pi/Desktop/picture/"
files        = glob.glob(os.path.join(input_path,'*'))
stored_names =  list(map(lambda x: x.split("/")[5], files))
my_bucket = "hyeonghakbucket"
s3 = boto3.client(
    's3',  # 사용할 서비스 이름, ec2이면 'ec2', s3이면 's3', dynamodb이면 'dynamodb'
    aws_access_key_id="AKIA27VRBCJZH7CEXQZM",         # 액세스 ID
    aws_secret_access_key="62DOftgv9nJfGE0R93dnT5Yk6NRHAu+f0cw21wqA")    # 비밀 엑세스 키

def file_upload():        
    for file,name in zip(files,stored_names):
        print(file,name)
        s3.upload_file(file,my_bucket,name)
    
    