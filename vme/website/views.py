from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 
        date = request.form.get('date')
        time = request.form.get('time')
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, date=date, time=time, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database  
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("home.html", user=current_user)






@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/board')
@login_required
def board():
    return render_template("board.html", user=current_user)

@views.route('/list')
@login_required
def list():
    return render_template("list.html", user=current_user)