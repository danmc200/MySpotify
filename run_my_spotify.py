#!/usr/bin/python
import wx
import gui.spotify_gui as spotify_gui
import core.audio_player as audio_player
import core.login as login

if __name__ == "__main__":
    app = wx.App()
    ui = spotify_gui.SpotifyGUI(None)

    session = login.get_session()
    player = audio_player.AudioPlayer(session, ui)
    un, pwd = login.get_username_password()
    login.login(session, un, pwd)

    ui.init_gui(player)
    app.MainLoop()
