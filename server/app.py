#!/usr/bin/env python
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False



CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["POST", "GET"])
def messages():
    if request.method == 'POST':
            m = Message(body=request.get_json()['body'], username=request.get_json()['username'])
            db.session.add(m)
            db.session.commit()
            return make_response(jsonify(m.to_dict()), 202)
    else:
        jso = []
        all = Message.query.order_by(Message.created_at).all()
        for el in all:
            jso.append(el.to_dict())
        return make_response(jsonify(jso), 202)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'DELETE':
        m = Message.query.filter(Message.id == id).first()
        db.session.delete(m)
        db.session.commit()
        return make_response('OK', 200)
    else:
        m = Message.query.filter(Message.id == id).first()
        m.body = request.get_json()['body']
        db.session.commit()
        return make_response(jsonify(m.to_dict()), 200)
if __name__ == '__main__':
    app.run(port=4000, debug=True)
