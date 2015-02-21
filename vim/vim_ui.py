import threading, time
import vim_listener

window_track = 0
window_album = 1
window_artist = 2

class VimUI():

    def __init__(self, vim):
        self.tracks = []
        self.albums = []
        self.artists = []
        self.vim = vim

    def init_ui(self, player):
        self.player = player
        self.listener = vim_listener.VimListener(self.vim, self.player, self)
        self.listener.start()

    def post_track_event(self, track):
        track_name = self.get_track_name(track)
        self.vim.command('/' + track_name)
        print track_name

    def play_next(self):
        self.player.set_index_offset(1)

    def play_prev(self):
        self.player.set_index_offset(-1)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def select(self):
        cur_win = self.vim.current.window
        i = 0
        for win in self.vim.windows:
            if win == cur_win:
                break
            i+=1
        row = cur_win.cursor[0] - 1
        if(i == window_track):
            self.player.play_track(row)
        elif(i == window_album):
            browser = self.player.browse_album(self.albums[row].link.uri)
            self.show_tracks(browser)
        elif(i == window_artist):
            browser = self.player.browse_artist(self.artists[row].link.uri)
            self.show_albums(browser)

    def do_search(self):
        query = self.vim.eval('g:query')
        if(query == ""):
            return
        results = self.player.search(query)
        self.show_tracks(results)
        self.show_albums(results)
        self.show_artists(results)

    def get_track_name(self, track):
        return track.name + " (" + track.artists[0].name + ")"

    def show_tracks(self, results):
        track_names = []
        queue = []
        self.tracks = []
        for track in results.tracks:
            track_name = self.get_track_name(track)
            if(track_name not in track_names):
                track_names.append(track_name)
                queue.append(track)
                self.tracks.append(track)
        self.player.set_queue(queue)
        cb = self.vim.windows[window_track].buffer
        cb[:] = None
        cb[:len(track_names)] = track_names

    def show_albums(self, results):
        album_names = []
        self.albums = []
        for album in results.albums:
            album_name = album.name 
            if(album_name not in album_names):
                album_names.append(album_name)
                self.albums.append(album)
        cb = self.vim.windows[window_album].buffer
        cb[:] = None
        cb[:len(album_names)] = album_names

    def show_artists(self, results):
        artist_names = []
        self.artists = []
        for artist in results.artists:
            artist_name = artist.name 
            if(artist_name not in artist_names):
                artist_names.append(artist_name)
                self.artists.append(artist)
        cb = self.vim.windows[window_artist].buffer
        cb[:] = None
        cb[:len(artist_names)] = artist_names

    def close(self):
        self.player.close()
        self.vim.command('qa!')
