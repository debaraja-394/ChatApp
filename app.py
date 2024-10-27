from flask import Flask,render_template,request,redirect,url_for
from flask_socketio import SocketIO,join_room,leave_room

app=Flask(__name__)
socketio=SocketIO(app)
port=5000
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
    # username=request.args.get('username')
    # roomID=request.args.get('roomID')
    return render_template('chat.html')

if __name__=='__main__':
    socketio.run(app,debug=True,port=port)