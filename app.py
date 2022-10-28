import os

from flask import Flask, render_template, redirect, url_for
import requests

from forms import CafeForm


SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
api_key = "TopSecretAPIKey"
API_BASE_URL = "http://127.0.0.1:8000"


@app.route("/")
def home():
    form = CafeForm()
    r = requests.get(f"{API_BASE_URL}/all")
    cafes = r.json()
    table_headers = ["Name", "Location", "Coffee Price", "Seats"]
    return render_template("home.html",
                           cafes=cafes,
                           table_headers=table_headers,
                           form=form)


@app.route("/add", methods=["POST"])
def add_cafe():
    form = CafeForm()
    if form.validate():
        requests.post(f"{API_BASE_URL}/add", data=form.data)
    return redirect(url_for("home"))


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    params = {
        "api-key": api_key
    }
    requests.delete(f"{API_BASE_URL}/report-closed/{cafe_id}", params=params)
    return redirect(url_for("home"))


@app.route("/cafe/<int:cafe_id>")
def get_cafe(cafe_id):
    params = {
        "api-key": api_key
    }
    r = requests.get(f"{API_BASE_URL}/cafe/{cafe_id}", params=params)
    cafe = r.json()
    return render_template("cafe.html", cafe=cafe)


if __name__ == '__main__':
    app.run(debug=True)