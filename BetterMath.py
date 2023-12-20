
from tkinter import *
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter.ttk import *
from PIL import Image,ImageTk
import math
import fitz # imports the pymupdf library
import time

## Default button bindings
infinite = "<Shift-i>"


##make window##
window = Tk()

style = Style(window)
#print(style.theme_names())
style.theme_use("winnative")
#style.configure("VisibleTextBox", borderwidth=3, background="#ce7e00")
#style.configure("HiddenTextBox", borderwidth=0)


screen_width= window.winfo_screenwidth()               
screen_height= window.winfo_screenheight()               
window.geometry("%dx%d" % (screen_width, screen_height))

window.title("DisText")
#Text(window, justify='center')



## Class Answer Grid, Stores all relevant data for a solution/ expression

class answerGrid:
    thickness = 20
    height =  40
    fontsize = 25
    row = 0
    col = 0
    
    def __init__(self, x1,y1,x2,y2):
        self.startx = min([x1,x2])
        self.starty = min([y1,y2])
        self.endx = max([x1,x2])
        self.endy = max([y1,y2])
        self.row = max(abs(math.floor((x1-x2)/self.thickness)),1)
        self.col = max(abs(math.floor((y1-y2)/self.height)),1)
        self.grid = [["" for i in range(self.col)] for j in range(self.row)]
        print(self.grid)

    #Capture and manage the keypress
    def key_press(self, event):
        print("ran")
        print(event.char)
        #take a look at some variables to maybe use for movement
        '''print(event.widget.__dict__)
            for x in self.grid:
                for y in x:
                    print(y.tk)'''
        print(event)
        #god forgive me for this yandere dev if elif nonsense. I hope i figure out a better situation at some point
        #movement section
        if event.char == "a":
            temp = event.widget
            for x in range(self.col):
                temp = temp.tk_focusPrev()
            temp.focus()
            return "break"
        elif event.char == "d":
            temp = event.widget
            for x in range(self.col):
                temp = temp.tk_focusNext()
            temp.focus()
            return "break"
        elif event.char == "s":
            event.widget.tk_focusNext().focus()
            return "break"
        elif event.char == "w":
            event.widget.tk_focusPrev().focus()
            return "break"
        #Deleting and other values section
        elif event.char == "\b":
            print("backspace")
        elif event.char == "":
            print("special character")
        elif event.char == '\x16': #ctrl + v
            event.widget.insert(INSERT, window.clipboard_get())
            return "break"
        #Symbols Section
        elif event.char == "P":
            event.widget.insert(INSERT, "𝝅")
            return "break"
        elif event.char == "R":
            event.widget.insert(INSERT, "√")
            return "break"
        elif event.char == '\x06':
            #print(event.widget.get("1.0",'end-1c'))
            original_input = event.widget.get('1.0','end-1c')
            event.widget.delete('1.0', END)
            event.widget.insert('1.0', f"\u0305{original_input}\u0305")
            #\u0305
            return "break"
        else:
            event.widget.insert(INSERT, f"{event.char}")
            temp = event.widget
            for x in range(self.col):
                temp = temp.tk_focusNext()
            temp.focus()
            return "break"
        #return "break" removes default behavior 
        #return "break"

    def draw(self,canvas):
        
        if abs(self.startx - self.endx) < self.thickness:
            self.row = 1
        if abs(self.starty - self.endy) < self.height:
            self.col = 1
        #if abs(self.startx - self.endx) > self.thickness and abs(self.starty-self.endy) > self.height:
        print("heyo", self.row, self.col)
        #aframe = Frame(canvas, bg="red")
        #aframe.place(x=self.startx, y=self.starty, width=self.fontsize*self.row , height=self.fontsize*self.col)
        for x in range(self.row):
            temp = NONE
            for y in range(self.col):
                temp = Text(canvas, height=1, width=1, padx=0, bg="white")
                self.grid[x][y] = temp 
                #print("im crying", self.grid[x][y])
                temp.tag_configure("center", justify='center')
                temp.tag_add("center", 1.0, "end")
                self.grid[x][y].config(font=('Arial', self.fontsize))
                #temp.configure(style="VisibleTextBox")
                #print(str(x),str(y))
                xcord = self.startx + (self.thickness*x)
                ycord = self.starty + (self.height*y)
                #self.grid[x][y].configure(yscrollcommand=scroll.set)
                canvas.create_window(xcord,ycord,window=self.grid[x][y],anchor=NW)
                self.grid[x][y].bind('<Key>', self.key_press)
                
                #self.grid[x][y].insert(END, f"{x},{y}") 
                #print("im crying2", self.grid[x][y])
                #self.grid[x][y].place(x=xcord, y=ycord)
                #print(x,y,"isfine")
            #print("im crying3", self.grid)
