import wx

class SpotifyGUI(wx.Frame):

    def __init__(self, *args, **kw):
        super(SpotifyGUI, self).__init__(*args, **kw) 
        
    def set_player(self, player):
        self.player = player

    def init_gui(self):   
        pnl = wx.Panel(self)
        top_row = 25
        col_pos = 10
        search_size = 175

        self.searchText = wx.TextCtrl(self, -1, "", pos=(col_pos, top_row), size=(search_size, -1))
        self.searchText.SetInsertionPoint(0)
        col_pos += search_size + 10
        self.btn = wx.Button(self, label='Play', pos=(col_pos, top_row))
        col_pos += 100
        btn2 = wx.Button(self, label='Stop', pos=(col_pos, top_row))

        self.searchText.Bind(wx.EVT_KEY_UP, self.search)
        self.btn.Bind(wx.EVT_BUTTON, self.play)
        btn2.Bind(wx.EVT_BUTTON, self.stop)
        
        self.SetSize(wx.DisplaySize())
        self.SetTitle('My Spotify')
        self.Centre()
        self.Show(True)          
        
    def flip_play_or_pause_button(self):
        label = self.btn.GetLabel() 
        if(label == "Play"):
            label = "Pause"
        else:
            label = "Play"
        self.btn.SetLabel(label)

    def search(self, e):
        if(e.GetKeyCode() == wx.WXK_RETURN):
            search = self.player.search(self.searchText.GetLineText(0))
            track = search.tracks[0].link.uri
            self.player.play_track(track)
            self.flip_play_or_pause_button()

    def play(self, e):
        #track = 'spotify:track:3N2UhXZI4Gf64Ku3cCjz2g'
        if(self.btn.GetLabel() == "Play"):
            self.player.play()
        else:
            self.player.pause()
        self.flip_play_or_pause_button()

    def pause(self, e):
        self.player.pause()

    def stop(self, e):
        self.player.stop()

    def OnClose(self, e):
        self.player.close()
        self.Close(True)     
