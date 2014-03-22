import os
import json
import uuid
import subprocess
import beanstalkc
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename, SharedDataMiddleware

DOWNLOAD_FOLDER = 'downloads/'
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['mp3', 'mp4', 'wav', 'ogg', 'flac', 'gif', 'try', 'to', 'break', 'char', 'limit'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

q = beanstalkc.Connection(host='localhost', port=14711)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def generate_unique_filename(filename):
    return '%s_%d_finished.wav' % (filename, uuid.uuid4())


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        uniq_filename = generate_unique_filename(file_path)
        werk = {
            "window": float(request.values['window']),
            "stretch": float(request.values["stretch"]),
            "filename": file_path,
            "uniq_filename": uniq_filename,
        }
        q.put(json.dumps(werk))
        return uniq_filename


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run()
