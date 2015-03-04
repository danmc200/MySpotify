import threading, time

class VimListener(threading.Thread):

    def __init__(self, vim, ui):
        super(VimListener, self).__init__()
        self.vim = vim
        self.ui = ui
        self.kill = False
        self.actions = {
            'quit': self.quit, 
            'search': self.ui.do_search,
            'next': self.ui.play_next,
            'prev': self.ui.play_prev,
            'pause': self.ui.pause,
            'play': self.ui.play,
            'select': self.ui.select}

    def quit(self):
        self.kill = True

    def run(self):
        while(not self.kill):
            action_key = self.vim.eval('g:action')
            if(action_key in self.actions.keys()):
                self.vim.command('let g:action=""')
                action = self.actions[action_key]
                action()
            time.sleep(.1)
        self.ui.close()