#test = Text(worksheet, height=1, width=3, bg="red")
#worksheet.create_window(10,10,window=test)
        #print(self.grid)



    #iterate through the grid and destroy the textboxes
    def delete_grid (self):
        #print(worksheet.__dict__)
        #print(self.grid[0][0])
        
        for x in range(self.row):
            for y in range(self.col):
                #print(x,y,"destroy")
                self.grid[x][y].destroy()
        
        #self.grid[0][0].destroy()
        #self.grid[1][1].destroy()
        #self.grid[2][0].destroy()
        #self.grid[1][0].destroy()
        
    def remove_borders(self):
        for x in range(self.row):
            for y in range(self.col):
                print(self.grid[x][y].__dict__)
                self.grid[x][y].configure(borderwidth=0)
                #self.grid[x][y].insert(END, f"{x},{y}") 
        #print("We removed the borders")
        
    def add_borders(self):
        for x in range(self.row):
            for y in range(self.col):
                self.grid[x][y].configure(borderwidth=2)


# Function for opening the 
# file explorer window
filename = "example.png"



## An array that holds all the grids so they can be referenced and deleted
stored_grids = []

def delete_last_grid():
    print("we ran")
    if len(stored_grids) > 0:
        stored_grids[0].delete_grid()
        stored_grids.pop(0)

#this exists to allow tkinter to update
def resize_for_save(canvas, frame):
    frame.config(height=1100)
    canvas.config(height=1100)
    for x in stored_grids:
        x.remove_borders()

    window.update()
#Stolen from the internet <3

def save_as_png(canvas, frame, fileName):
    # save postscipt image 
    save_as_filename = filedialog.asksaveasfilename(initialdir = "/")
    print(save_as_filename)
    canvas.postscript(file = fileName + '.eps') 
    
    frame.config(height=700)
    canvas.config(height=700)
    window.update()
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    
    img.save(save_as_filename + '.png', 'png') 
    





##menu bar top##
MenuFrame = Frame(window)
MenuFrame.place(x=0,y=0)
UndoBtn = Button(MenuFrame, text="Delete Last Grid", command=delete_last_grid)
UndoBtn.pack(side="left", padx=4)
OpenBtn = Button(MenuFrame, text="Open")
OpenBtn.pack(side="left", padx=4)
SaveBtn = Button(MenuFrame, text="Save", command= lambda: [resize_for_save(worksheet,work_area), save_as_png(worksheet,work_area,"sample")])
SaveBtn.pack(side="left", padx=4)
InsertBtn = Button(MenuFrame, text="Insert")
InsertBtn.pack(side="left", padx=4)

##comand box##
#Unclear on the functionality of this widget
#CMD = Entry(window)
#CMD.place(x=40,y=30, width=730)

##X cords##
#XCords = Frame(window)
#XCords.place(x=64, y=64)

#max_x = 28
#max_y = 24
'''
x = 1
while x != 29:
    if x < 10:
        x = f'0{x}'
    x1 = Label(XCords,text=f'{x}', justify='center')
    x1.pack(side='left')
    x = int(x)
    x += 1

##Y cords##
YCords = Frame(window)
YCords.place(x=48, y=80)
y = 1
while y != 25:
    y1 = Label(YCords,text=f'{y}', justify='center')
    y1.pack(side='top')
    y += 1
'''
#Work area for the worksheet 
work_w = 850
work_h = 700
image_w = 850
image_h = 1100

work_area = Frame(window, width=work_w , height=work_h)
work_area.place(x=int(work_w/3), y=100)

##Current Grid## 
#window.wm_attributes('-transparentcolor', '#ab23ff')


##Canvas for background image##
initial_worksheet = (Image.open(filename))
initial_worksheet=  initial_worksheet.resize((image_w,image_h),Image.LANCZOS)
worksheet_image = ImageTk.PhotoImage(initial_worksheet)


