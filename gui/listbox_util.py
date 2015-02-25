import wx

def clear(lb):
    leng = lb.GetCount()
    for index in range(0, leng):
        lb.Delete(0) 

def listbox_insert(listbox, selections):
    selections.reverse()
    for selection in selections:
        listbox.Insert(selection, 0)

def show(col, search_col, listbox, decorator=None):
    names = []
    for el in search_col:
        name = el.name
        if(decorator != None):
            name = decorator(el)
        if(name not in names):
            names.append(name)
            col.append(el)
    clear(listbox)
    listbox_insert(listbox, names)
    return col

def show_tracks(search, listbox, tracks, artist=True):
    decor = lambda track : track.name + " (" + track.artists[0].name + ")"
    tracks = []
    return show(tracks, search.tracks, listbox, decor)

def show_albums(search, album_listbox, albums):
    albums = []
    return show(albums, search.albums, album_listbox)

def show_artists(search, artist_listbox, artists):
    artists = []
    return show(artists, search.artists, artist_listbox)
