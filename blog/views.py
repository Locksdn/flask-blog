from flask import render_template
from .models import Entry
from .app import app

@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/entry/<entry_id>')
def entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()
    return render_template('entry.html', entry=entry)