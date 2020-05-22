
import sys
import wx
import json
import constants

class PdfProtectFrame(wx.Frame):

    def __init__(self, parent, title):
        super(PdfProtectFrame, self).__init__(parent, title=title)

        self.panel = wx.Panel(self)
        self.statusbar = self.CreateStatusBar(1)

        self.in_fp = wx.FilePickerCtrl(self.panel, wildcard=constants.WILDCARD, size=(400,-1))
        self.in_fp.TextCtrl.SetEditable(False)

        self.out_fp = wx.FilePickerCtrl(self.panel, style=wx.FLP_SAVE | wx.FLP_USE_TEXTCTRL | wx.FLP_OVERWRITE_PROMPT , wildcard=constants.WILDCARD, size=(400,-1))
        self.out_fp.TextCtrl.SetEditable(False)

        self.protect_btn = wx.Button(self.panel, label=constants.LABEL_PROTECT)
        self.close_btn = wx.Button(self.panel, label=constants.LABEL_CLOSE)
        self.protect_btn.Disable()

        self.layout_ui()
        self.Centre()

    @property
    def in_path(self):
        return self.in_fp.GetPath()

    @in_path.setter
    def in_path(self, val):
        self.in_fp.SetPath(val)

    @property
    def out_path(self):
        return self.out_fp.GetPath()

    @out_path.setter
    def out_path(self, val):
        self.out_fp.SetPath(val)

    @property
    def status_text(self):
        return self.statusbar.GetValue()

    @status_text.setter
    def status_text(self, val):
        self.statusbar.SetStatusText(val)

    @property
    def protect_enabled(self):
        return self.protect_btn.IsEnabled()
    
    @protect_enabled.setter
    def protect_enabled(self, value):
        self.protect_btn.Enable() if value == True else self.protect_btn.Disable()

    def bind_file_changed(self, handler):
        self.in_fp.Bind(wx.EVT_FILEPICKER_CHANGED, handler)
        self.out_fp.Bind(wx.EVT_FILEPICKER_CHANGED, handler)

    def bind_close(self, handler):
        self.close_btn.Bind(wx.EVT_BUTTON, handler)

    def bind_protect(self, handler):
        self.protect_btn.Bind(wx.EVT_BUTTON, handler)
        
    def layout_file_picker(self, panel, text, fp, font):

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(panel, label=text, size=(60, -1))
        st.SetFont(font)
        hbox.Add(st, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        hbox.Add(fp, proportion=1)

        return hbox

    def layout_buttons(self, panel, protect_btn, close_btn):

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(protect_btn, flag=wx.RIGHT, border=8)
        hbox.Add(close_btn, flag=wx.RIGHT, border=8)

        return hbox

    def layout_ui(self):

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(self.layout_file_picker(self.panel, constants.LABEL_INPUT, self.in_fp, font), flag=wx.EXPAND |
                 wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        vbox.Add((-1, 10))

        vbox.Add(self.layout_file_picker(self.panel, constants.LABEL_OUTPUT, self.out_fp, font), flag=wx.EXPAND |
                 wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        vbox.Add((-1, 10))

        vbox.Add(self.layout_buttons(self.panel, self.protect_btn, self.close_btn), flag=wx.ALIGN_CENTER, border=5)
        vbox.Add((-1, 10))

        vbox.SetSizeHints(self)

        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(vbox)
        self.panel.Layout()

    def show_password_dialog(self, label):
        with wx.PasswordEntryDialog(self, label, style=wx.TextEntryDialogStyle) as pass_dialog:
            res = pass_dialog.ShowModal()
            if res == wx.ID_OK:
                return pass_dialog.GetValue()
            return None

    def show_message_dialog(self, message, style = wx.ICON_INFORMATION):
        with wx.MessageDialog(self, message, style=style) as message_dialog:
            res = message_dialog.ShowModal()

    def show_error_dialog(self, message):
        self.show_message_dialog(message, style=wx.ICON_ERROR | wx.OK)

    def clear(self):
        self.in_fp.SetPath("")
        self.out_fp.SetPath("")
        self.protect_btn.Disable()
        
