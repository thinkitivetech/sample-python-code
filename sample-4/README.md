## Custom User Authenticaiton

#### Setup

Create virtual environment
python -m venv venv

Activate virtual environment
source venv/bin/activate

Install the requirements
pip install -r requirements.txt

Create .env file in project level and add following lines-
        export EMAIL_USE_TLS=True
        export EMAIL_HOST=smtp.gmail.com
        export EMAIL_HOST_USER=Enter mail id to send verification mail
        export EMAIL_HOST_PASSWORD=Mail password
        export EMAIL_PORT=587

        SECRET_KEY= Secret key from setting.py file 

        DATABASE_NAME=Your postgres database name
        DATABASE_USER=user name
        DATABASE_PASSWORD=Password
        DATABASE_HOST=localhost


Migrations 
python manage.py makemigrations
python manage.py migrate


Run on localhost-
python manage.py runserver 


To access all api
http://127.0.0.1:8000/swagger/
