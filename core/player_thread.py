import threading
import spotify
import time

class PlayerThread(threading.Thread):

    def __init__(self, player, session):
        super(PlayerThread, self).__init__()
        self.player = player
        self.session = session

        self.queue = []
        self.index = 0
        self.index_flag = False
        self.kill = False

    def get_track(self):
        return self.queue[self.index]
    
    def set_queue(self, queue):
        self.queue = queue

    def set_index_offset(self, index_offset):
        new_index = self.index + index_offset
        if(new_index >= 0 and new_index < len(self.queue)):
            self.index = new_index
            self.index_flag = True

    def set_index(self, index):
        self.index = index
        self.index_flag = True

    def kill_thread(self):
        self.kill = True

    def run(self):
        end_listener = lambda sess: (self.player.set_index_offset(1))
        self.session.on(spotify.SessionEvent.END_OF_TRACK, end_listener)
        while(not self.kill):
            if(self.index_flag):
                self.index_flag = False
                self.player.play()

            time.sleep(.1)
