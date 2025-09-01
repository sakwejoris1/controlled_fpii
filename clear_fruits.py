from myapp.database import SessionLocal
from myapp.models import Fruit

# Create a session
db = SessionLocal()

# Delete all fruits
num_deleted = db.query(Fruit).delete()
db.commit()

db.close()

print(f"Deleted {num_deleted} fruits from the database!")
