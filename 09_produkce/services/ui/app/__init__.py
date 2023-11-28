from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request, send_from_directory
)

import random
import json
import urllib.request
from .form import ImageAddForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object("app.config.Config")
csrf = CSRFProtect(app)


@app.route("/")
def index():
    content = urllib.request.urlopen('http://images:5000/api/images').read().decode('utf-8')
    try:
        images = json.loads(content)
    except ValueError as e:
        return render_template("errors/500.jinja"), 500

    image = random.choice(images)
    return render_template('index.html', url=image['image_url'])


@app.route("/admin")
def admin():
    imageadd_form = ImageAddForm()

    content = urllib.request.urlopen('http://images:5000/api/images').read().decode('utf-8')
    try:
        images = json.loads(content)
    except ValueError as e:
        return render_template("errors/500.jinja"), 500

    return render_template('admin.html', form=imageadd_form, images=images)


@app.route("/admin/add_image", methods=["POST"])
def add_image():
    imageadd_form = ImageAddForm(request.form)

    if imageadd_form.validate():
        url = 'http://images:5000/api/images'
        data = {"image_url": imageadd_form.image_url.data}

        data = json.dumps(data)
        req = urllib.request.Request(url=url,
                                     data=bytes(data.encode("utf-8")), method="POST")
        req.add_header("Content-type", "application/json; charset=UTF-8")

        with urllib.request.urlopen(req) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
            print(response_data)

        return redirect(url_for("admin"))
    else:
        for _, errors in imageadd_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if len(error) > 0:
                        for k in error.keys():
                            flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")

        return redirect(url_for("admin"))


@app.route("/admin/delete/<image_id>", methods=["GET"])
def delete_image(image_id):
    url = f"http://images:5000/api/images/{image_id}"

    req = urllib.request.Request(url=url, method="DELETE")
    req.add_header("Content-type", "application/json; charset=UTF-8")

    with urllib.request.urlopen(req) as resp:
        response_data = json.loads(resp.read().decode("utf-8"))
        print(response_data)
    return redirect(url_for("admin"))


@app.route("/admin/edit/<image_id>", methods=["GET"])
def view_image(image_id):
    content = urllib.request.urlopen('http://images:5000/api/images/' + image_id).read().decode('utf-8')
    try:
        image = json.loads(content)
        imageadd_form = ImageAddForm()
        imageadd_form.image_url.data=image['image_url']
        return render_template('edit.html', form=imageadd_form, image=image)

    except ValueError as e:
        return render_template("errors/500.jinja"), 500


@app.route("/admin/edit/<image_id>", methods=["POST"])
def edit_image(image_id):
    print ("test")
    imageadd_form = ImageAddForm(request.form)

    if imageadd_form.validate():
        print (imageadd_form.image_url.data)
        url = f"http://images:5000/api/images/{image_id}"
        data = {"id": image_id, "image_url": imageadd_form.image_url.data}
        data = json.dumps(data)
        req = urllib.request.Request(url=url,
                                     data=bytes(data.encode("utf-8")), method="PUT")
        req.add_header("Content-type", "application/json; charset=UTF-8")

        with urllib.request.urlopen(req) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
            print(response_data)

        return redirect(url_for("admin"))

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.jinja"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.jinja"), 404
