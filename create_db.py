# Create the table if table doesn't exist in database
from model import *
engine = sqlalchemy.create_engine('postgresql://localhost:5432', echo=True)
Base.metadata.create_all(engine)
