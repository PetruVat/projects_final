import wx
from GUI.display import Application



def main():
    app = wx.App()
    Application()
    app.MainLoop()

if __name__ == '__main__':
    main()