from flask_wtf import FlaskForm
from wtforms import StringField, FormField
from wtforms.validators import length, InputRequired, ValidationError

class ImageAddForm(FlaskForm):
    image_url = StringField("Image URL",
                            validators=[InputRequired(), length(min=10, max=1000, message='URL lenght in 10-1000) ')])
