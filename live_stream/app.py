import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User
from pprint import pprint
from flask_socketio import SocketIO, emit
import platform
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins='*')

# In Rails, controller actions and routes are separate
# Here in Flask, they are put together

@app.get('/')
def home():
    return send_file('welcome.html')


@app.get('/example')
def example():
    return {'message': 'Your app is running Python'}


@app.get('/info')
def info():
    print(dir(platform))
    return {'machine': platform.node()}


@app.post('/users')
def users():
    data = request.form
    user = User(data['username'], data['email'], data['password'])
    print(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.post('/login')
def login():
    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'No user found'}), 404
    given_password = data['password']
    if user.password == given_password:
        # encode JWT as the token variable, signing it with our application's secret key
        # we store only what the token will need while identifying the users on any given request
        token = create_access_token(identity=user.id)
        return jsonify({'user': user.to_dict(), 'token': token})
    else:
        return jsonify({'error': 'Invalid email or password'}), 422


@app.get('/users/<int:id>')
def show(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    else:
        return {}, 404


# run user.to_dict() for every user in users
@app.get('/users')
def all_users():
    users = User.query.all()
    User.query.count()
    return jsonify([user.to_dict() for user in users])


@app.patch('/users/<int:id>')
def update_user(id):
    user = User.query.get_or_404(id)
    user.username = request.form['username'] # currently only updates the username. Add more as you see fit
    db.session.commit()
    return jsonify(user.to_dict())


# This is how we protect routes. Ideally you'd check to ensure that the current_user id
# is the same as the id of the user who owns the resources being deleted
@app.delete('/users/<int:id>')
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if user:
        # db.session.delete(user)
        # db.session.commit()
        current_user = get_jwt_identity() # get the current user ID (not the object itself)
        print('deleting user')
        return jsonify(user.to_dict())
    else:
        return {'error': 'No user found'}, 404    


# def login():
#      data = request.form
#       user = User.query.filter_by(email=data['email']).first()
#        if not user:
#             return jsonify({'error': 'No accoutn found'}), 404
#         else:
#             given_password = data['password']
#             if user.paswrod == given_password:
#                 # authenticate user
#                 token = create_access_token(identity=user.id)
#                 return jsonify({'user': user.to_dict(), 'token': token})
#             else:
#                 return jsonify({'error': 'invalid password'}), 422

@app.get('/posts/<int:id>')
def show_post(id):
    post = Post.query.get(id)
    return jsonify(post.to_dict())


# Below->>>>Define an event handler for the join event and get the username and room from the client’s argument. Add the client to that room with join_room. Now, send a ready event to all other connected peers(only one in our case) using emit with the help of skip_sid = request.sid.
@socketio.on('join')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print('RoomEvent: {} has joined the room {}\n'.format(username, room))
    emit('ready', {username: username}, to=room, skip_sid=request.sid)


# Below ->>>> Define an event handler for the data event. This will be used to transfer the data part of the message from the sender to the other client(by excluding the sender’s sid with skip_sid).                  This is PROB where we would pass game data
@socketio.on('data')
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print('DataEvent: {} has sent the data:\n {}\n'.format(username, data))
    emit('data', data, to=room, skip_sid=request.sid)

# Below ->>>>> Our basic signaling server is almost ready now. All that’s left is to handle various errors and deploy it to production. Of course, don’t forget to stop the server on encountering any errors.


@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()


# @socketio.on('connect')
# def connected():
#     '''This function is an event listener that gets called when the client connects to the server'''
#     print(f'Client {request.sid} has connected')
#     emit('connect', {'data': f'id: {request.sid} is connected'})


# @socketio.on('data')
# def handle_message(data):
#     '''This function runs whenever a client sends a socket message to be broadcast'''
#     print(f'Message from Client {request.sid} : ', data)
#     emit('data', {'data': 'data', 'id': request.sid}, broadcast=True)


# @socketio.on("disconnect")
# def disconnected():
#     '''This function is an event listener that gets called when the client disconnects from the server'''
#     print(f'Client {request.sid} has disconnected')
#     emit('disconnect', f'Client {request.sid} has disconnected', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ.get('PORT', 3000))