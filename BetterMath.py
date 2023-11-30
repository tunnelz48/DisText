import fitz # imports the pymupdf library
import tkinter as tk
from PIL import Image,ImageTk
import math



## Class Answer Grid, Stores all relevant data for a solution/ expression

class answerGrid:
    thickness = 64
    height =  48
    fontsize = 30
    row = 0
    col = 0
    
    def __init__(self, x1,y1,x2,y2):
        self.startx = min([x1,x2])
        self.starty = min([y1,y2])
        self.endx = max([x1,x2])
        self.endy = max([y1,y2])
        self.row = max(abs(math.floor((x1-x2)/self.thickness)),1)
        self.col = max(abs(math.floor((y1-y2)/self.height)),1)
        self.grid = [[""] * self.col] * self.row
        #print(self.grid)

    def draw(self,canvas):
        
        if abs(self.startx - self.endx) < self.thickness:
            self.row = 1
        if abs(self.starty - self.endy) < self.height:
            self.col = 1
        #if abs(self.startx - self.endx) > self.thickness and abs(self.starty-self.endy) > self.height:
        print("heyo", self.row, self.col)
        #aframe = tk.Frame(canvas, bg="red")
        #aframe.place(x=self.startx, y=self.starty, width=self.fontsize*self.row , height=self.fontsize*self.col)
        for x in range(self.row):
            for y in range(self.col):
                self.grid[x][y] = tk.Text(canvas, height=1, width=3, bg="white")
                self.grid[x][y].config(font=('Arial', self.fontsize))
                #print(str(x),str(y))
                xcord = self.startx + (self.thickness*x)
                ycord = self.starty + (self.height*y)
                #self.grid[x][y].configure(yscrollcommand=scroll.set)
                canvas.create_window(xcord,ycord,window=self.grid[x][y],anchor=tk.NW)
                self.grid[x][y].insert(tk.END, f"{x},{y}") 
                #self.grid[x][y].place(x=xcord, y=ycord)
                #print(x,y,"isfine")
#test = tk.Text(worksheet, height=1, width=3, bg="red")
#worksheet.create_window(10,10,window=test)

    
    #iterate through the grid and destroy the textboxes
    def delete_grid (self):
        print(self.grid[0][0])
        
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                print(x,y,"destroy")
                self.grid[x][y].destroy()
        
        self.grid[0][0].destroy()
        #self.grid[1][1].destroy()
        #self.grid[2][0].destroy()
        #self.grid[1][0].destroy()
        
        


## An array that holds all the grids so they can be referenced and deleted
stored_grids = []

def delete_last_grid():
    print("we ran")
    if len(stored_grids) > 0:
        stored_grids[0].delete_grid()
        stored_grids.pop(0)

##make window##
window = tk.Tk()

screen_width= window.winfo_screenwidth()               
screen_height= window.winfo_screenheight()               
window.geometry("%dx%d" % (screen_width, screen_height))

window.title("DisText")



#Stolen from the internet <3

def save_as_png(canvas,fileName):
    # save postscipt image 
    print("something worked")
    canvas.postscript(file = fileName + '.eps') 
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    img.save(fileName + '.png', 'png') 
    





##menu bar top##
MenuFrame = tk.Frame(window)
MenuFrame.place(x=0,y=0)
file = tk.Button(MenuFrame, text="Delete Last Grid", command=delete_last_grid)
file.pack(side="left", padx=4)
Edit = tk.Button(MenuFrame, text="Edit")
Edit.pack(side="left", padx=4)
View = tk.Button(MenuFrame, text="Save", command= lambda: save_as_png(worksheet,"sample"))
View.pack(side="left", padx=4)
Insert = tk.Button(MenuFrame, text="Insert", command="drawZone")
Insert.pack(side="left", padx=4)

##comand box##
#Unclear on the functionality of this widget
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

#Work area for the worksheet 
work_w = 850
work_h = 700
image_w = 850
image_h = 1100

work_area = tk.Frame(window, width=work_w , height=work_h, bg='red')
work_area.place(x=int(work_w/3), y=100)

##Current Grid## 
#window.wm_attributes('-transparentcolor', '#ab23ff')

def create_page(x,y,canvas):
  #Starting with a 20x30 grid and adjusting later
  '''work_w = 850
     work_h = 700'''
  boxes_x = x
  boxes_y = y
  canvas = canvas
  box_width = int((image_w) / boxes_x)
  box_height = int(image_h / boxes_y)

  for i in range(0, image_w, box_width):
      canvas.create_line([(i, 0), (i, image_h)],dash = (1, 200), tag='grid_line')
      print(i)
  for i in range(0, image_h, box_height):
      canvas.create_line([(0,i), (image_w, i)], tag='grid_lines')





##Canvas for background image##
initial_worksheet = (Image.open("example.png"))
initial_worksheet=  initial_worksheet.resize((image_w,image_h),Image.LANCZOS)
worksheet_image = ImageTk.PhotoImage(initial_worksheet)


worksheet = tk.Canvas(work_area, width=work_w , height=work_h,scroll='y', scrollregion=(0,0,0,image_h),  bg='green')
worksheet.place(x=0, y=0)
#work_frame = tk.Frame(worksheet, bg="red")
#work_frame.place(x=0,y=0, width=work_w , height=work_h,)

worksheet.create_image(0,0,image=worksheet_image,anchor=tk.NW)



scroll = tk.Scrollbar(worksheet, orient = 'vertical', command=worksheet.yview)
scroll.place(relx=1, rely=0, relheight=1, anchor='ne')

worksheet.configure(yscrollcommand=scroll.set)
#create_page(30,39, worksheet)
##text box##
#textbox = tk.Text(window, bg='light grey')
#textbox.place(x=64, y=80)


## Edit the canvas ##

#Function to create the working grid
upcomingZoneX = False
upcomingZoneY = False



def toggledrawZone():
    addArea = not addArea    

def startDraw(event):
    global upcomingZoneX 
    global upcomingZoneY
    
    upcomingZoneX = event.x
    upcomingZoneY = event.y


def draw(event):
    #print(event)
    color="red"
    x1,y1= (event.x-1), (event.y-1)
    x2,y2= (event.x), (event.y)
    worksheet.create_oval(x1,y1,x2,y2,fill=color,outline=color)

def endDraw(event):
    color="red"
    x1,y1 = upcomingZoneX, upcomingZoneY
    x2,y2= (event.x), (event.y)
    #if abs(x1-x2) > 20 and abs(y1-y2) > 20:
        #worksheet.create_rectangle(x1,y1,x2,y2, fill=color,outline=color)
    temp = answerGrid(x1,y1,x2,y2)
    stored_grids.insert(0,temp)
    temp.draw(worksheet)

worksheet.bind('<Button-1>', startDraw)
worksheet.bind('<B1-Motion>',draw)
worksheet.bind('<ButtonRelease-1>', endDraw)


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
c = tk.Canvas(textbox, width=500, height=500)
c.pack(fill=tk.BOTH)
c.bind('<Configure>', create_grid)
textbox.tkraise
'''
#A failed test to see if a frame would help
#w = tk.Frame(worksheet)
#w.place(x = 10, y = 10, height = 40, width = 40)
#for x in range(4):
#    for y in range(4):
#        temp = tk.Text(w, height=10, width=10, bg="white")
#        xcord = 0+10*x
#        ycord = 0+10*y
#        temp.place(x=xcord, y=ycord)

window.mainloop()



doc = fitz.open("example.pdf") # open a document
for page in doc: # iterate the document pages
  text = page.get_text() # get plain text encoded as UTF-8
print(text)
