from flask import jsonify, request, current_app
from flask_login import current_user
from flask.views import MethodView
from .app import db, app
from .models import Entry

class EntryAPI(MethodView):
    def get(self, entry_id, draft=False):
        if entry_id is None:
            if draft is True:
                if not current_user.is_authenticated:
                    return current_app.login_manager.unauthorized()
                entries = Entry.query.all()
            else:
                entries = Entry.query.filter_by(draft=False)
            
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

        title = request.form.get('title')
        content = request.form.get('content')

        new_entry = Entry(title, content)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            'message': 'Entry created!',
            'entry': new_entry.to_dic()
        })

    def put(self, entry_id):

        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        entry = Entry.query.filter_by(id=entry_id).first()

        if not entry:
            return jsonify({'message': 'Entry not found'})

        entry.title = request.form.get('title')
        entry.content = request.form.get('content')

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