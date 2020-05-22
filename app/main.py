from view import PdfProtectFrame
from controller import Controller
from model import Model
import wx
import constants

def main():
    app = wx.App()
    frame = PdfProtectFrame(None, title=constants.TITLE)
    controller = Controller(frame, Model())
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
