from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    text_content = Column(String)

    def __repr__(self):
        return f"<Document(filename='{self.filename}', upload_date='{self.upload_date}')>"