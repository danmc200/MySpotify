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
        row = cur_win.cursor[0]-1
        win_num = 0#windowlist?
        for win in self.vim.windows:
            if win == cur_win:
                break
            win_num+=1

        if(win_num == window_track):
            self.player.play_track(row)
        elif(win_num == window_album):
            browser = self.player.browse_album(self.albums[row].link.uri)
            self.show_tracks(browser)
        elif(win_num == window_artist):
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

    def show(self, col, results_col, window, decor=None):
        names = []
        for el in results_col:
            name = el.name
            if(decor != None):
                name = decor(el)
            if(name not in names):
                names.append(name)
                col.append(el)
        cb = self.vim.windows[window].buffer
        cb[:] = None
        cb[:len(names)] = names
        return col

    def show_tracks(self, results):
        self.tracks = []
        self.tracks = self.show(self.tracks, results.tracks, window_track, self.get_track_name)
        self.player.set_queue(self.tracks)

    def show_albums(self, results):
        self.albums = []
        self.albums = self.show(self.albums, results.albums, window_album)

    def show_artists(self, results):
        self.artists = []
        self.artists = self.show(self.artists, results.artists, window_artist)

    def close(self):
        self.player.close()
        self.vim.command('qa!')
