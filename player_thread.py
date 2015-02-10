import threading
import spotify
import time

class PlayerThread(threading.Thread):

    def __init__(self, player, session):
        super(PlayerThread, self).__init__()
        self.player = player
        self.session = session

        self.queue = []
        self.stop = True
        self.next_flag = False
        self.prev_flag = False
        self.index = 0
        self.kill = False

    def set_stop(self, stop):
        self.stop = stop

    def set_queue(self, queue):
        self.queue = queue

    def set_prev_flag(self):
        index = self.index
        if(self.index-1 > 0):
            self.prev_flag = True
            index -= 1
        return self.queue[index]

    def set_next_flag(self):
        index = self.index
        if(self.index+1 < len(self.queue)-1):
            self.next_flag = True
            index += 1
        return self.queue[index]

    def set_index(self, index):
        self.index = index

    def kill_thread(self):
        self.kill = True

    def run(self):
        end_listener = lambda sess: (self.player.set_next_flag())
        self.session.on(spotify.SessionEvent.END_OF_TRACK, end_listener)
        while(1):
            if(self.kill):
                return
            elif(self.next_flag):
                self.next_flag = False
                self.index += 1
                self.player.play_track(self.queue[self.index])

            elif(self.prev_flag):
                self.prev_flag = False
                self.index -= 1
                self.player.play_track(self.queue[self.index])

            time.sleep(.1)
