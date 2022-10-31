import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# https://documenter.getpostman.com/view/13261708/UVeFPSk4


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    cafes = Cafe.query.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/cafe/<int:cafe_id>")
def get_cafe_by_id(cafe_id):
    cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe with this ID."})


def str_to_bool(user_input):
    if user_input in ["True", "true", "1"]:
        return True
    return False


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    try:
        new_cafe = Cafe(
            name=request.form["name"],
            map_url=request.form["map_url"],
            img_url=request.form["img_url"],
            location=request.form["location"],
            seats=request.form["seats"],
            has_toilet=str_to_bool(request.form["has_toilet"]),
            has_wifi=str_to_bool(request.form["has_wifi"]),
            has_sockets=str_to_bool(request.form["has_sockets"]),
            can_take_calls=str_to_bool(request.form["can_take_calls"]),
            coffee_price=str_to_bool(request.form["coffee_price"])
        )
        db.session.add(new_cafe)
        db.session.commit()
    except KeyError:
        return jsonify(error={"error": "Wrong request"})
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        if new_price:
            cafe.coffee_price = new_price
            db.session.commit()
            return jsonify(success={"success": "Successfully updated the price"}), 200
        return jsonify(error={"error": "Missing new price parameter"}), 400
    return jsonify(error={"error": "No cafe with this id was found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        if api_key and api_key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success={"success": "Successfully deleted the cafe from the database"}), 200
        return jsonify(error={"error": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    return jsonify(error={"error": "No cafe with this id was found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8000)