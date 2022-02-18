import random
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bistros.db'
app.config['api_key'] = 'TopSecretAPIKey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Bistro(db.Model):
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
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.before_first_request
def create_tables():
    db.create_all()

#@app.route("/")
#def home():
#    return render_template("index.html")
@app.route("/")
def home():
    all_bistros = Bistro.query.order_by(Bistro.id).all()
    for i in range(len(all_bistros)):
        all_bistros[i].ranking = len(all_bistros) - i
    db.session.commit()

    counter = 0
    bistros_to_append = []
    all_bistros_three_list = []
    # create lists of three bistros inside a big list:
    for _ in all_bistros:
        bistros_to_append.append(all_bistros[counter])
        counter += 1
        if len(bistros_to_append) % 3 != 0:
            continue
        else:
            all_bistros_three_list.append(bistros_to_append)
            bistros_to_append = []
    # if there are leftovers in cafes_to_append, add them to the list as well:
    if len(bistros_to_append) > 0:
        all_bistros_three_list.append(bistros_to_append)
    return render_template("index.html", all_bistros=all_bistros_three_list)

@app.route("/random")
def get_random_bistro():
    bistros = db.session.query(Bistro).all()
    random_bistro = random.choice(bistros)
    return jsonify(bistro={
        "id": random_bistro.id,
        "name": random_bistro.name,
        "map_url": random_bistro.map_url,
        "img_url": random_bistro.img_url,
        "location": random_bistro.location,
        "seats": random_bistro.seats,
        "has_toilet": random_bistro.has_toilet,
        "has_wifi": random_bistro.has_wifi,
        "has_sockets": random_bistro.has_sockets,
        "can_take_calls": random_bistro.can_take_calls,
        "coffee_price": random_bistro.coffee_price,
    })

@app.route("/cafes")
def cafes():
    return render_template("add_cafes.html")

## HTTP GET - Get All Records
@app.route("/all")
def get_all_bistros():
    bistros = db.session.query(Bistro).all()
# This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(bistros=[bistro.to_dict() for bistro in bistros])

# Always nice to use 15 lines for something that could be done in 4:
def get_all_bistros():
    bistros = db.session.query(Bistro).all()
    bistro_list = []
    for bistro in bistros:
        bistro_dict = {"id": bistro.id, "name": bistro.name, "map_url": bistro.map_url, "img_url": bistro.img_url,
                       "location": bistro.location, "has_sockets": bistro.has_sockets,"has_toilet": bistro.has_toilet,
                       "has_wifi": bistro.has_wifi, "can_take_calls": bistro.can_take_calls, "seats": bistro.seats,
                       "coffee_price": bistro.coffee_price}
        bistro_list.append(bistro_dict)
    all_bistros = {"bistros": bistro_list}
    all_bistros_json = jsonify(bistros=all_bistros["bistros"])
    return all_bistros_json

## HTTP ADD - Post a new Record
@app.route("/add", methods=["GET", "POST"])
def post_new_bistro():
    new_bistro = Bistro(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_bistro)
    db.session.commit()
    return redirect(url_for("home"))


## HTTP DELETE - Delete Record
@app.route("/delete", methods=["DELETE", "GET"])
def delete():
    bistro_id = request.args.get("id")
    bistro = Bistro.query.get(bistro_id)
    db.session.delete(bistro)
    db.session.commit()
    return redirect("/#coffee-shops")


if __name__ == '__main__':
    app.run(debug=True)
