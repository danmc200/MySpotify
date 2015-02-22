import wx

class Util():

    def __init__(self):
        self.tracks = []
        self.albums = []
        self.artists = []

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
        self.tracks = []
        for track in search.tracks:
            track_name = track.name 
            if(artist):
                track_name += " (" + track.artists[0].name + ")"
            if(track_name not in track_names):
                track_names.append(track_name)
                self.tracks.append(track)
        self.clear_tracks(listbox)
        self.listbox_insert(listbox, track_names)
    def clear_tracks(self, listbox):
        self.clear(listbox)

    def show_albums(self, search, album_listbox):
        albums_names = []
        self.albums = []
        for album in search.albums:
            if(album.name not in albums_names):
                albums_names.append(album.name)
                self.albums.append(album)
        self.clear_albums(album_listbox)
        self.listbox_insert(album_listbox, albums_names)
    def clear_albums(self, album_listbox):
        self.clear(album_listbox)

    def show_artists(self, search, artist_listbox):
        artists_names = []
        self.artists = []
        for artist in search.artists:
            if(artist.name not in artists_names):
                artists_names.append(artist.name)
                self.artists.append(artist)
        self.clear_artists(artist_listbox)
        self.listbox_insert(artist_listbox, artists_names)
    def clear_artists(self, artist_listbox):
        self.clear(artist_listbox)
