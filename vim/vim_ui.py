import threading, time
import vim_listener

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

    def select(self):
        cur_win = self.vim.current.window
        i = 0
        for win in self.vim.windows:
            if win == cur_win:
                break
            i+=1
        row = cur_win.cursor[0] - 1
        if(i == 0):
            self.player.play_track(row)
        if(i == 1):
            browser = self.player.browse_album(self.albums[row].link.uri)
            self.show_tracks(browser)
        if(i == 2):
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

    def show_tracks(self, results, artist=True):
        track_names = []
        queue = []
        self.tracks = []
        for track in results.tracks:
            track_name = track.name 
            if(artist):
                track_name += " (" + track.artists[0].name + ")"
            if(track_name not in track_names):
                track_names.append(track_name)
                queue.append(track)
                self.tracks.append(track)
        self.player.set_queue(queue)
        cb = self.vim.windows[0].buffer
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
        cb = self.vim.windows[1].buffer
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
        cb = self.vim.windows[2].buffer
        cb[:] = None
        cb[:len(artist_names)] = artist_names

    def close(self):
        self.player.close()
        self.vim.command('qa!')
