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
        self.searchText.SetFocus()
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

    def show_results(self, search):
        self.show_tracks(search)
        self.show_albums(search)
        self.show_artists(search)

    def show_tracks(self, search, artist=True):
        track_names = []
        self.tracks = {}
        for track in search.tracks:
            track_name = track.name 
            if(artist):
                track_name += " (" + track.artists[0].name + ")"
            if(track_name not in track_names):
                track_names.append(track_name)
                self.tracks[track_name] = track
        self.tracks_label = wx.StaticText(self, label="Tracks:", pos=(10,80))
        self.listbox = wx.ListBox(self, choices=track_names, pos=(10, 100), size=(500, 700))
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.play_track)

    def clear_albums(self, search):
        self.clear(self.album_listbox)
    def show_albums(self, search):
        albums_names = []
        self.albums = {}
        for album in search.albums:
            if(album.name not in albums_names):
                albums_names.append(album.name)
                self.albums[album.name] = album
        self.album_label = wx.StaticText(self, label="Albums:", pos=(520,80))
        self.album_listbox = wx.ListBox(self, choices=albums_names, pos=(520, 100), size=(500, 700))
        self.album_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_album)

    def clear_artists(self, search):
        self.clear(self.artist_listbox)
    def show_artists(self, search):
        artists_names = []
        self.artists = {}
        for artist in search.artists:
            if(artist.name not in artists_names):
                artists_names.append(artist.name)
                self.artists[artist.name] = artist
        self.artist_label = wx.StaticText(self, label="Artists:", pos=(1040,80))
        self.artist_listbox = wx.ListBox(self, choices=artists_names, pos=(1040, 100), size=(500, 700))
        self.artist_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_artist)

    def clear(self, lb):
        leng = lb.GetCount()
        for index in range(0, leng):
            lb.Delete(0) 

    def browse_artist(self, e):
        select = self.artist_listbox.GetSelection()
        if(select == wx.NOT_FOUND):
            print "not found"
            return
        artist_name = self.artist_listbox.GetString(select)
        artist = self.artists[artist_name]
        browser = self.player.browse_artist(artist.link.uri)
        self.show_albums(browser)

    def browse_album(self, e):
        select = self.album_listbox.GetSelection()
        if(select == wx.NOT_FOUND):
            print "not found"
            return
        album_name = self.album_listbox.GetString(select)
        album = self.albums[album_name]
        browser = self.player.browse_album(album.link.uri)
        self.show_tracks(browser)

    def play_track(self,e):
        select = self.listbox.GetSelection()
        if(select == wx.NOT_FOUND):
            print "not found"
            return
        track_name = self.listbox.GetString(select)
        track = self.tracks[track_name]
        self.player.play_track(track.link.uri)
        self.btn.SetLabel("Pause")

    def search(self, e):
        if(e.GetKeyCode() == wx.WXK_RETURN):
            search = self.player.search(self.searchText.GetLineText(0))
            self.show_results(search)

    def play(self, e):
        #track = 'spotify:track:3N2UhXZI4Gf64Ku3cCjz2g'
        if(self.btn.GetLabel() == "Play"):
            self.player.play()
            self.btn.SetLabel("Pause")
        else:
            self.player.pause()
            self.btn.SetLabel("Play")

    def pause(self, e):
        self.player.pause()

    def stop(self, e):
        self.player.stop()

    def OnClose(self, e):
        self.player.close()
        self.Close(True)     
