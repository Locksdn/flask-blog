from flask import jsonify, request
from .app import db, app
from .models import Entry

#   GET EVERY ENTRY
@app.route('/api/entry', methods=['GET'])
def get_all_entries():
    entries = Entry.query.all()

    output = []
    for entry in entries:
        output.append(entry.getJson())
    
    return jsonify(output)

#   GET ENTRY BY ID
@app.route('/api/entry/<entry_id>', methods=['GET'])
def get_post(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()

    if not entry:
        return jsonify({'message': 'No entry found'})
    return jsonify(entry.getJson())


#   CREATE ENTRY
@app.route('/api/entry', methods=['POST'])
def create_entry():
    data = request.get_json()

    new_entry = Entry(data['title'], data['content'])
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({
        'message': 'Entry created!',
        'entry': new_entry.getJson()
    })

#   EDIT ENTRY
@app.route('/api/entry/<entry_id>', methods=['PUT'])
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
@app.route('/api/entry/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()

    if not entry:
        return jsonify({'message': 'No entry found'})
    
    db.session.delete(entry)
    db.session.commit()

    return jsonify({'message': 'Entry deleted!'})