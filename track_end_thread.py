import spotify
import threading, time

class EndThread(threading.Thread):

    def __init__(self, player, session):
        super(EndThread, self).__init__()
        self.player = player
        self.session = session
        self.kill = False
    
    def kill_thread(self):
        self.kill = True

    def run(self):
        end_listener = lambda sess: (self.player.set_next_flag())
        self.session.on(spotify.SessionEvent.END_OF_TRACK, end_listener)
        while(1):
            if(self.kill):
                return
            time.sleep(.1)       
