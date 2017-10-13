# Create the table if table doesn't exist in database
# Table definition is in model.py
from model import *
engine = sqlalchemy.create_engine('postgresql://localhost:5432', echo=True)
Base.metadata.create_all(engine)
