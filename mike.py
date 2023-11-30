import tkinter as tk

##make window##
window = tk.Tk()
window.geometry("800x500")
window.title("DisText")


##menu bar top##
MenuFrame = tk.Frame(window)
MenuFrame.place(x=0,y=0)
file = tk.Button(MenuFrame, text="File")
file.pack(side="left", padx=4)
Edit = tk.Button(MenuFrame, text="Edit")
Edit.pack(side="left", padx=4)
View = tk.Button(MenuFrame, text="View")
View.pack(side="left", padx=4)
Insert = tk.Button(MenuFrame, text="Insert")
Insert.pack(side="left", padx=4)

##comand box##
CMD = tk.Entry(window)
CMD.place(x=40,y=30, width=730)

##X cords##
XCords = tk.Frame(window)
XCords.place(x=64, y=64)

max_x = 28
max_y = 24

x = 1
while x != 29:
    if x < 10:
        x = f'0{x}'
    x1 = tk.Label(XCords,text=f'{x}', justify='center')
    x1.pack(side='left')
    x = int(x)
    x += 1

##Y cords##
YCords = tk.Frame(window)
YCords.place(x=48, y=80)
y = 1
while y != 25:
    y1 = tk.Label(YCords,text=f'{y}', justify='center')
    y1.pack(side='top')
    y += 1

##text box##
textbox = tk.Text(window, bg='light grey')
textbox.place(x=64, y=80)

def create_grid(event=None):
    w = c.winfo_width()
    h = c.winfo_height()
    c.delete('grid_lines')
    print(f"w is {w} and h is {h}")
    totalX = 0
    for i in range(0, w, int(w/max_x)):
        totalX += 1
        c.create_line([(i, 0), (i, h)], tag='grid_line')
    for i in range(0, h, int(h/max_y)):
        c.create_line([(0,i), (w, i)], tag='grid_lines')
    print(totalX)
c = tk.Canvas(textbox, width=500, height=500)
c.pack(fill=tk.BOTH)
c.bind('<Configure>', create_grid)
textbox.tkraise

window.mainloop()