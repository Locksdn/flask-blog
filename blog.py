from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    draft = db.Column(db.Boolean, default=True, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def publish(self):
        self.draft = False


@app.route('/entry', methods=['GET'])
def get_all_entries():
    entries = Entry.query.all()

    output = []

    for entry in entries:
        entry_data = {
            'title': entry.title,
            'content': entry.content
        }
        output.append(entry_data)
    
    return jsonify(output)

#   GET ENTRY
@app.route('/entry/<entry_id>', methods=['GET'])
def get_post(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()

    if not entry:
        return jsonify({'message': 'No entry found'})
    
    entry_data = {
        'title': entry.title,
        'content': entry.content
    }
    
    return jsonify(entry_data)


#   CREATE ENTRY
@app.route('/entry', methods=['POST'])
def create_entry():
    data = request.get_json()

    new_entry = Entry(data['title'], data['content'])
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({
        'message': 'Entry created!'
    })

#   EDIT ENTRY
@app.route('/entry/<entry_id>', methods=['PUT'])
def post_entry(entry_id):
    data = request.get_json()

    entry = Entry.query.filter_by(id=entry_id).first()

    if not entry:
        return jsonify({'message': 'Entry not found'})

    entry.title = data['title']
    entry.content = data['content']

    db.session.commit()
    return jsonify({'message': 'Entry edited!'})

#   DELETE ENTRY
@app.route('/entry/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()

    if not entry:
        return jsonify({'message': 'No entry found'})
    
    db.session.delete(entry)
    db.session.commit()

    return jsonify({'message': 'Entry deleted!'})

if __name__ == '__main__':
    app.run(debug=True)