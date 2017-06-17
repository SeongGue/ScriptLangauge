import datetime
from tkinter import*
from tkinter import font
from TourMapClass import*
from TourAPIClass import*

from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk

class TkUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("400x600")

    def InitLabel(self, labelText, xPos, yPos, fontData):
        label = Label(self.window, text=labelText, font=fontData)
        label.place(x=xPos, y=yPos)

    def InitButton(self, buttonText, func, xPos, yPos, fontData):
        button = Button(self.window, text = buttonText, font=fontData, command = func)
        button.place(x=xPos, y=yPos)

    def Initimage(self, image_name, xPos, yPos):
        img = PhotoImage(file=image_name)
        lbl = Label(image=img)
        lbl.image = img  # 레퍼런스 추가
        lbl.place(x=xPos, y=yPos)

    def InitListBox(self, width, height, xPos, yPos, fontData, scroll_bar):
        listBox = Listbox(self.window, font=fontData, activestyle='none', width=width, height=height, borderwidth=12,
                                relief='ridge', yscrollcommand=scroll_bar)

        listBox.pack()
        listBox.place(x=xPos, y=yPos)
        return listBox

    def InitScrollbar(self, xPos, yPos):
        scroll_bar = Scrollbar(self.window)
        scroll_bar.pack()
        scroll_bar.place(x=xPos, y=yPos)

        return scroll_bar

    def InitURLImage(self, width, height, xPos, yPos, URL):
        # openapi로 이미지 url을 가져옴.
        with urllib.request.urlopen(URL) as u:
            raw_data = u.read()

        im = Image.open(BytesIO(raw_data))
        resized = im.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(resized)

        lbl = Label(image=image)
        lbl.image = image  # 레퍼런스 추가

        lbl.place(x=xPos, y=yPos)

    def InitEntry(self, width, height, xPos, yPos, fontData):
        entry = Entry(self.window, font=fontData, width=width, borderwidth = 12, relief='ridge')
        #entry.pack()
        entry.place(x=xPos, y=yPos)

        return entry