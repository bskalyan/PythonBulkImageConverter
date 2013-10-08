# mass image converter app
# Designed to take a bunch of images in one format
# and convert them into another format.
# relatively simple if you use PIL.

import wx
from PIL import Image
import os
# I'm really tired of seeing these stupid PEP8 errors in NinjaIDE
# I don't know how to disable them, so I'm hacking up my code and rewriting
# stuff to make the stupid fucking yellow highlights disappear.


class MyMenu(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(640, 480))

        self.convert_target = None
        self.files_to_convert = []

        self.panel = wx.Panel(self, -1)

        # Load files button and binding
        self.Button1 = wx.Button(self.panel, -1, "Load Files")
        self.Button1.Bind(wx.EVT_BUTTON, self.SelectFileDialog)

        # Conversion type selection box label
        # Tired of seeing these "Line too long errors" need to fix them.
        self.choice_list_desc = wx.StaticText(self.panel, -1, "Select format to convert to: ")

        # Conversion type selection box and binding
        self.choice_list = wx.Choice(self.panel, -1, choices=[".jpg", ".gif", ".pcx", ".msp",
                                                ".pcx", ".png", ".ppm", ".tiff"])
        self.choice_list.Bind(wx.EVT_CHOICE, self.SelectFromChoice)

        # TextCtrl that'll display the list of files that you've selected
        # Note: use .SetValue() to change the value of TextCtrl
        self.text_box_desc = wx.StaticText(self.panel, -1, "Files to convert:")
        self.text_box = wx.TextCtrl(self.panel, -1,
                        "Select filetype to convert to, and then click Load Files.",
                        style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.go_button = wx.Button(self.panel, -1, "Convert!")
        self.go_button.Bind(wx.EVT_BUTTON, self.PerformConversion)

        # Sizers, bitch.
        self.master_container = wx.BoxSizer(wx.VERTICAL)

        self.top_row = wx.BoxSizer(wx.HORIZONTAL)
        self.top_row.Add(self.Button1, 1, wx.ALIGN_CENTER)
        self.top_row.Add(self.choice_list_desc, 0, wx.ALIGN_CENTER)
        self.top_row.Add(self.choice_list, 1, wx.ALIGN_CENTER)

        self.mid_row = wx.BoxSizer(wx.VERTICAL)
        self.mid_row.Add(self.text_box_desc, 0, wx.ALIGN_LEFT, border=5)
        self.mid_row.Add(self.text_box, 1, wx.EXPAND | wx.ALL)

        self.bot_row = wx.BoxSizer(wx.HORIZONTAL)
        self.bot_row.Add(self.go_button, 1, wx.EXPAND)

        self.master_container.Add(self.top_row, 0, wx.EXPAND | wx.ALL)
        self.master_container.Add(self.mid_row, 1, wx.EXPAND | wx.ALL)
        self.master_container.Add(self.bot_row, 0, wx.EXPAND | wx.ALL)

        self.panel.SetSizer(self.master_container)

    # simple utility function so I don't have to write three lines of code
    # every time I write a dialog call.

    def UtilityInfoDialog(self, text, title):
        msg = wx.MessageDialog(self, text, title, style=wx.OK | wx.ICON_INFORMATION)
        msg.ShowModal()
        msg.Destroy()

    def UpdateTextCtrl(self):
        self.text_box.Clear()
        for x in self.files_to_convert:
            self.text_box.AppendText(x + "\n")

    def PerformConversion(self, event):
        # this probably isn't necessary, but just in case...
        if len(self.files_to_convert) == 0 or self.convert_target is None:
            self.UtilityInfoDialog(
                "Need to select files and a type to convert to before hitting the convert button!",
                "Error!")
        else:
            self.ConvertBulkImages(self.files_to_convert, self.convert_target)

    def SelectFileDialog(self, event):
        if self.convert_target is None:
            error_msg = "Select type to convert to before loading files!"
            self.UtilityInfoDialog(error_msg, "Error!")
        else:
            dialog = wx.FileDialog(self, message="Select Files", defaultDir=os.getcwd(),
                               defaultFile="", style=wx.OPEN | wx.CHANGE_DIR | wx.MULTIPLE)
            if dialog.ShowModal() == wx.ID_OK:
                for x in dialog.GetPaths():
                    self.files_to_convert.append(x)
                for x in self.files_to_convert:
                    print x
                    self.text_box.AppendText(x + "\n")
                #self.ConvertBulkImages(dialog.GetPaths(), self.convert_target)
            self.UpdateTextCtrl()
            dialog.Destroy()

    def SelectFromChoice(self, event):
        self.convert_target = event.GetString()

    def ConvertBulkImages(self, list_of_imgs, convert_to):
        """ Takes two arguments, first is a list of filepaths to images including the extension
        while the second is the extension that you wish to convert to.

        Example usage: ConvertBulkImages(["C://foo.bmp","C://bar.bmp",], ".jpg")

        Uses PIL.Image to do the conversions, and supports bmp, gif, jpg, msp, pcx,
        png, ppm, tiff and xbm. """
        counter = 0
        for x in list_of_imgs:
            if os.path.splitext(x)[1].lower() == convert_to.lower():
                self.UtilityInfoDialog("%s is already of filetype %s" % (x, convert_to), "Error")
                continue

            else:
                Image.open(x).save(os.path.splitext(x)[0] + convert_to)
                counter = counter + 1

        self.UtilityInfoDialog("Operation complete! %d files converted." % counter, "Op Success")


class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, 'Python Bulk Image Converter')
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
