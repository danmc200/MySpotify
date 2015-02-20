import threading, time

class VimListener(threading.Thread):

    def __init__(self, vim, player):
        super(VimListener, self).__init__()
        self.vim = vim
        self.player = player

    def run(self):
        while(1):
            is_quit = self.vim.eval('g:quitSpot')
            if(is_quit == 'true'):
                self.player.close()
                return
            time.sleep(.2)
