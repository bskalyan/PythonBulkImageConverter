# mass image converter app
# Designed to take a bunch of images in one format
# and convert them into another format.
# relatively simple if you use PIL.

import wx
from PIL import Image
import os

class MyMenu(wx.Frame):
    # redo.
    # single image converter. 
    # select one file, convert one file.
    # extend it to accept multiple files later.
    # start with the interface.
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        valid_targets = ["jpg", "gif", "pcx", 
            "msp", "png", "ppm", "tiff"]

        # time for a redesign!
        # Cheap Image Converter v .1
        # File to convert: [            ] <Select File>
        # Convert to: [.jpg]v 
        # [CONVERT]

        self.convert_target = None
        self.raw_file = None

        self.panel = wx.Panel(self, -1)

        # all elements will be declared in the order in which
        # they appear, top to bottom, left to right.
        self.intro_text = wx.StaticText(self.panel, -1, "Image Converter v 0.1")

        # Load files button and binding
        self.file_convert_text = wx.StaticText(self.panel, -1, 
            "Select a file to convert.")
        self.file_text_box = wx.TextCtrl(self.panel, -1,
            "Select a file to get started!", style=wx.TE_READONLY)
        self.load_file_button = wx.Button(self.panel, -1, "Load Files")
        self.load_file_button.Bind(wx.EVT_BUTTON, self.SelectFileDialog)

        # Conversion type selection box and label
        self.choice_list_desc = wx.StaticText(self.panel, -1, 
            "Select format to convert to: ")
        self.choice_list = wx.Choice(self.panel, -1, 
            choices=valid_targets)
        self.choice_list.Bind(wx.EVT_CHOICE, 
            self.SelectFromChoice)

        # Convert button!
        self.go_button = wx.Button(self.panel, -1, "Convert!")
        self.go_button.Bind(wx.EVT_BUTTON, self.PerformConversion)

        # Sizers, bitch.
        self.master_container = wx.BoxSizer(wx.VERTICAL)
        self.top_row = wx.BoxSizer(wx.HORIZONTAL)
        self.mid_row = wx.BoxSizer(wx.HORIZONTAL)
        self.mid_row2 = wx.BoxSizer(wx.HORIZONTAL)
        self.bot_row = wx.BoxSizer(wx.HORIZONTAL)

        self.top_row.Add(self.intro_text, 1, wx.ALIGN_LEFT, wx.EXPAND) 

        self.mid_row.Add(self.file_convert_text, 1, wx.ALIGN_RIGHT)
        self.mid_row.Add(self.file_text_box, 1, wx.ALIGN_RIGHT)
        self.mid_row.Add(self.load_file_button, 1, wx.ALIGN_LEFT)

        self.mid_row2.Add(self.choice_list_desc, 1, wx.ALIGN_LEFT)
        self.mid_row2.Add(self.choice_list, 1, wx.ALIGN_LEFT)

        self.bot_row.Add(self.go_button, 0, wx.ALIGN_CENTER)

        self.master_container.Add(self.top_row, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.master_container.Add(self.mid_row, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.master_container.Add(self.mid_row2, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.master_container.Add(self.bot_row, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=10)

        self.panel.SetSizer(self.master_container)

    def UtilityInfoDialog(self, text, title):
        msg = wx.MessageDialog(self, text, title, style=wx.OK | wx.ICON_INFORMATION)
        msg.ShowModal()
        msg.Destroy()

    def PerformConversion(self, event):
        # this probably isn't necessary, but just in case...
        if not self.raw_file: 
            self.UtilityInfoDialog(
                "Need to select files and a type to convert to before hitting the convert button!",
                "Error!")
        elif not self.convert_target:
            self.UtilityInfoDialog(
                "Select a file to convert before hitting the convert button!",
                "Error!")
        else:
            self.ConvertImage(self.raw_file, self.convert_target)

    def SelectFileDialog(self, event):
        dialog = wx.FileDialog(self, message="Select Files", defaultDir=os.getcwd(),
                           defaultFile="", style=wx.OPEN | wx.CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            self.raw_file = dialog.GetPath()
            if self.raw_file:
                self.file_text_box.SetValue(self.raw_file)
            else: 
                self.UtilityInfoDialog("File could not be loaded for some reason!",
                    "Error!")
        # i dont remember what this one is for.
            dialog.Destroy()

    def SelectFromChoice(self, event):
        self.convert_target = event.GetString()

    def ConvertImage(self, image, convert_to):
        """ Takes two arguments, first is a path to the image you wish to convert,
        while the second is the extension that you wish to convert to. Saves the new file to
        disk at the same filepath (albeit with a different extension) but the function 
        itself returns nothing.

        Uses PIL.Image to do the conversions, and supports bmp, gif, jpg, msp, pcx,
        png, ppm, tiff and xbm. """
        if os.path.splitext(image)[1].lower() == convert_to.lower():
            self.UtilityInfoDialog("%s is already of filetype %s" % (x, convert_to), "Error")
        else:
            Image.open(image).save("%s-%s.%s" % (os.path.splitext(image)[0], convert_to, convert_to))
            self.UtilityInfoDialog("Image conversion successful. Check source directory for new file.", 
                "Success!")

class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, 'Python Bulk Image Converter')
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
