from flask import Flask, render_template, request
import csv
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CSV_FILE = 'doulas.csv'

# Route: Registration form
@app.route('/')
def index():
    return render_template('register.html')

# Route: Handle registration form submission
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    area = request.form['area']
    email = request.form['email']
    phone = request.form['phone']
    experience = request.form['experience']
    expertise = request.form['expertise']

    # Save uploaded picture
    picture = request.files['picture']
    filename = secure_filename(picture.filename)
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    picture.save(picture_path)

    # Save data to CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, area, email, phone, experience, expertise, filename])

    return render_template('register.html', message="You are successfully registered!")

# Route: Display all doulas
@app.route('/doulas')
def doulas():
    doulas = []
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, header=None)
        for row in df.values:
            if len(row) == 7:  # Ensure row is complete
                name, area, email, phone, experience, expertise, image = row
                doulas.append({
                    'name': name,
                    'area': area,
                    'experience': int(experience),
                    'expertise': expertise,
                    'phone':phone,
                    
                    'image': image
                })
    return render_template('doulas.html', doulas=doulas)

if __name__ == '__main__':
    app.run(debug=True)
