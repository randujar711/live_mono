from app import app
from models import db, User, Post
from faker import Faker

def run_seeds():
    fake = Faker()
    print('Seeding database ... 🌱')
    # Add your seed data here
    with app.app_context():
      user1 = User('rmdashrfv', 'rmdashrfv@example.com', '111111111')
      user2 = User('mikegpt', 'mikegpt@example.com', '22222222')
      user3 = User('flyinggeese', 'flyinggeese@example.com', '33333333')
      db.session.add_all([user1, user2, user3])
      db.session.commit()
      user = User.query.first()
      seeded_posts = []
      for _ in range(5):
        post = Post(fake.text())
        post.user_id = user.id
        seeded_posts.append(post)
      db.session.add_all(seeded_posts)
      db.session.commit()
      print('Done! 🌳')

run_seeds()