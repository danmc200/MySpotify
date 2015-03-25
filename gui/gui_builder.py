import wx

class Builder():

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
        label.SetForegroundColour('red')
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        label.SetFont(font)

