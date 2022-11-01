from flask import Flask, render_template, request
import boto
import boto.s3.connection
import boto3
app = Flask(__name__)

from werkzeug.utils import secure_filename
#import key_config as keys

access_key = 'AKIA2BUHV4R2RS54PBTY'
secret_key = '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'
conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key)

client = boto3.client('s3', aws_access_key_id = access_key,
                    aws_secret_access_key = secret_key)

BUCKET_NAME= "mattdtest"

@app.route('/')  
def home():
    return render_template("html2AWS.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                client.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "

    return render_template("html2AWS.html",msg =msg)

    

if __name__ == "__main__":
    
    app.run(debug=True)