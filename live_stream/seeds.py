from app import app
from models import db, User, Property, Room
# from faker import Faker

def run_seeds():
    # fake = Faker()
    print('Seeding database ... 🌱')
    # Add your seed data here
    with app.app_context():
      user1 = User('ryanusername', 'example@example.com', '123', 'Ryan Andujar', '[]')
      
      print('this is the user', user1)
      db.session.add_all([user1])
      db.session.commit()
      print('user committed')
      properties = [
          {'price': '200', 'name': 'Go', 'hotel': False, 'hotel_price': '0', 'user_id':'0'},
          {'price': '200', 'name': 'Central Park', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Empire State Building', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Statue of Liberty', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '0', 'name': 'Go to Jail', 'hotel': False, 'hotel_price': '0', 'user_id': '0'},
          {'price': '200', 'name': 'Lincoln Tunnel', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Port Authority', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '100', 'name': 'Pay 100', 'hotel': False, 'hotel_price': '0', 'user_id': '0'},
          {'price': '200', 'name': 'Trump Tower', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Tiffany & Co.', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '0', 'name': 'Back 3 Spaces', 'hotel': False, 'hotel_price': '0', 'user_id': '0'},
          {'price': '200', 'name': 'Kiss FM', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Thirteen .Net', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'New York Times', 'hotel': False,'hotel_price': '600', 'user_id': '0', 'user_id': '0'},
          {'price': '0', 'name': 'Muted', 'hotel': False, 'hotel_price': '0', 'user_id': '0'},
          {'price': '200', 'name': 'Rangers', 'hotel': False,'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Knicks', 'hotel': False,'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'MSG', 'hotel': False,'hotel_price': '600', 'user_id': '0'},
          {'price': '0', 'name': 'Go to Go', 'hotel': False,'hotel_price': '0', 'user_id': '0'},
          {'price': '200', 'name': 'Essex House', 'hotel': False,'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'The Plaza', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'The Regency Hotel', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Macys', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Fao Schwartz', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Bloomingdales', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'CitiBank', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Delotte & Touche', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '200', 'name': 'Smothsonian', 'hotel': False, 'hotel_price': '600', 'user_id': '0'},
          {'price': '0', 'name': 'jail', 'hotel': False, 'hotel_price': '0', 'user_id': '0'}
          ]

      property_list = []

      for item in properties:
          try:
              prop = Property(
                  price=item['price'],
                  name=item['name'],
                  hotel=item['hotel'],
                  hotel_price=item['hotel_price'], 
                  user_id= item['user_id']
              )
              property_list.append(prop)
          except Exception as e:
              print(f"Error creating property {item}: {e}")
          
      print('this is the prop list', property_list)
      db.session.add_all(property_list)
      room = Room(True, [user1]) 
      # I need to pass a list of instances into the constructor, not a string, this will need to change when I make functionality to add  multiple users 
      print('this is room', room)
      db.session.add(room)
      db.session.commit()
      print('Done! 🌳')
      print('room', room)
      print('this is the prop list', property_list)

run_seeds()