import os
import uuid

from flask import Flask, request, send_file, render_template
from peewee import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

psql_db = PostgresqlDatabase('images-db', user='postgres', password='password', host='localhost', port=5432)


class Image(Model):
    name = CharField()

    class Meta:
        database = psql_db


@app.route('/images/<image_id>')
def get_image(image_id):
    data = Image.get(Image.id == image_id)
    file_path = f"images/{data.name}"
    return send_file(file_path, mimetype='image/png')


@app.route('/images', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        images = Image.select()
        return render_template('images.html', image_list=images)
    if request.method == 'POST':
        if 'image' in request.files:
            uid = uuid.uuid1()
            image = request.files['image']
            filename = secure_filename(f'{str(uid)}.png')
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return str(Image.create(name=f'{str(uid)}.png').get_id())


if __name__ == "__main__":
    with psql_db:
        psql_db.create_tables([Image])
    app.run(debug=True)
