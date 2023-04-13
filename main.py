try:
    import os, sys
    from tkinter import *
    from tkinter import filedialog, messagebox
    from PIL import Image, ImageTk
    import time
    import numpy as np
    import webbrowser
    
except ImportError:
    os.system('pip install numpy & pip install tkinter & pip install Pillow')
    sys.exit("Restart the script.")

stdSize = 500

class Cursa4():
    def __init__(self):
        self.root = Tk() 
        self.setWindow()
        self.firstPage()
        self.root.mainloop()

    def clearFrame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def Pathswitch(self):
        self.filePath = self.filePath[::-1]
        self.secondPage()

    def setWindow(self):
        self.width = stdSize
        self.height = stdSize
        self.root.geometry(str(self.width) + "x" + str(self.height))
        self.root.title("Cursa4")
        self.frame = Frame(self.root)
        self.canvasSize = self.width - 100
    
    def firstPage(self):
        def callback(event):
            webbrowser.open_new(event.widget.cget("text"))
        self.clearFrame()
        self.filePath = []
        self.root.geometry(str(250) + "x" + str(250))
        self.frame.pack(side="top", expand=True, fill="both")

        lf = LabelFrame(self.frame,text="Hello everyone!")
        Label(lf, text="Please select two images:").pack(padx=10, pady=10)
        Button(lf,text="Open a files", command=self.ChooseFile).pack(padx=10, pady=(0,20))
        Label(lf, text="Made by:Makxex").pack(anchor="s", padx=10)
        link = Label(lf, text="https://github.com/MaKxex")
        link.pack(anchor="s", pady=2)
        link.bind("<Button-1>", callback)
        link.configure(underline=True)
        lf.place(anchor="c", relx=.5, rely=.5)
        
    def secondPage(self):
        self.clearFrame()
        self.root.geometry(str(250) + "x" + str(300))
        lf = LabelFrame(self.frame,text="Please choose action")
        Button(lf, text="Switch", command=self.Pathswitch).pack(padx=10, pady=10)
        Label(lf, text=f"bg: {str(os.path.split(os.path.realpath(self.filePath[0]))[1])}\nfg: {str(os.path.split(os.path.realpath(self.filePath[1]))[1])}").pack(padx=10, pady=10)
        Button(lf, text="fade", command=self.fade).pack(padx=10, pady=(10,0))
        Button(lf, text="swipe", command=self.swipe).pack(pady=10)
        Button(lf, text="curtain", command=self.curtain).pack(pady=(0,10))
        Button(lf, text="Back", command=self.firstPage).pack(pady=(0,10))
        lf.place(anchor="c", relx=.5, rely=.5)

    def thirdPage(self):
        self.clearFrame()
        self.root.geometry(str(self.width) + "x" + str(self.height))

        canvas = Canvas(self.frame, width=self.canvasSize-3, height=self.canvasSize-3, bg="black")
        canvas.pack()
        self.fr = Frame(self.frame, width=self.width, height=self.canvasSize)
        Button(self.fr,text="Back", command=self.secondPage).grid(row=0, column=0)
        self.fr.pack()
        return canvas

    #  Effects
    def changeImageOpacity(self,img,opacity):
        data = np.asarray(img)
        #data = np.copy(data)
        #data.setflags(write=1)
        for i in data:
            for j in i:
                j[3] = opacity
        return Image.fromarray(data)

    def cropX(self,img,left,up):
        data = np.asarray(img)
        data = np.copy(data)
        data.setflags(write=1)

        for index,x in enumerate(data):
            if index >= up:
                for index2, y in enumerate(x):
                    if index2 >= left:
                        y[3] = 0
        return Image.fromarray(data)

    def cropY(self,img,right,bottom):
        data = np.asarray(img)
        data = np.copy(data)
        data.setflags(write=1)

        for index,x in enumerate(reversed(data)):
            if index >= bottom:
                for index2, y in enumerate(reversed(x)):
                    if index2 >= right:
                        y[3] = 0
        return Image.fromarray(data)
    
    # /Effects
    def fade(self):
        try:
            canvas = self.thirdPage()
            bg = Image.open(self.filePath[0]).resize((self.canvasSize,self.canvasSize)).convert("RGBA")
            fg = Image.open(self.filePath[1]).resize((self.canvasSize,self.canvasSize)).convert("RGBA")
            cl = Image.new('RGBA', (self.canvasSize, self.canvasSize), (255, 255, 255, 0))
            i = 255
            while i > 0:
                fg = self.changeImageOpacity(fg,i) # fg.putalpha(i)
                cl.paste(bg, (0,0), bg)
                cl.paste(fg, (0,0), fg)
                bgCanvas = ImageTk.PhotoImage(cl)
                canvas.create_image(0,0,image=bgCanvas,anchor="nw")
                self.root.update()
                time.sleep(0.02)
                i-=4
                if i < 0: time.sleep(2); i = 255
        except TclError:
            pass
    
    def swipe(self):
        try:
            canvas = self.thirdPage()
            bg = Image.open(self.filePath[1]).resize((self.canvasSize,self.canvasSize)).convert("RGBA")
            fg = Image.open(self.filePath[0]).resize((self.canvasSize,self.canvasSize)).convert("RGBA")
            cl = Image.new('RGBA', (self.canvasSize, self.canvasSize), (255, 255, 255, 0))
            i = 0
            while i < self.canvasSize:
                cl.paste(bg, (0,0), bg)
                newfg = self.cropY(fg,0,i)
                cl.paste(newfg, (0,0), newfg) # cl.paste(newfg, (0,self.canvasSize-(self.canvasSize+int(i))), newfg)
                bgCanvas = ImageTk.PhotoImage(cl)
                canvas.create_image(0,0,image=bgCanvas,anchor="nw")
                self.root.update()
                i+=2
                if i >= self.canvasSize: time.sleep(2); i = 0
        except TclError:
            pass


    def curtain(self):
        try:
            canvas = self.thirdPage()
            bg = Image.open(self.filePath[0]).resize((self.canvasSize,self.canvasSize)).convert("RGBA")
            fg = Image.open(self.filePath[1]).resize((self.canvasSize,self.canvasSize)).convert("RGBA")
            cl = Image.new('RGBA', (self.canvasSize, self.canvasSize), (255, 255, 255, 0))
            i = 0
            while i < int(self.canvasSize/2):
                cl.paste(bg, (0,0), bg)
                leftSide = self.cropX(fg,200-i,0)  #leftSide = fg.crop((0, 0, int((self.canvasSize/2)-i), self.canvasSize + self.canvasSize)) # left side
                rightSide = self.cropY(fg,200-i,0) #rightSide = fg.crop((int((self.canvasSize/2)+i), 0, 0+self.canvasSize, 0+self.canvasSize)) # right side
                cl.paste(leftSide, (0,0), leftSide)
                cl.paste(rightSide, (0,0), rightSide)
                bgCanvas = ImageTk.PhotoImage(cl)
                canvas.create_image(0,0,image=bgCanvas,anchor="nw")
                self.root.update()
                i+=2
                if i >= int(self.canvasSize/2): time.sleep(2);i=0
        except TclError:
            pass
        
    def ChooseFile(self):
        self.filePath = list(filedialog.askopenfilenames(
            initialdir=os.path.dirname(os.path.realpath(__file__)),
            filetypes=(('Image files', '*.PNG *.jpg'),('All files', '*.*')),
            title="Open a files",))
        if len(self.filePath) == 2:
            self.secondPage()
        else:
            messagebox.showwarning("Warning", "Please select two images")
Cursa4()