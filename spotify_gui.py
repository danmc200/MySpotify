import wx

class SpotifyGUI(wx.Frame):

    def __init__(self, *args, **kw):
        super(SpotifyGUI, self).__init__(*args, **kw) 
        
    def set_player(self, player):
        self.player = player

    def InitUI(self):   
        pnl = wx.Panel(self)
        top_row = 25
        col_pos = 10
        search_size = 175

        self.searchText = wx.TextCtrl(self, -1, "", pos=(col_pos, top_row), size=(search_size, -1))
        self.searchText.SetInsertionPoint(0)
        col_pos += search_size + 10
        btn = wx.Button(self, label='Play', pos=(col_pos, top_row))
        col_pos += 100
        btn2 = wx.Button(self, label='Pause', pos=(col_pos, top_row))
        col_pos += 100
        btn3 = wx.Button(self, label='Stop', pos=(col_pos, top_row))

        self.searchText.Bind(wx.EVT_KEY_UP, self.search)
        btn.Bind(wx.EVT_BUTTON, self.play)
        btn2.Bind(wx.EVT_BUTTON, self.pause)
        btn3.Bind(wx.EVT_BUTTON, self.stop)
        
        self.SetSize(wx.DisplaySize())
        self.SetTitle('My Spotify')
        self.Centre()
        self.Show(True)          
        
    def search(self, e):
        if(e.GetKeyCode() == wx.WXK_RETURN):
            search = self.player.search(self.searchText.GetLineText(0))
            track = search.tracks[0].link.uri
            self.player.play(track)

    def play(self, e):
        #track = 'spotify:track:3N2UhXZI4Gf64Ku3cCjz2g'
        search = self.player.search(self.searchText.GetLineText(0))
        track = search.tracks[0].link.uri
        self.player.play(track)

    def pause(self, e):
        self.player.pause()

    def stop(self, e):
        self.player.stop()

    def OnClose(self, e):
        self.player.close()
        self.Close(True)     
