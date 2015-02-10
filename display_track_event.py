import wx

myEVT_DISPLAY_TRACK = wx.NewEventType()
EVT_DISPLAY_TRACK = wx.PyEventBinder(myEVT_DISPLAY_TRACK, 1)
class DisplayTrackEvent(wx.PyCommandEvent):

    def __init__(self, etype, eid, value=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.value = value

    def GetValue(self):
        return self.value