worksheet = Canvas(work_area, width=work_w , height=work_h,scroll='y', scrollregion=(0,0,0,image_h),  bg='green')
worksheet.place(x=0, y=0)
#work_frame = Frame(worksheet, bg="red")
#work_frame.place(x=0,y=0, width=work_w , height=work_h,)

worksheet.create_image(0,0,image=worksheet_image,anchor=NW)



scroll = Scrollbar(worksheet, orient = 'vertical', command=worksheet.yview)
scroll.place(relx=1, rely=0, relheight=1, anchor='ne')

worksheet.configure(yscrollcommand=scroll.set)
#create_page(30,39, worksheet)
##text box##
#textbox = Text(window, bg='light grey')
#textbox.place(x=64, y=80)


## Edit the canvas ##

#Function to create the working grid
upcomingZoneX = False
upcomingZoneY = False

def browseFiles(canvas):
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("JPG Image",
                                                        "*.jpg*"),
                                                       ("PDF",
                                                        "*.pdf*"),
                                                        ("PNG Image",
                                                        "*.png*")
                                                        )
                                            )
    initial_worksheet = (Image.open(filename))
    initial_worksheet=  initial_worksheet.resize((image_w,image_h),Image.BICUBIC)
    global worksheet_image
    worksheet_image= ImageTk.PhotoImage(initial_worksheet)
    canvas.create_image(0,0,image=worksheet_image,anchor=NW)
    #im = Image.open(r"D:\Ethan\Pictures\fuck around 2.png")
    #ph = ImageTk.PhotoImage(im)
    #canvas.create_image(0,0,image=ph,anchor=NW)
      
    # Change label contents
    #label_file_explorer.configure(text="File Opened: "+filename)

gridInsert = False
def toggle_grid_insert():
    global gridInsert
    print(gridInsert)
    gridInsert = not gridInsert 
    if gridInsert:
        InsertBtn.configure(text = "Stop Inserting")
    else:
        InsertBtn.configure(text = "Insert Grid")
    
    
    print(gridInsert)   


#This line helps while the file is a mess, clean up later
InsertBtn.configure(text = "Insert Grid", command=toggle_grid_insert)
OpenBtn.configure(command=lambda: browseFiles(worksheet))
def start_draw(event):
    global upcomingZoneX 
    global upcomingZoneY
    
    #upcomingZoneX = event.x
    upcomingZoneX  = worksheet.canvasx(event.x)
    #upcomingZoneY = event.y
    upcomingZoneY = worksheet.canvasy(event.y)


def draw(event):
    #print(event)
    color="red"
    x1,y1= (event.x-1), (event.y-1)
    x2,y2= (event.x), (event.y)
    #worksheet.create_oval(x1,y1,x2,y2,fill=color,outline=color)
    #print(worksheet.canvasx(event.x), worksheet.canvasy(event.y))

def end_draw(event):
    color="red"
    x1,y1 = upcomingZoneX, upcomingZoneY
    #x2,y2= (event.x), (event.y)
    x2,y2= worksheet.canvasx(event.x), worksheet.canvasy(event.y)
    #if abs(x1-x2) > 20 and abs(y1-y2) > 20:
        #worksheet.create_rectangle(x1,y1,x2,y2, fill=color,outline=color)
    if gridInsert:
        temp = answerGrid(x1,y1,x2,y2)
        stored_grids.insert(0,temp)
        temp.draw(worksheet)

worksheet.bind('<Button-1>', start_draw)
worksheet.bind('<B1-Motion>', draw)
worksheet.bind('<ButtonRelease-1>', end_draw)


#Useful Grid Code for future reference
''' 
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
c = Canvas(textbox, width=500, height=500)
c.pack(fill=BOTH)
c.bind('<Configure>', create_grid)
textbox.tkraise
'''
#A failed test to see if a frame would help
#w = Frame(worksheet)
#w.place(x = 10, y = 10, height = 40, width = 40)
#for x in range(4):
#    for y in range(4):
#        temp = Text(w, height=10, width=10, bg="white")
#        xcord = 0+10*x
#        ycord = 0+10*y
#        temp.place(x=xcord, y=ycord)

window.mainloop()



doc = fitz.open(filename) # open a document
for page in doc: # iterate the document pages
  text = page.get_text() # get plain text encoded as UTF-8
print(text)
