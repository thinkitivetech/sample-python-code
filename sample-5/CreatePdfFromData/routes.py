from __main__ import app
from flask import Flask, render_template, request
from flask_weasyprint import render_pdf, HTML
from reportlab.pdfgen import canvas


# Displays html form to get user data
@app.route('/')
def show_form():
    return render_template("form.html")


# Create pdf using data submited by user 
@app.route('/create-pdf', methods = ['POST'])
def create_pdf():
    if request.headers.get('Content-Type') == "application/json":
        data = request.json
    else:
        data = request.form.to_dict()
    print("data = ",data)        
    html = render_template('pdf_template.html', data=data)
    pdf = HTML(string=html).write_pdf("static/generatedpdfs/"+data['first_name']+".pdf")
    return "PDF saved successfully"

