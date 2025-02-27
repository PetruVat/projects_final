import wx
from GUI.display import Application



def main():
    """Инициализация и запуск GUI-приложения."""
    app = wx.App()
    Application()
    app.MainLoop()

if __name__ == '__main__':
    main()