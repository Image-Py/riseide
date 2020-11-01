import wx

def make_logo(obj):
    bmp = None
    if isinstance(obj, str) and len(obj)>1:
        bmp = wx.Bitmap(obj)
    if isinstance(obj, str) and len(obj)==1:
        bmp = wx.Bitmap(16, 16)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        dc.SetTextForeground((0,0,150))
        font = dc.GetFont()
        font.SetPointSize(12)
        dc.SetFont(font)
        w, h = dc.GetTextExtent(obj)
        dc.DrawText(obj, 8-w//2, 8-h//2)
        rgb = bytes(768)
        dc.SelectObject(wx.NullBitmap)
        bmp.CopyToBuffer(rgb)
        a = memoryview(rgb[::3]).tolist()
        a = bytes([255-i for i in a])
        bmp = wx.Bitmap.FromBufferAndAlpha(16, 16, rgb, a)
    img = bmp.ConvertToImage()
    img.Resize((20,20), (2,2))
    return img.ConvertToBitmap()

class ToolBar(wx.aui.AuiToolBar):
    def __init__(self, parent, vertical=False):
        self.app = parent
        wx.aui.AuiToolBar.__init__( self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_TB_HORZ_LAYOUT )

    def on_tool(self, evt, tol):
        tol.start(self.app)
        # evt.Skip()
        btn = evt.GetEventObject()
        #print(self.GetBackgroundColour())
        #print(btn.GetClassDefaultAttributes().colFg)
        if not self.curbtn is None:
            self.curbtn.SetBackgroundColour(self.GetBackgroundColour())
        self.curbtn = btn
        btn.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )

    def on_config(self, evt, tol):
        if not hasattr(tol, 'view'): return
        self.app.show_para(tol.title, tol.para, tol.view)
        tol.config()

    def on_help(self, evt, tol): pass

    def on_info(self, event, tol): 
        self.app.info(tol.title)

    def bind(self, btn, tol):
        # obj = tol()
        self.Bind( wx.EVT_MENU, lambda e, obj=tol: obj().start(self.app), id=btn.GetId())
        #btn.Bind( wx.EVT_RIGHT_DOWN, lambda e, obj=obj: self.on_help(e, obj))
        #btn.Bind( wx.EVT_ENTER_WINDOW, lambda e, obj=obj: self.on_info(e, obj))
        #if not isinstance(data[0], Macros) and issubclass(data[0], Tool):
        #btn.Bind(wx.EVT_LEFT_DCLICK, lambda e, obj=obj: self.on_config(e, obj))

    def clear(self):
        del self.toolset[:]
        self.GetSizer().Clear()
        self.DestroyChildren()

    def add_tool(self, logo, tool):
        btn = self.AddTool( wx.ID_ANY, u"tool", wx.Bitmap(logo), #make_logo(logo), 
            wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.bind(btn, tool)
        self.Realize()
        

    def add_tools(self, name, tools):
        for logo, tool in tools: self.add_tool(logo, tool)     
        
if __name__ == '__main__':
    path = 'C:/Users/54631/Documents/projects/imagepy/imagepy/tools/drop.gif'
    app = wx.App()
    frame = wx.Frame(None)
    tool = ToolBar(frame, vertical=True)
    path = 'C:/Users/54631/Documents/projects/imagepy2/fucai/imgs/_help.png'
    tool.add_tools('A', [('A', None)] * 3)
    tool.add_tools('B', [('B', None)] * 3)
    tool.add_tools('C', [('C', None)] * 3)
    tool.Fit()
    frame.Fit()
    frame.Show()
    app.MainLoop()