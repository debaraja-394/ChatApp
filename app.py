from flask import Flask,render_template,request,redirect,url_for
from flask_socketio import SocketIO,join_room,leave_room
from flask_login import LoginManager, login_user
from ChatApp import db
from users import User

app=Flask(__name__)
socketio=SocketIO(app)
port=5000
login_manager=LoginManager()
login_manager.init_app(app)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        username=request.form['username']
        roomID=request.form['roomID']
        print(username)

        if username and roomID : 
            return render_template("chat.html",username=username,roomID=roomID)
        else: 
            redirect(url_for('home'))

    return render_template("index.html")

@login_manager.user_loader
def load_user(username):
    return db.get_user(username)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        message=""
        username=request.form['username']
        password=request.form['password']
        user=db.get_user(username)
        if user and User.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message="Failed to Login !!"
    return render_template('login.html',message=message)


@socketio.on('join_room')
def handleEventJoin(data):
    app.logger.info("{} is the username and room is: {}".format(data['username'],data['roomID']))
    join_room(data['roomID'])
    socketio.emit('join_room_announcement',data,room=data['roomID'])

@socketio.on('leave_room')
def handleEventLeave(data):
    app.logger.info("{} is the username and room is: {}".format(data['username'],data['roomID']))
    leave_room(data['roomID'])
    socketio.emit('leave_room_announcement',data,room=data['roomID'])

@socketio.on('send_message')
def handle_send_message(data):
    app.logger.info("{} is the username and room is: {} \n the message is: {}".format(data['username'],data['roomID'],data['message']))
    socketio.emit('receive_message',data,room=data['roomID'])

@app.route('/chat',methods=['POST','GET'])
def chat():
    return render_template('chat.html')

if __name__=='__main__':
    socketio.run(app,debug=True,port=port)