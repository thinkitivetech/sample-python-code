Contact Us App
============== 

## Contact Us Page (Always public)

Fields of the Contact Us Form: 

- subject: Required Field , type text (must have a acceptable size limit)
- Name: Optional Field, type text (both first and last name with acceptable size limit for the field)
- Email: Required Field, type text (need acceptable size limit and Proper email validation will earn extra points) 
- Message: Required Field

Validation and other limit checks must be implemented in back-end (Python/Flask).
Note: For Optional email validation , don't send email to the provided email_id. Regex can be used to perform validation.

### Captcha Validation: 

On the contact form there must be a required Captcha field. 
This field will only accept numeric value.   

### Captcha question: 

What is the sum of `x` and `y` ?  

Here `x` and `y` both are integer and value (random value) must be within the range of `1 - 99` . 



### Contact Form Submission: 

Upon submission of contact form invalid submission must receive proper 
error message and valid submission must be stored in a database table. 


## Admin Section to view Submitted Queries 

### Listing Page of all submitted contact form

This page will list all the contact form submission. Tabular representation  
must provide the following fields 

- ID: Database table ID (type integer)
- Subject: subject of the contact form (show excerpt only)
- Name: display full name (can be empty)
- Email: Email from the contact form
- Message: Message of the contact form (show excerpt only)
- Date: Date of submission (database table must have proper field)
- Details: An Anchor to the details view page for the specific submission 

Ordering: descending order of submission data-time

Pagination (optional): Implementation of proper pagination will earn extra point. 


### Details view Page of a specific submission 

This page will provide the details of the submission. Fields can be viewed are


- Subject: subject of the contact form 
- Name: display full name (can be empty)
- Email: Email from the contact form
- Message: Message of the contact form 
- Date: Date of submission (database table must have proper field)



## Auth For Admin Section (Optional):

Implementation of this feature will earn extra points. 

Implement a basic auth to access admin section. If implemented then admin section must be inaccessible without proper 
authentication and user must receive appropriate error code. Username and password can be configured using environment 
variable. Please mention the details of the required env vars and usages on `README` file. 


## Docker: 

Please include valid Dockerfile within the repository and add documentation and instructions to run the application 
using docker on `README` file. 


## Git: 

Use git as version control system and host the repository on `gitlab.com` . 
Please share the link of the repository with gitlab account `actstylo` .  


## Gitlab Pipeline (Optional):

Implementation of this feature will earn extra points. 

Implement CI/CD Pipeline to build image of the application.  


## System Requirements:

- Programming language: Python (version >= 3.6)
- Web Framework: Flask 
- Frontend Framework: no specific requirements and plain html/css can be used but for convenience `Bootstrap` can be used 
- Database: Sqlite  
- ORM: SQLAlchemy 


Note: We are not expecting polished or good-looking frontend .
