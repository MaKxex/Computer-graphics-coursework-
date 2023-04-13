import tkinter
import time
import numpy
from PIL import Image, ImageTk
 
animation_window_width=400
animation_window_height=400
animation_refresh_seconds = 0.01



def createImages(bgPath,fgPath):
    bg = Image.open(bgPath).resize((400,400))
    fg = Image.open(fgPath).resize((400,400))
    fg.putalpha(128)
    bg.paste(fg, (0,0), fg)
    bg.show()


def create_animation_window():
    window = tkinter.Tk()
    window.title("Kursa4 v0.03")
    window.geometry(f'{animation_window_width}x{animation_window_height}')
    return window
 
def create_animation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black",width=400,height=400)
    canvas.pack(fill="both", expand=True)
    return canvas

def changeImageOpacity(img,opacity):
    data = numpy.asarray(img)
    data = numpy.copy(data)
    data.setflags(write=1)
    for i in data:
        for j in i:
            j[3] = opacity
    img = Image.fromarray(data)
    return img

def fade(window, canvas,bgPath,fgPath):
    bg = Image.open(bgPath).resize((400,400)).convert("RGBA")
    fg = Image.open(fgPath).resize((400,400)).convert("RGBA")
    cl = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    i = 255
    while i > 0:
        fg = changeImageOpacity(fg,i) # fg.putalpha(i)
        cl.paste(bg, (0,0), bg)
        cl.paste(fg, (0,0), fg)
        bgCanvas = ImageTk.PhotoImage(cl)
        canvas.create_image(400,400,image=bgCanvas)
        window.update()
        time.sleep(animation_refresh_seconds)
        i-=2
        if i < 0: break
    window.mainloop()
    
def swipe(window, canvas,bgPath,fgPath):
    bg = Image.open(bgPath).resize((400,400)).convert("RGBA")
    fg = Image.open(fgPath).resize((400,400)).convert("RGBA")
    cl = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    i = 0
    while i < 400:
        newfg = fg.crop((0, int(i), 0+400, 400+400))
        cl.paste(bg, (0,0), bg)
        cl.paste(newfg, (0,400-(400+int(i))), newfg)
        bgCanvas = ImageTk.PhotoImage(cl)
        canvas.create_image(400,400,image=bgCanvas)
        window.update()
        time.sleep(animation_refresh_seconds)
        i+=0.5
        if i >= 400:
            print("s")
            i = 0
    window.mainloop()

def curtain(window, canvas,bgPath,fgPath):
    bg = Image.open(bgPath).resize((400,400)).convert("RGBA")
    fg = Image.open(fgPath).resize((400,400)).convert("RGBA")
    cl = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    i = 0
    while i < 400:
        leftSide = fg.crop((0, 0, 200-i, 200+400)) # left side
        rightSide = fg.crop((200+i, 0, 0+400, 0+400)) # right side
        cl.paste(bg, (0,0), bg)
        cl.paste(leftSide, (0,0), leftSide)
        cl.paste(rightSide, (200+i,0), rightSide)

        bgCanvas = ImageTk.PhotoImage(cl)
        canvas.create_image(0,0,image=bgCanvas,anchor="nw")
        window.update()
        time.sleep(animation_refresh_seconds)
        i+=1
        if i >= 400: i=0
    window.mainloop()



animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
#swipe(animation_window, animation_canvas, "asd.png","3.png")
curtain(animation_window, animation_canvas, "asd.png","3.png")
#fade(animation_window,animation_canvas,"coolvin.jpg","vin.png")



