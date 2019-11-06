import io
import os

from flask import Flask, render_template, send_file, request, redirect, url_for
from PIL import Image

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return redirect(url_for('go_to_image', file_name=f.filename))


@app.route('/go_to_image', methods=['GET'])
def go_to_image():
    file_object = io.BytesIO()
    img = Image.open(os.path.join(app.config['UPLOADED_PATH'], request.args.get('file_name')))
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


if __name__ == '__main__':
    app.run(debug=True)

