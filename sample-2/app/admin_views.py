import base64
from flask import render_template, request, Response
from functools import wraps
from sqlalchemy import desc
from app import app
from .models import Submission

def check(authorization_header):
    username = "admin"
    password = "admin@123"
    encoded_uname_pass = authorization_header.split()[-1]

    if bytes(encoded_uname_pass, 'utf-8') == base64.b64encode(bytes(username + ":" + password, 'utf-8')):
        return True

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
    return decorated  

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    submissions = Submission.query.order_by(desc(Submission.created_at)).all()
    return render_template('admin/dashboard.html', submissions = submissions)
    
@app.route("/admin/submissions/<id>")
@login_required
def submission_details(id):
    submission = Submission.query.get(id)
    return render_template('admin/submission_details.html', submission = submission)
