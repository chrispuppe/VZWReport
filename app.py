import os
import os.path
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__, static_url_path='')

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Run application on uploaded data file
        os.system('python Verizon_Charges.py ./uploads/' + filename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return send_from_directory(directory='', filename='current_report.rtf')
        return render_template('vzw-report-download.html')


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/report1/')
def return_files_tut1():
	try:
		return send_file('current_report.rtf',
                    download_name='current_report.rtf', 
                    as_attachment=True)
	except Exception as e:
		return str(e)

@app.route('/report2/')
def return_files_tut2():
	try:
		return send_file('data_list.csv',
                    download_name='data_list.csv', 
                    as_attachment=True)
	except Exception as e:
		return str(e)

@app.route('/report3/')
def return_files_tut3():
	try:
		return send_file('charge_list.csv',
                    download_name='charge_list.csv', 
                    as_attachment=True)
	except Exception as e:
		return str(e)

@app.route('/report4/')
def return_files_tut4():
	try:
		return send_file('equip_charge_list.csv',
                    download_name='equip_charge_list.csv', 
                    as_attachment=True)
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5000")#,
        #debug=True
    )

