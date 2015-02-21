import threading, time
import vim_listener

class VimUI():

    def __init__(self, vim):
        self.tracks = {}
        self.albums = {}
        self.artists = {}
        self.vim = vim

    def init_ui(self, player):
        self.player = player
        self.listener = vim_listener.VimListener(self.vim, self.player, self)
        self.listener.start()
        self.vim.command('set hls')

    def post_track_event(self, track):
        self.vim.command('/' + track.name)
        print track.name

    def play_next(self):
        self.player.set_index_offset(1)

    def play_prev(self):
        self.player.set_index_offset(-1)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def do_search(self):
        query = self.vim.eval('g:query')
        if(query == ""):
            return
        results = self.player.search(query)
        self.show_tracks(results)
        self.show_albums(results)
        self.show_artists(results)

    def show_tracks(self, results, artist=True):
        track_names = []
        queue = []
        for track in results.tracks:
            track_name = track.name 
            if(artist):
                track_name += " (" + track.artists[0].name + ")"
            if(track_name not in track_names):
                track_names.append(track_name)
                queue.append(track)
                self.tracks[track_name] = track
        self.player.set_queue(queue)
        cb = self.vim.windows[0].buffer
        cb[:len(track_names)] = track_names
        self.player.play_track(0)#TODO

    def show_albums(self, results):
        album_names = []
        for album in results.albums:
            album_name = album.name 
            if(album_name not in album_names):
                album_names.append(album_name)
                self.albums[album_name] = album
        cb = self.vim.windows[1].buffer
        cb[:len(album_names)] = album_names

    def show_artists(self, results):
        artist_names = []
        for artist in results.artists:
            artist_name = artist.name 
            if(artist_name not in artist_names):
                artist_names.append(artist_name)
                self.artists[artist_name] = artist
        cb = self.vim.windows[2].buffer
        cb[:len(artist_names)] = artist_names
