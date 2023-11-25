from flask import (
    Flask,
    render_template
)
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(1024), nullable=False)

    def __init__(self, url_image):
        self.image_url = url_image


@app.route("/")
def hello_world():
    images=Image.query.all()
    image = random.choice(images)
    return render_template('index.html', url=image.image_url)
