import wx
import gui_util, my_events

class SpotifyGUI(wx.Frame):

    def __init__(self, *args, **kw):
        super(SpotifyGUI, self).__init__(*args, **kw) 
        
    def init_gui(self, player):
        self.player = player
        pnl = wx.Panel(self)
        util = gui_util.GuiUtil()
        search_size = 180
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(my_events.EVT_DISPLAY_TRACK, self.display_track)

        self.searchText = wx.TextCtrl(self, -1, "", pos=util.get_next_pos(0), size=(search_size, -1))
        self.searchText.SetInsertionPoint(0)
        self.searchText.SetFocus()
        self.searchText.Bind(wx.EVT_KEY_UP, self.search)

        self.btn = wx.Button(self, label='Play', pos=util.get_next_pos(search_size+10))
        self.btn.Bind(wx.EVT_BUTTON, self.play)

        btn2 = wx.Button(self, label='Stop', pos=util.get_next_pos(100))
        btn2.Bind(wx.EVT_BUTTON, self.stop)

        self.playing_label = wx.StaticText(self, label="Track: ", pos=(20, 45))
        util.set_playing_label_color(self.playing_label)

        util.set_next_pos(20, 70)
        btn3 = wx.Button(self, label='Prev', pos=util.get_next_pos(0))
        btn3.Bind(wx.EVT_BUTTON, self.play_prev)

        btn4 = wx.Button(self, label='Next', pos=util.get_next_pos(100))
        btn4.Bind(wx.EVT_BUTTON, self.play_next)

        util.set_next_pos(20, 110)
        listbox_size = util.get_listbox_size()
        self.tracks_label = wx.StaticText(self, label="Tracks:", pos=util.get_next_pos(0))
        util.set_label_color(self.tracks_label)
        self.listbox = wx.ListBox(self, choices=[], pos=util.get_pos_offset(height_off=20), size=listbox_size)
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.play_track)
        util.set_listbox_color(self.listbox)

        self.album_label = wx.StaticText(self, label="Albums:", pos=util.get_next_pos(listbox_size[0] + util.get_listbox_margin()))
        util.set_label_color(self.album_label)
        self.album_listbox = wx.ListBox(self, choices=[], pos=util.get_pos_offset(height_off=20), size=listbox_size)
        self.album_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_album)
        util.set_listbox_color(self.album_listbox)

        self.artist_label = wx.StaticText(self, label="Artists:", pos=util.get_next_pos(listbox_size[0] + util.get_listbox_margin()))
        util.set_label_color(self.artist_label)
        self.artist_listbox = wx.ListBox(self, choices=[], pos=util.get_pos_offset(height_off=20), size=listbox_size)
        self.artist_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_artist)
        util.set_listbox_color(self.artist_listbox)
        
        self.SetSize(wx.DisplaySize())
        self.SetTitle('My Spotify')
        self.SetBackgroundColour('black')
        self.Centre()
        self.Show(True)          

    def show_results(self, search):
        self.show_tracks(search)
        self.show_albums(search)
        self.show_artists(search)

    def build_queue(self, listbox, dic):
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

    def listbox_insert(self, listbox, selections):
        selections.reverse()
        for selection in selections:
            listbox.Insert(selection, 0)

    def clear(self, lb):
        leng = lb.GetCount()
        for index in range(0, leng):
            lb.Delete(0) 

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
        self.listbox_insert(self.listbox, track_names)
    def display_track(self, evt):
        track = evt.GetValue()
        self.playing_label.SetLabel("Track: " + track.name)
    def clear_tracks(self):
        self.clear(self.listbox)

    def show_albums(self, search):
        albums_names = []
        self.albums = {}
        for album in search.albums:
            if(album.name not in albums_names):
                albums_names.append(album.name)
                self.albums[album.name] = album
        self.clear_albums()
        self.listbox_insert(self.album_listbox, albums_names)
    def clear_albums(self):
        self.clear(self.album_listbox)

    def show_artists(self, search):
        artists_names = []
        self.artists = {}
        for artist in search.artists:
            if(artist.name not in artists_names):
                artists_names.append(artist.name)
                self.artists[artist.name] = artist
        self.clear_artists()
        self.listbox_insert(self.artist_listbox, artists_names)
    def clear_artists(self):
        self.clear(self.artist_listbox)

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

    def search(self, e):
        if(e.GetKeyCode() == wx.WXK_RETURN):
            search = self.player.search(self.searchText.GetLineText(0))
            self.show_results(search)

    def play_track(self,e):
        track = self.get_selection(self.listbox, self.tracks)
        if(track != wx.NOT_FOUND):
            self.player.set_queue(self.build_queue(self.listbox, self.tracks))
            index = self.listbox.GetSelection()
            self.player.play_track(index)
            self.btn.SetLabel("Pause")

    def play_next(self, e):
        self.player.set_index_offset(1)

    def play_prev(self, e):
        self.player.set_index_offset(-1)

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

    def post_track_event(self, track):
        evt = my_events.DisplayTrackEvent(my_events.myEVT_DISPLAY_TRACK, -1, track)
        wx.PostEvent(self, evt)

    def OnCloseWindow(self, e):
        self.player.close()
        self.Destroy()
