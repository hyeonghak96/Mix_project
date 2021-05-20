import boto3
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name):
    print("Creating a bucket... " + bucket_name)

    s3 = boto3.client(
        's3',  # 사용할 서비스 이름, ec2이면 'ec2', s3이면 's3', dynamodb이면 'dynamodb'
        aws_access_key_id="YOUR_ID",         # 액세스 ID
        aws_secret_access_key="YOUR_KEY")    # 비밀 엑세스 키

    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-northeast-2' # Seoul  # us-east-1을 제외한 지역은 LocationConstraint 명시해야함.
            }
        )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Bucket already exists. skipping..")
        else:
            print("Unknown error, exit..")


response = create_s3_bucket(bucket_name="BUCKET_NAME_YOU_WANT")
print("Bucket : " + str(response))