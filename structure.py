from app import app
from models import db, User
with app.app_context():
    user3 = User(name = 'manas', email = 'abc@gmail.com', username='manager', role='manager', approved=True)
    user3.set_password('password')
    # db.session.add_all([user1, user2, user3])
    db.session.add_all([user3])
    db.session.commit()
