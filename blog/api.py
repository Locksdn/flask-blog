from flask import jsonify, request, current_app
from flask_login import current_user
from flask.views import MethodView
from .app import db, app
from .models import Entry

class EntryAPI(MethodView):
    def get(self, entry_id):
        if entry_id is None:
            entries = Entry.query.all()
            output = [entry.to_dic() for entry in entries]
            
            return jsonify(output)

        else:
            entry = Entry.query.filter_by(id=entry_id).first()
            if not entry:
                return jsonify({'message': 'No entry found'})
            return jsonify(entry.to_dic())

    def post(self):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        data = request.get_json()

        new_entry = Entry(data['title'], data['content'])
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            'message': 'Entry created!',
            'entry': new_entry.to_dic()
        })

    def put(self, entry_id):

        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        data = request.get_json()

        entry = Entry.query.filter_by(id=entry_id).first()

        if not entry:
            return jsonify({'message': 'Entry not found'})

        entry.title = data['title']
        entry.content = data['content']

        db.session.commit()
        return jsonify({'message': 'Entry edited!'})

    def delete(self, entry_id):

        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        entry = Entry.query.filter_by(id=entry_id).first()

        if not entry:
            return jsonify({'message': 'No entry found'})
        
        db.session.delete(entry)
        db.session.commit()

        return jsonify({'message': 'Entry deleted!'})


entry_api = EntryAPI.as_view('entry_api')

app.add_url_rule('/api/entry', defaults={'user_id': None}, view_func=entry_api, methods=['GET'])
app.add_url_rule('/api/entry', view_func=entry_api, methods=['POST'])
app.add_url_rule('/api/entry/<int:entry_id>', view_func=entry_api, methods=['GET', 'PUT', 'DELETE'])