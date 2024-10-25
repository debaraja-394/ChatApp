from flask import Flask,render_template,request,redirect,url_for
from flask_socketio import SocketIO

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
def handleEvent(data):
    app.logger.info("{} is the username and room is: {}".format(data['username'],data['roomID']))

@app.route('/chat',methods=['POST','GET'])
def chat():
    # username=request.args.get('username')
    # roomID=request.args.get('roomID')
    return render_template('chat.html')

if __name__=='__main__':
    socketio.run(app,debug=True,port=port)