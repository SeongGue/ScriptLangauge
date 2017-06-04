from tkinter import *
from tkinter import font
import tkinter.messagebox
g_Tk = Tk()
g_Tk.title("나들이")
g_Tk.geometry("400x600+750+200")

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="<전국 행사정보 서비스>")
    MainText.pack()
    MainText.place(x=80)


def mainimage():
    img = PhotoImage(file='나들이.gif')
    lbl = Label(image=img)
    lbl.image = img  # 레퍼런스 추가
    lbl.place(x=0, y=0)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=80)
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',width=10, height=1, borderwidth=12, relief='ridge',yscrollcommand=ListBoxScrollbar.set)
    SearchListBox.insert(1, "지역 검색")
    SearchListBox.insert(2, "텍스트 검색")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=80)

InitTopText()
mainimage()
InitSearchListBox()
g_Tk.mainloop()