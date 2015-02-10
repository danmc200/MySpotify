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
        self.prev_flag = True

    def set_next_flag(self):
        self.next_flag = True

    def set_index(self, index):
        self.index = index

    def kill_thread(self):
        self.kill = True

    def run(self):
        while(1):
            if(self.kill):
                return
            if(self.session.player.state == 'unloaded' and len(self.queue) > 0 and not self.stop):
                self.index += 1
                self.player.play_track(self.queue[self.index])

            elif(self.next_flag):
                self.next_flag = False
                if(self.index+1 < len(self.queue)-1):
                    self.index += 1
                    self.player.play_track(self.queue[self.index])

            elif(self.prev_flag):
                self.prev_flag = False
                if(self.index-1 > 0):
                    self.index -= 1
                    self.player.play_track(self.queue[self.index])

            time.sleep(.1)
