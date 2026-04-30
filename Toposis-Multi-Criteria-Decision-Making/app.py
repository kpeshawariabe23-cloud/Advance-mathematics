from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import numpy as np
import smtplib
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

app = Flask(__name__)
app.secret_key = 'topsis_secret_key'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def run_topsis(input_file, weights, impacts):
    df = pd.read_csv(input_file)
    weights = [float(w) for w in weights.split(',')]
    impacts = impacts.split(',')
    
    data = df.iloc[:, 1:].values.astype(float)
    norm = data / np.sqrt((data ** 2).sum(axis=0))
    weighted = norm * weights
    
    ideal_best = np.where([i == '+' for i in impacts], weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where([i == '+' for i in impacts], weighted.min(axis=0), weighted.max(axis=0))
    
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
    
    score = dist_worst / (dist_best + dist_worst)
    df['Topsis Score'] = score
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
    
    return df

def send_email(to_email, file_path):
    from_email = "your_email@gmail.com"  # Replace with your email
    password = "your_app_password"  # Replace with your app password
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "TOPSIS Result"
    
    body = "Please find attached the TOPSIS result file."
    msg.attach(MIMEText(body, 'plain'))
    
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=result.csv')
        msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        weights = request.form.get('weights', '')
        impacts = request.form.get('impacts', '')
        email = request.form.get('email', '')
        
        if not file or file.filename == '':
            flash('Please select a file')
            return redirect('/')
        
        if not weights or not impacts:
            flash('Weights and Impacts are required')
            return redirect('/')
        
        if not is_valid_email(email):
            flash('Format of email id must be correct')
            return redirect('/')
        
        weights_list = weights.split(',')
        impacts_list = impacts.split(',')
        
        if len(weights_list) != len(impacts_list):
            flash('Number of weights must be equal to number of impacts')
            return redirect('/')
        
        for imp in impacts_list:
            if imp.strip() not in ['+', '-']:
                flash('Impacts must be either +ve or -ve')
                return redirect('/')
        
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)
        
        result_path = os.path.join(UPLOAD_FOLDER, 'result.csv')
        result_df = run_topsis(input_path, weights, impacts)
        result_df.to_csv(result_path, index=False)
        
        send_email(email, result_path)
        flash('Result sent to your email!')
        return redirect('/')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


