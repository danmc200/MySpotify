import wx

class GuiBuilder():

    def __init__(self):
        self.last_pos = [20, 10]
        self.listbox_margin = 20
        self.listbox_count = 3

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

    def get_listbox_margin(self):
        return self.listbox_margin

    def get_listbox_size(self):
        width = wx.DisplaySize()[0]
        width -= (self.listbox_margin*4)
        width /= self.listbox_count
        height = wx.DisplaySize()[1]
        top = 180
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

class ListboxUtil():

    def __init__(self):
        self.tracks = {}
        self.albums = {}
        self.artists = {}

    def clear(self, lb):
        leng = lb.GetCount()
        for index in range(0, leng):
            lb.Delete(0) 

    def listbox_insert(self, listbox, selections):
        selections.reverse()
        for selection in selections:
            listbox.Insert(selection, 0)

    def show_tracks(self, search, listbox, artist=True):
        track_names = []
        self.tracks = {}
        for track in search.tracks:
            track_name = track.name 
            if(artist):
                track_name += " (" + track.artists[0].name + ")"
            if(track_name not in track_names):
                track_names.append(track_name)
                self.tracks[track_name] = track
        self.clear_tracks(listbox)
        self.listbox_insert(listbox, track_names)
    def clear_tracks(self, listbox):
        self.clear(listbox)

    def show_albums(self, search, album_listbox):
        albums_names = []
        self.albums = {}
        for album in search.albums:
            if(album.name not in albums_names):
                albums_names.append(album.name)
                self.albums[album.name] = album
        self.clear_albums(album_listbox)
        self.listbox_insert(album_listbox, albums_names)
    def clear_albums(self, album_listbox):
        self.clear(album_listbox)

    def show_artists(self, search, artist_listbox):
        artists_names = []
        self.artists = {}
        for artist in search.artists:
            if(artist.name not in artists_names):
                artists_names.append(artist.name)
                self.artists[artist.name] = artist
        self.clear_artists(artist_listbox)
        self.listbox_insert(artist_listbox, artists_names)
    def clear_artists(self, artist_listbox):
        self.clear(artist_listbox)
