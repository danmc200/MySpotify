#!/usr/bin/python
import spotify
import threading
import getpass

import wx, spotify_gui, player_thread

class AudioPlayer():

    def __init__(self, session):
        self.session = session
        self.audio = spotify.AlsaSink(session)
        self.loop = spotify.EventLoop(session)
        self.loop.start()
        self.p_thread = player_thread.PlayerThread(self, self.session)
        self.p_thread.start()

    def search(self, query):
        search = self.session.search(query)
        search.load()
        return search

    def browse_artist(self, artist):
        self.artist = session.get_artist(artist)
        self.browser = self.artist.browse()
        self.browser.load()
        return self.browser

    def browse_album(self, album):
        self.album = session.get_album(album)
        self.browser = self.album.browse()
        self.browser.load()
        return self.browser
        
    def set_queue(self, tracks):
        self.p_thread.set_queue(tracks)

    def play_track(self, track):
        self.p_thread.set_stop(False)
        try:
            track = session.get_track(track.link.uri)
            track.load()
            self.session.player.load(track)
            self.session.player.play()
        except:
            print "couldn't play"#todo show in gui

    def set_next_flag(self):
        self.p_thread.set_next_flag()
    def set_prev_flag(self):
        self.p_thread.set_prev_flag()

    def set_index(self, index):
        self.p_thread.set_index(index)

    def play(self):
        self.p_thread.set_stop(False)
        self.session.player.play()

    def pause(self):
        self.session.player.pause()

    def stop(self):
        self.p_thread.set_stop(True)
        self.session.player.unload()

    def close(self):
        self.session.logout()
        self.p_thread.kill_thread()

def get_username_password():
    un = raw_input('Enter Username\n')
    pwd = getpass.getpass('Enter password\n')
    return un, pwd

def login(session):
    logged_in_event = threading.Event()
    connection_state_listener = lambda sess: (
        logged_in_event.set() if sess.connection.state is spotify.ConnectionState.LOGGED_IN else 0)
    session.on(
        spotify.SessionEvent.CONNECTION_STATE_UPDATED,
        connection_state_listener)
    un, pwd = get_username_password()
    session.login(un, pwd)
    while not logged_in_event.wait(.1):
        session.process_events()

if __name__ == "__main__":
    session = spotify.Session()
    player = AudioPlayer(session)
    login(session)

    app = wx.App()
    ui = spotify_gui.SpotifyGUI(None)
    ui.init_gui(player)
    app.MainLoop()
