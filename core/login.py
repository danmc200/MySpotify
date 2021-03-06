import spotify
import threading
import getpass
import os

def get_username_password():
    un = raw_input('Enter Username\n')
    pwd = getpass.getpass('Enter password\n')
    return un, pwd

def login(session, un, pwd):
    logged_in_event = threading.Event()
    connection_state_listener = lambda sess: (
        logged_in_event.set() if sess.connection.state is spotify.ConnectionState.LOGGED_IN else 0)
    session.on(
        spotify.SessionEvent.CONNECTION_STATE_UPDATED,
        connection_state_listener)
    session.login(un, pwd)
    while not logged_in_event.wait(.1):
        session.process_events()

def get_session():
    config = spotify.Config()
    filename = os.path.dirname(os.path.realpath(__file__)) + "/spotify_appkey.key"
    config.load_application_key_file(filename=filename)
    session = spotify.Session(config=config)
    return session
