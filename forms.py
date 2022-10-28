from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, URLField
from wtforms.validators import DataRequired, URL


class CafeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price £', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired(), URL(require_tld=False)])
    img_url = URLField('Image URL', validators=[DataRequired(), URL(require_tld=False)])
    has_toilet = BooleanField("Toilet", false_values=(False, 'false', 0, '0'))
    has_wifi = BooleanField("WiFi")
    has_sockets = BooleanField("Sockets")
    can_take_calls = BooleanField("Calls")
