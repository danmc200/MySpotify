import threading, time
import vim_listener

class VimUI():

    def __init__(self, vim):
        self.tracks = {}
        self.queue = []
        self.vim = vim

    def init_ui(self, player):
        self.player = player
        self.listener = vim_listener.VimListener(self.vim, self.player, self)
        self.listener.start()

    def post_track_event(self, track):
        print track.name

    def do_search(self):
        self.vim.command("let query=input('enter search: ')")
        query = self.vim.eval('query')
        results = self.player.search(query)
        self.show_tracks(results)

    def show_tracks(self, results, artist=True):
        track_names = []
        for track in results.tracks:
            track_name = track.name 
            if(artist):
                track_name += " (" + track.artists[0].name + ")"
            if(track_name not in track_names):
                track_names.append(track_name)
                self.queue.append(track)
                self.tracks[track_name] = track
        self.player.set_queue(results.tracks)
        cb = self.vim.current.buffer
        cb[: len(track_names)] = track_names
        self.player.play_track(0)#TODO
