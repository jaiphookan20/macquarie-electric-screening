# app/routes.py

import os
from flask import render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from . import db
from .utils import validate_excel_file

@current_app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads and validation."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload an Excel (.xlsx or .xls) file.', 'error')
                return redirect(url_for('upload_file'))
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.instance_path, filename)
            file.save(filepath)

            # Validate the uploaded file
            is_valid, message = validate_excel_file(filepath)
            if is_valid:
                flash('File successfully uploaded and validated.', 'success')
                # Here you would trigger the processing
            else:
                flash(f'Invalid file: {message}', 'error')
            
            return redirect(url_for('upload_file'))

    return render_template('index.html')

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    allowed_extensions = {'xlsx', 'xls'}  # Allow both .xlsx and .xls
    return extension in allowed_extensions
