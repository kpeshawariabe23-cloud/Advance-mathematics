import streamlit as st
import pandas as pd
import numpy as np
import smtplib
import re
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

st.set_page_config(page_title="TOPSIS Web Service", page_icon="📊")

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def run_topsis(df, weights, impacts):
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

def send_email(to_email, csv_data):
    from_email = st.secrets.get("EMAIL", "")
    password = st.secrets.get("EMAIL_PASSWORD", "")
    
    if not from_email or not password:
        return False
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "TOPSIS Result"
    
    body = "Please find attached the TOPSIS result file."
    msg.attach(MIMEText(body, 'plain'))
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_data.encode())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=result.csv')
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    return True

st.title("TOPSIS Web Service")

uploaded_file = st.file_uploader("File Name", type=['csv'])
weights = st.text_input("Weights", placeholder="1,1,1,1")
impacts = st.text_input("Impacts", placeholder="+,+,-,+")
email = st.text_input("Email Id", placeholder="example@gmail.com")

if st.button("Submit"):
    if uploaded_file is None:
        st.error("Please select a file")
    elif not weights or not impacts:
        st.error("Weights and Impacts are required")
    elif not is_valid_email(email):
        st.error("Format of email id must be correct")
    else:
        weights_list = weights.split(',')
        impacts_list = impacts.split(',')
        
        if len(weights_list) != len(impacts_list):
            st.error("Number of weights must be equal to number of impacts")
        elif not all(imp.strip() in ['+', '-'] for imp in impacts_list):
            st.error("Impacts must be either +ve or -ve")
        else:
            df = pd.read_csv(uploaded_file)
            result_df = run_topsis(df, weights, impacts)
            
            csv_data = result_df.to_csv(index=False)
            
            if send_email(email, csv_data):
                st.success("Result sent to your email!")
            else:
                st.warning("Email not configured. Download result below:")
            
            st.download_button("Download Result", csv_data, "result.csv", "text/csv")
            st.dataframe(result_df)


