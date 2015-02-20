import threading, time

class VimListener(threading.Thread):

    def __init__(self, vim, player, ui):
        super(VimListener, self).__init__()
        self.vim = vim
        self.player = player
        self.ui = ui
        self.kill = False
        self.actions = {
            'quit': self.quit, 
            'search': self.search,
            'next': self.play_next,
            'prev': self.play_prev,
            'pause': self.pause,
            'play': self.play}

    def quit(self):
        self.player.close()
        self.kill = True

    def reset(self):
        self.vim.command('let g:action=""')

    def search(self):
        self.reset()
        self.ui.do_search()

    def play_next(self):
        self.reset()
        self.player.set_index_offset(1)

    def play_prev(self):
        self.reset()
        self.player.set_index_offset(-1)

    def pause(self):
        self.reset()
        self.player.pause()

    def play(self):
        self.reset()
        self.player.play()
    
    def run(self):
        while(not self.kill):
            action_key = self.vim.eval('g:action')
            if(action_key in self.actions.keys()):
                action = self.actions[action_key]
                action()
            time.sleep(.2)
