from tkinter import *
import plist_time as pc

win = Tk()

Label(win, text="Playlist ID : ").grid(row=0, column=0)
id = Entry(win, width=75, borderwidth=5)
id.grid(row=1, column=0)

def onClick():
    pl = pc.plist(id.get())
    h, m = pl.calTime()
    Label(win, text="Hours : {} and Minutes : {}".format(h, m)).grid(row=3, column=0)

button = Button(win, text="Calculate", padx=50, command=onClick).grid(row=2, column=0)



win.mainloop()