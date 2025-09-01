from myapp.database import Base, engine
import myapp.models

Base.metadata.create_all(bind=engine)
print("Database created!")
