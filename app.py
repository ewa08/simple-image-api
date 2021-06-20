import uuid
from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename

# UID = uuid.uuid1()
# print(UID)

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/images/<image_id>')
def get_image(image_id):
    file_path = f"images/{image_id}.png"
    return send_file(file_path, mimetype='image/png')


@app.route('/images', methods=['GET', 'POST'])
def upload_image():
    uid = uuid.uuid1()
    if 'image' in request.files:
        image = request.files['image']
        filename = secure_filename(f'{str(uid)}.png')
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return str(uid)


if __name__ == "__main__":
    app.run(debug=True)
