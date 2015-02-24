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

    def show(self, col, search_col, listbox, decorator=None):
        names = []
        for el in search_col:
            name = el.name
            if(decorator != None):
                name = decorator(el)
            if(name not in names):
                names.append(name)
                col.append(el)
        self.clear(listbox)
        self.listbox_insert(listbox, names)
        return col

    def show_tracks(self, search, listbox, artist=True):
        decor = lambda track : track.name + " (" + track.artists[0].name + ")"
        self.tracks = []
        self.tracks = self.show(self.tracks, search.tracks, listbox, decor)

    def show_albums(self, search, album_listbox):
        self.albums = []
        self.albums = self.show(self.albums, search.albums, album_listbox)

    def show_artists(self, search, artist_listbox):
        self.artists = []
        self. artists = self.show(self.artists, search.artists, artist_listbox)
