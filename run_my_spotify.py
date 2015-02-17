#!/usr/bin/python
import spotify
import threading
import getpass
import wx
import spotify_gui, player_thread, my_events

class AudioPlayer():

    def __init__(self, session, ui):
        self.session = session
        self.ui = ui
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

    def play_track(self, index):
        self.p_thread.set_index(index)

    def set_index_offset(self, index_offset):
        self.p_thread.set_index_offset(index_offset)

    def play(self):
        if(self.session.player.state != 'paused'):
            try:
                track = self.p_thread.get_track()
                trackS = session.get_track(track.link.uri)
                trackS.load()
                self.session.player.load(trackS)
                self.session.player.play()
                evt = my_events.DisplayTrackEvent(my_events.myEVT_DISPLAY_TRACK, -1, track)
                wx.PostEvent(self.ui, evt)
            except:
                print "couldn't play"#todo show in gui
        self.session.player.play()

    def pause(self):
        self.session.player.pause()

    def stop(self):
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
    app = wx.App()
    ui = spotify_gui.SpotifyGUI(None)

    session = spotify.Session()
    player = AudioPlayer(session, ui)
    login(session)

    ui.init_gui(player, my_events)
    app.MainLoop()
