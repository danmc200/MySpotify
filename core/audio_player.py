import spotify
import player_thread
import time

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
        self.artist = self.session.get_artist(artist)
        self.browser = self.artist.browse()
        self.browser.load()
        return self.browser

    def browse_album(self, album):
        self.album = self.session.get_album(album)
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
        track = self.p_thread.get_track()
        if(self.session.player.state != 'paused'):
            try:
                trackS = self.session.get_track(track.link.uri)
                trackS.load()
            except:
                print "couldn't play"#todo show in gui
            self.session.player.load(trackS)
            self.session.player.play()
        self.ui.post_track_event(track)
        self.session.player.play()

    def pause(self):
        if(self.session.player.state == 'paused'):
            self.play()
        else:
            self.session.player.pause()

    def stop(self):
        self.session.player.unload()

    def close(self):
        self.session.logout()
        self.p_thread.kill = True
