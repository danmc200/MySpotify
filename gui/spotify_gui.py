import wx
import gui_util, my_events

class SpotifyGUI(wx.Frame):

    def __init__(self, *args, **kw):
        super(SpotifyGUI, self).__init__(*args, **kw) 
        
    def init_gui(self, player):
        self.player = player
        pnl = wx.Panel(self)
        builder = gui_util.GuiBuilder()
        self.util = gui_util.ListboxUtil()
        search_size = 180
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(my_events.EVT_DISPLAY_TRACK, self.display_track)

        self.searchText = wx.TextCtrl(self, -1, "", pos=builder.get_next_pos(0), size=(search_size, -1))
        self.searchText.SetInsertionPoint(0)
        self.searchText.SetFocus()
        self.searchText.Bind(wx.EVT_KEY_UP, self.search)

        self.btn = wx.Button(self, label='Play', pos=builder.get_next_pos(search_size+10))
        self.btn.Bind(wx.EVT_BUTTON, self.play)

        btn2 = wx.Button(self, label='Stop', pos=builder.get_next_pos(100))
        btn2.Bind(wx.EVT_BUTTON, self.stop)

        self.playing_label = wx.StaticText(self, label="Track: ", pos=(20, 45))
        builder.set_playing_label_color(self.playing_label)

        builder.set_next_pos(20, 70)
        btn3 = wx.Button(self, label='Prev', pos=builder.get_next_pos(0))
        btn3.Bind(wx.EVT_BUTTON, self.play_prev)

        btn4 = wx.Button(self, label='Next', pos=builder.get_next_pos(100))
        btn4.Bind(wx.EVT_BUTTON, self.play_next)

        builder.set_next_pos(20, 110)
        listbox_size = builder.get_listbox_size()
        self.tracks_label = wx.StaticText(self, label="Tracks:", pos=builder.get_next_pos(0))
        builder.set_label_color(self.tracks_label)
        self.listbox = wx.ListBox(self, choices=[], pos=builder.get_pos_offset(height_off=20), size=listbox_size)
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.play_track)
        builder.set_listbox_color(self.listbox)

        self.album_label = wx.StaticText(self, label="Albums:", pos=builder.get_next_pos(listbox_size[0] + builder.get_listbox_margin()))
        builder.set_label_color(self.album_label)
        self.album_listbox = wx.ListBox(self, choices=[], pos=builder.get_pos_offset(height_off=20), size=listbox_size)
        self.album_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_album)
        builder.set_listbox_color(self.album_listbox)

        self.artist_label = wx.StaticText(self, label="Artists:", pos=builder.get_next_pos(listbox_size[0] + builder.get_listbox_margin()))
        builder.set_label_color(self.artist_label)
        self.artist_listbox = wx.ListBox(self, choices=[], pos=builder.get_pos_offset(height_off=20), size=listbox_size)
        self.artist_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.browse_artist)
        builder.set_listbox_color(self.artist_listbox)
        
        self.SetSize(wx.DisplaySize())
        self.SetTitle('My Spotify')
        self.SetBackgroundColour('black')
        self.Centre()
        self.Show(True)          

    def show_results(self, search):
        self.util.show_tracks(search, self.listbox)
        self.util.show_albums(search, self.album_listbox)
        self.util.show_artists(search, self.artist_listbox)

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

    def display_track(self, evt):
        track = evt.GetValue()
        self.playing_label.SetLabel("Track: " + track.name)

    def browse_artist(self, e):
        artist = self.get_selection(self.artist_listbox, self.util.artists)
        if(artist != wx.NOT_FOUND):
            browser = self.player.browse_artist(artist.link.uri)
            self.util.show_albums(browser, self.album_listbox)

    def browse_album(self, e):
        album = self.get_selection(self.album_listbox, self.util.albums)
        if(album != wx.NOT_FOUND):
            browser = self.player.browse_album(album.link.uri)
            self.util.show_tracks(browser, self.listbox)

    def search(self, e):
        if(e.GetKeyCode() == wx.WXK_RETURN):
            search = self.player.search(self.searchText.GetLineText(0))
            self.show_results(search)

    def play_track(self,e):
        track = self.get_selection(self.listbox, self.util.tracks)
        if(track != wx.NOT_FOUND):
            self.player.set_queue(self.util.queue)
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
