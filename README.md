 Features

- View available fruits with name, description, and price  
- Add fruits to the cart with quantity  
- Delete items from the cart  
- View cart total and checkout  
- Place orders (cart items converted into order items)  
- Flash messages for feedback  
- Fully functional frontend with Jinja templates  

- Python 3.x  
- Flask  
- SQLAlchemy (without Flask-SQLAlchemy)  
- HTML / CSS / Bootstrap  
- SQLite (default, can be replaced with PostgreSQL or MySQL)  

Clone the repository
git clone https://github.com/yourusername/flask-fruit-shop.git
cd flask-fruit-shop

Create a virtual environment
python -m venv venv

Activate the virtual environment
macOS/Linux
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Initialize the database
python
>>> from app.database import Base, engine
>>> Base.metadata.create_all(bind=engine)
>>> exit()
Run the Flask app
flask run
