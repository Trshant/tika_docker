from sqlalchemy import Column, Integer, String, LargeBinary, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BINARY

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(BINARY(16), primary_key=True)
    mdhash = Column(String(64), unique=True, nullable=False)
    meta_data = Column(JSON)
    file_path = Column(String(255), nullable=False, index=True)
    text_content = Column(Text)  # Or TEXT, depending on your needs
