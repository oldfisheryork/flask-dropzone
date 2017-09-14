from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)

from werkzeug import secure_filename
import os
from os.path import isfile, join

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

from logging import Formatter, FileHandler

handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')

handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)

# set the file's extensions that could be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    if endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# get uploaded filenames
def get_files():
    mypath = 'uploads'
    only_files = [ f for f in os.listdir(mypath) if isfile(join(mypath, f)) ]
    return only_files


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.root_path + '/uploads/', filename)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        files = request.files.getlist('file[]')

        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                uploaded_files = get_files()

                # print("filename: %s" % filename)

                # deal with duplicate file names
                # if exists then give a new name
                if filename in uploaded_files:
                    count = 0
                    name, ext = filename.split('.')
                    print('filename already exists')
                    while filename in uploaded_files:
                        count += 1
                        filename = name + '_' + str(count) + '.' + ext

                # log, to print new filename
                print('uploaded file name: %s' % filename)

                updir = os.path.join(basedir, 'uploads/')
                f.save(os.path.join(updir, filename))
                file_size = os.path.getsize(os.path.join(updir, filename))
            else:
                app.logger.info('ext name error')
                print('upload error')
                return jsonify(error='ext name error')
        # log
        print('upload successfully')
        return jsonify(name=filename, size=file_size)

@app.route('/filenameajax', methods=['GET'])
def getfilenames():
    only_files = get_files()
    return jsonify(result=only_files)

if __name__ == '__main__':
    app.run(host="localhost", port=9393)