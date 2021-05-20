import os 
import glob
input_path = "/home/pi/Desktop/picture/"
files        = glob.glob(os.path.join(input_path,'*'))
stored_names =  list(map(lambda x: x.split("\")[1], files))

for file,name in zip(files,stored_names):
    s3.upload_file(file,"BUCKET_NAME_YOU_WANT",name)

