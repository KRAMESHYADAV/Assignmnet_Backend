from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_price = db.Column(db.Integer, nullable=False)
    dollars_off = db.Column(db.Integer, nullable=False)
    net_price = db.Column(db.Integer, nullable=False)
    percent_off = db.Column(db.Integer, nullable=True)
    harmony_cost = db.Column(db.Integer, nullable=False)
    cost_concessions = db.Column(db.Integer, nullable=True)
    special_cost = db.Column(db.Integer, nullable=True)
    net_cost = db.Column(db.Integer, nullable=True)
    comments = db.Column(db.String(250), nullable=True)


class PriceSchema(ma.ModelSchema):
    class Meta:
        model = Price


def get_price_model():
    try:
        price_data = Price.query.all()
        price_schema = PriceSchema(many=True).dump(price_data)
        return price_schema
    except Exception:
        return dict(Unsuccessful="Sever is not responding")


def save_price_model(add_price):
    try:
        create_price = Price(**add_price)
        db.session.add(create_price)
        db.session.commit()
        db.session.close()
        return dict(Successful="Data Added Successfully")
    except:
        return dict(Unsuccessful="Sever is not responding")


@app.route("/", methods=['GET'])
def showprice():
    return jsonify(get_price_model())

@app.route("/addprice", methods=['POST'])
def add_price():
    if request.method == 'POST':
        add_data = request.get_json(force=True)
        print(add_data)
        try:
            return jsonify(save_price_model(add_data))
        except Exception:
            return jsonify({'Unsuccessful': 'Looks like you missed something'})


#


if __name__ == '__main__':
    app.run(debug=True)
