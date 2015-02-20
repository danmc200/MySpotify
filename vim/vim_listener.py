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
            'search': self.ui.do_search,
            'next': self.ui.play_next,
            'prev': self.ui.play_prev,
            'pause': self.ui.pause,
            'play': self.ui.play}

    def quit(self):
        self.player.close()
        self.kill = True

    def run(self):
        while(not self.kill):
            action_key = self.vim.eval('g:action')
            if(action_key in self.actions.keys()):
                action = self.actions[action_key]
                action()
                self.vim.command('let g:action=""')
            time.sleep(.2)
