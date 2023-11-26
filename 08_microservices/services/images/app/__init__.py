from flask import (
    Flask,
    jsonify,
    request
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(1024), nullable=False)

    def __init__(self, image_url):
        self.image_url = image_url


@app.route("/api/images")
def get_images():
    try:
        images = Image.query.all()
        if images:
            result = []
            for image in images:
                result.append({"id": image.id, "image_url": image.image_url})
            return jsonify(result)
        else:
            return jsonify({"error": f"Images not found."}), 404
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return jsonify({"error": "An error occurred while getting all images."}), 500


@app.route('/api/images/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image = Image.query.get(image_id)
        if image:
            result = {"id": image.id, "image_url": image.image_url}
            return jsonify(result)
        else:
            return jsonify({"error": f"Image not found."}), 404
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return jsonify({"error": "An error occurred while getting image."}), 500


@app.route('/api/images', methods=['POST'])
def create_image():
    """ {"image_url": "https://apod.nasa.gov/apod/image/2003/BhShredder_NASA_1080.jpg"}
    """
    data = request.get_json()
    try:
        image_url = data["image_url"]
        new_image = Image(image_url=image_url)
        db.session.add(new_image)
        db.session.commit()
        return jsonify({"id": new_image.id, "image_url": new_image.image_url, "message": f"Image created."}), 201
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return {"error": "An error occurred while creating the image."}, 500


@app.route('/api/images/<image_id>', methods=['PUT'])
def update_image(image_id):
    """ {"id":"6", "image_url": "https://apod.nasa.gov/apod/image/1707/carina08_hubble_960.jpg"}
    """
    data = request.get_json()
    try:
        image_url = data["image_url"]

        image = Image.query.get(image_id)
        image.image_url = image_url
        db.session.commit()
        return jsonify({"id": image_id, "image_url": image_url, "message": f"Image updated."}), 201
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return {"error": "An error occurred while updating the image."}, 500


@app.route('/api/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        Image.query.filter_by(id=image_id).delete()
        db.session.commit()
        return jsonify({"id": image_id, "message": f"Image deleted."}), 201
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return jsonify({"error": "An error occurred while deleting image."}), 500
