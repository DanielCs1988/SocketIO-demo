from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)

# Setting the secret key is a necessity for SocketIO. You should fetch this from an envvar normally.
app.secret_key = 'super_secret_key'
app.debug = True

# Creating an instance of the SocketIO object, we pass the current app as a parameter.
# This will act as our API to interact with the socket connections.
socket = SocketIO(app)

# Just to spare you the effort of setting up a database for this small demo.
# This also means that the chat/text history will be purged when the server shuts down.
chat_history = []
text_history = ''


@app.route('/')
def login_page():
    # We can still use normal HTTP flask routes just like before.
    # We should also serve individual HTML files this way.
    return render_template('login.html')


@app.route('/login')
def login_user():
    # Please note that SocketIO alters the way session behaves, so we should assert it's state
    # (handle the login attempt) before opening up the socket connection.
    nickname = request.args['nickname']
    if len(nickname) >= 5:
        session['user'] = nickname
        paragraph_text = text_history if text_history else get_bacon_ipsum()
        return render_template('index.html', paragraph_text=paragraph_text, chat_history=chat_history)

    return redirect(url_for('login_page'))


@socket.on('connect')
def init_socket_connection():
    # Connect is the default event that is fired when a client opens a socket connection.
    # The script does not allow unauthorized connection, but the console can be exploited to bypass that,
    # so we need this extra layer of security. Disconnect cuts the socket connection.
    if not session.get('user'):
        disconnect()


@socket.on('chat')
def handle_incoming_chat_message(chat_msg):
    # Appending the name of the current user to the message, while converting it to a dictionary.
    full_msg = {'nick': session.get('user'), 'message': chat_msg}

    # First we save the message to the 'database'.
    chat_history.append(full_msg)

    # Then we broadcast the message to all the connected clients, including sender.
    # Dictionary is automatically converted to JSON.
    emit('chat', full_msg, broadcast=True)

    # It's nice to give a feedback to the sender about the successful data transfer.
    # This message is overly verbose for demonstration purposes. See the script side for more info.
    return 'Message received and saved.'


@socket.on('text-edited')
def update_paragraph(text):
    # We are broadcasting the current state of the paragraph after each and every keystroke.
    # Providing a return value - aka feedback to the sender - is not necessary as you can see.
    emit('text-edited', text, broadcast=True, include_self=False)

    # Saving the current state of the text for the new arrivals.
    global text_history
    text_history = text


def get_bacon_ipsum():
    with open('bacon.txt') as file:
        return file.read()


if __name__ == '__main__':
    # Please note that we have to call run on the socket, not the app.
    socket.run(app)
