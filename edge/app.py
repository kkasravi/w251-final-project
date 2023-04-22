import os, shutil
from ultralytics import YOLO
from PIL import Image

from flask import Flask, flash, render_template, redirect, request, \
    send_from_directory, session, url_for
from werkzeug.utils import secure_filename
from markupsafe import escape # Escape user provided values in HTML

UPLOAD_FOLDER = 'static/images'
PRED_FOLDER =  'static/preds'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif'}
MAX_IMG_SIZE = 2 * 1000 * 1000 # Set max img size to ~2 MB
REMOTE_SERVER_URL = '' # URL for remote AWS server

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Set image upload folder
app.config['MAX_CONTENT_LENGTH'] = MAX_IMG_SIZE # Max file upload size

# Set to False for production. Required during development for debugging
dev_code = True
if dev_code:
    app.debug = True

# Secret key to some random bytes
app.secret_key = b'_5#yr2Lrwq"Fbzxb4Qasd8zavwewwe\n\xec]/'

# Pretrained YOLO model placeholder pending training


def run_model(img_src):
    
    model = YOLO('yolov8n.pt')    
    conf_threshold = 0.5
    results = model.predict(
        source=img_src,
        show=False,
        save_txt=False,
        save=True,
        project="static",
        name='preds',
        conf=conf_threshold
    )
    
    preds = []
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
    #    masks = result.masks  # Masks object for segmenation masks outputs
        probs = result.probs  # Class probabilities
    #    print(result.names)
        
        for box in boxes:
            x,y,width,height = box.xywh.tolist()[0]
            class_name = result.names[box.cls.tolist()[0]]
            conf = box.conf.tolist()[0]
#            print(f'Class Name: {class_name}, Confidence Interval: {conf:.4f} \n' \
#                'BB: x: {x}, y: {y}, width: {width}, height: {height} \n')
            preds.append({
                'x':x, 'y':y, 'width':width, 'height':height, 
                'confidence':conf, 'class':class_name, 'image_path':'NA', 
                'prediction_type':'NA'})
    
    im = Image.open(img_src)
    width, height = im.size
    #print(img_dict)    
    img_dict = {"predictions":preds, "image":{"width":width,"height":height}}
    print(img_dict)
    return img_dict

# Checks if upload extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_fileext(filename):
    return filename.rsplit('.', 1)[1].lower()

def img_cleanup():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for filename in os.listdir(PRED_FOLDER):
        file_path = os.path.join(PRED_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    # Try to remove the tree; if it fails, throw an error using try...except.
    try:
        shutil.rmtree(PRED_FOLDER)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/<name>')
def index_user(name):
    return render_template('index_user.html')

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(session['username'] + '.'
                + split_fileext(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            print(session['username'])
                       
            img_dict = run_model(os.path.join(app.config['UPLOAD_FOLDER'], 
                filename))

            cuisine = request.form.get("cuisine")
            img_dict["cuisine"] = cuisine

            # Post ingredient list to remote server
#           headers = {'Content-type': 'text/html; charset=UTF-8'}
#           response = requests.post(REMOTE_SERVER_URL, data=img_dict, headers=headers)            

            return redirect(url_for('index_user', name=session['username'], img_dict=img_dict))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index_user', 
            name=session['username']))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
    
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    
    img_cleanup()
    
    session.pop('username', None)
    return redirect(url_for('index'))
    
#@app.route('/user/<username>')
#def profile(username):
#    return f'{username}\'s profile'

'''@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")'''


#@app.route("/<name>")
#def hello(name):
#    return f"Hello, {escape(name)}!"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    # Required during development for debugging. Comment in production
    if dev_code:
        app.run(debug=True)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))    