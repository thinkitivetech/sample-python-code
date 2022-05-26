from flask import render_template, request, redirect, flash
from random import randint
import re

from app import app
from .models import Submission
from .database import db_session

def generate_captcha():
    val1 = randint(1, 99)
    val2 = randint(1, 99)
    return {'val1': val1, 'val2': val2}

def validate_captcha(form):
    val1 = int(form.get('val1'))
    val2 = int(form.get('val2'))
    if(val1+val2 == int(form.get('captcha'))):
        return True
    else:
        return False

def validate_contact_form(form):
    err_message = None
    missing = list()

    for k, v in form.items():
        if k in ['subject', 'email', 'message', 'captcha'] and v == "":
            missing.append(k)

    if missing:
        err_message = f"Missing fields for {', '.join(missing)}"
    
    if form.get('email') != '':
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, form.get('email')):
            err_message = "Invalid email address: "+form.get('email')
    
    if err_message:
        return False, err_message
    elif not validate_captcha(form):
        return False, 'Captcha is incorrect'
    else:
        return True, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact-us", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        valid, err_message = validate_contact_form(request.form)
        
        if(valid):
            submission = Submission(
                request.form.get('subject'),
                request.form.get('fname'),
                request.form.get('lname'),
                request.form.get('email'),
                request.form.get('message')
            )
            db_session.add(submission)
            db_session.commit()
            flash("Thankyou for Submitting, Contact form Saved!")
            return redirect(request.url)
        else:
            return render_template("public/contact-us.html", err_message=err_message, form=request.form, captcha = generate_captcha())

    return render_template("public/contact-us.html", form='', captcha = generate_captcha())
