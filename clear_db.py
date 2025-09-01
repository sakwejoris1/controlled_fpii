from myapp.database import Base, engine

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("All tables dropped!")
