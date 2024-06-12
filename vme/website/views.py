from flask import Blueprint, render_template, request, flash, jsonify, redirect, send_from_directory,current_app
from flask_login import login_required, current_user
from .models import Note, File
from . import db
import json
import os


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

@views.route('/')
def index():
    files = File.query.all()
    return render_template('home.html',files=files)



@views.route('/uploads',methods=['POST'])
def uploads():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            # os.mkdir(current_app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            new_file = File(filename = filename)
            db.session.add(new_file)
            db.session.commit()
            return redirect('/board')
    return 'Error. Try again.'

@views.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@views.route('/download/<int:file_id>')
def download(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

@views.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for f in request.files.getlist('photo'):
            filename = uuid.uuid4().hex
            photos.save(f, name=filename + '.')
        success = True
    else:
        success = False
    return render_template('board.html', form=form, success=success)

@views.route('/manage')
def manage_file():
    files_list = os.listdir(current_app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('manage.html', files_list=files_list)

@views.route('/delete/<int:file_id>')
def delete(file_id):
    file = File.query.get_or_404(file_id)
    filename = file.filename
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
    os.remove(file_path)

    db.session.delete(file)
    db.session.commit()

    return redirect('/')



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


@views.route('/list')
@login_required
def list():
    return render_template("list.html", user=current_user)

@views.route('/board')
@login_required
def board():
    return render_template("board.html", user=current_user)

