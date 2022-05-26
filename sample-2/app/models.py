from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    subject = Column(String(100), nullable=False)
    fname = Column(String(100), nullable=True)
    lname = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    message = Column(String(1000), nullable=False)
    
    created_at = Column(DateTime, default=func.now())

    def __init__(self, subject=None, fname=None, lname=None, email=None, message=None):
        self.subject = subject
        self.fname = fname
        self.lname = lname
        self.email = email
        self.message = message

    def __repr__(self):
        return f'<Submission {self.id!r}>'
