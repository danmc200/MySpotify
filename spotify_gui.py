import wx

class SpotifyGUI(wx.Frame):

    def __init__(self, *args, **kw):
        super(SpotifyGUI, self).__init__(*args, **kw) 
        self.last_pos = (20,10)
        self.listbox_margin = 20
        self.listbox_count = 3
        
    def init_gui(self, player, EVT_DISPLAY_TRACK):
        self.player = player
        pnl = wx.Panel(self)
        search_size = 175
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(EVT_DISPLAY_TRACK, self.display_track)

        self.searchText = wx.TextCtrl(self, -1, "", pos=self.get_next_pos(0), size=(search_size, -1))
        self.searchText.SetInsertionPoint(0)
        self.searchText.SetFocus()
        self.searchText.Bind(wx.EVT_KEY_UP, self.search)

        self.btn = wx.Button(self, label='Play', pos=self.get_next_pos(search_size+10))
        self.btn.Bind(wx.EVT_BUTTON, self.play)

        btn2 = wx.Button(self, label='Stop', pos=self.get_next_pos(100))
        btn2.Bind(wx.EVT_BUTTON, self.stop)

        btn3 = wx.Button(self, label='Prev', pos=self.get_next_pos(100))
        btn3.Bind(wx.EVT_BUTTON, self.play_prev)

        btn4 = wx.Button(self, label='Next', pos=self.get_next_pos(100))
        btn4.Bind(wx.EVT_BUTTON, self.play_next)

        self.playing_label = wx.StaticText(self, label="Track: ", pos=(20, 40))
        self.set_playing_label_color(self.playing_label)

        self.set_next_pos(20, 80)
        listbox_size = self.get_listbox_size()
        self.tracks_label = wx.StaticText(self, label="Tracks:", pos=self.get_next_pos(0))
        self.set_label_color(self.tracks_label)
        self.listbox = wx.ListBox(self, choices=[], pos=self.get_pos_offset(height_off=20), size=listbox_size)
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.play_track)
        self.set_listbox_color(self.listbox)

        self.album_label = wx.StaticText(self, label="Albums:", pos=self.get_next_pos(listbox_size[0] + self.listbox_margin))
        self.set_label_color(self.album_label)
        self.album_listbox = wx.ListBox(self, choices=[], pos=self.get_pos_offset(height_off=20), size=listbox_size)
        self.album_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_album)
        self.set_listbox_color(self.album_listbox)

        self.artist_label = wx.StaticText(self, label="Artists:", pos=self.get_next_pos(listbox_size[0] + self.listbox_margin))
        self.set_label_color(self.artist_label)
        self.artist_listbox = wx.ListBox(self, choices=[], pos=self.get_pos_offset(height_off=20), size=listbox_size)
        self.artist_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_artist)
        self.set_listbox_color(self.artist_listbox)
        
        self.SetSize(wx.DisplaySize())
        self.SetTitle('My Spotify')
        self.SetBackgroundColour('black')
        self.Centre()
        self.Show(True)          

    def get_pos_offset(self, width_off=0, height_off=0):
        pos = (self.last_pos[0] + width_off, self.last_pos[1] + height_off)
        return pos

    def set_next_pos(self, width, height=0):
        pos = (width, height)
        self.last_pos = pos

    def get_next_pos(self, width, height=0):
        pos = (self.last_pos[0] + width, self.last_pos[1] + height)
        self.last_pos = pos
        return pos

    def get_listbox_size(self):
        width = wx.DisplaySize()[0]
        width -= (self.listbox_margin*4)
        width /= self.listbox_count
        height = wx.DisplaySize()[1]
        top = 150
        bottom = 50
        height -= (top + bottom)
        return (width,height)

    def set_listbox_color(self, label):
        label.SetForegroundColour('black')
        label.SetBackgroundColour('white')

    def set_playing_label_color(self, label):
        label.SetForegroundColour('blue')
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        label.SetFont(font)

    def set_label_color(self, label):
        label.SetForegroundColour('yellow')
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        label.SetFont(font)

    def show_results(self, search):
        self.show_tracks(search)
        self.show_albums(search)
        self.show_artists(search)

    def get_queue(self, listbox, dic):
        queue = []
        for s in range(0, listbox.GetCount()):
            if(s == wx.NOT_FOUND):
                print "not found"
                return s
            name = listbox.GetString(s)
            queue.append(dic[name])
        return queue

    def get_selection(self, listbox, dic):
        select = listbox.GetSelection()
        if(select == wx.NOT_FOUND):
            print "not found"
            return select
        name = listbox.GetString(select)
        return dic[name]

    def load_selections(self, listbox, selections):
        selections.reverse()
        for selection in selections:
            listbox.Insert(selection, 0)

    def clear(self, lb):
        leng = lb.GetCount()
        for index in range(0, leng):
            lb.Delete(0) 

    def clear_tracks(self):
        self.clear(self.listbox)
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
        self.clear_tracks()
        self.load_selections(self.listbox, track_names)
    def display_track(self, evt):
        track = evt.GetValue()
        self.playing_label.SetLabel("Track: " + track.name)

    def clear_albums(self):
        self.clear(self.album_listbox)
    def show_albums(self, search):
        albums_names = []
        self.albums = {}
        for album in search.albums:
            if(album.name not in albums_names):
                albums_names.append(album.name)
                self.albums[album.name] = album
        self.clear_albums()
        self.load_selections(self.album_listbox, albums_names)

    def clear_artists(self):
        self.clear(self.artist_listbox)
    def show_artists(self, search):
        artists_names = []
        self.artists = {}
        for artist in search.artists:
            if(artist.name not in artists_names):
                artists_names.append(artist.name)
                self.artists[artist.name] = artist
        self.clear_artists()
        self.load_selections(self.artist_listbox, artists_names)

    def browse_artist(self, e):
        artist = self.get_selection(self.artist_listbox, self.artists)
        if(artist != wx.NOT_FOUND):
            browser = self.player.browse_artist(artist.link.uri)
            self.show_albums(browser)

    def browse_album(self, e):
        album = self.get_selection(self.album_listbox, self.albums)
        if(album != wx.NOT_FOUND):
            browser = self.player.browse_album(album.link.uri)
            self.show_tracks(browser)

    def play_track(self,e):
        track = self.get_selection(self.listbox, self.tracks)
        if(track != wx.NOT_FOUND):
            self.player.set_queue(self.get_queue(self.listbox, self.tracks))
            self.player.set_index(self.listbox.GetSelection())
            self.player.play_track(track)
            self.btn.SetLabel("Pause")

    def play_next(self, e):
        self.player.set_next_flag()
    def play_prev(self, e):
        self.player.set_prev_flag()

    def search(self, e):
        if(e.GetKeyCode() == wx.WXK_RETURN):
            search = self.player.search(self.searchText.GetLineText(0))
            self.show_results(search)

    def play(self, e):
        if(self.btn.GetLabel() == "Play"):
            self.player.play()
            self.btn.SetLabel("Pause")
        else:
            self.player.pause()
            self.btn.SetLabel("Play")

    def pause(self, e):
        self.player.pause()

    def stop(self, e):
        self.btn.SetLabel("Play")
        self.player.stop()

    def OnCloseWindow(self, e):
        self.player.close()
        self.Destroy()
