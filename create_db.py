from myapp.database import Base, engine
from myapp import models

Base.metadata.create_all(bind=engine)
print("Database created!")
