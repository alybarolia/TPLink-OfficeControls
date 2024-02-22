import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import asyncio
from kasa import SmartPlug, SmartBulb
from tkinter import colorchooser
import colorsys
##test
### INIT ###
window = tk.Tk();
window.title("AK Office");

buttonFrame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    );

textFrame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    );

statusFrame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    );

ico = Image.open('resources/images/settings_icon.ico')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

label = tk.Label(textFrame, text="", font="Times 12 bold");
label.pack(fill = tk.BOTH);

### Resizing the Image
activeImg = Image.open("resources/images/green-checkmark-icon.png"); # Open Image
activeResized = activeImg.resize((20, 20), Image.LANCZOS); # resize
activeImg = ImageTk.PhotoImage(activeResized) # assign resize image to original

inactiveImg = Image.open("resources/images/red-x-icon.png"); 
inactiveResized = inactiveImg.resize((20, 20), Image.LANCZOS);
inactiveImg = ImageTk.PhotoImage(inactiveResized)

warningImg = Image.open("resources/images/warning.png"); 
warningResized = warningImg.resize((20, 20), Image.LANCZOS);
warningImg = ImageTk.PhotoImage(warningResized)
### END OF Resizing the Image

statusLabel = tk.Label(statusFrame, text="Status: ", font="Times 11 bold", image=activeImg, compound="right");
statusLabel.pack();
### END OF INIT ###






### BUTTONS ###
fan_on_button = tk.Button(buttonFrame, text ="Turn ON fan",command=lambda m="Turn ON fan" : button_pressed(m));
fan_on_button.grid(row=0, column=0, sticky='nesw', padx=1, pady=1);
fan_off_button = tk.Button(buttonFrame, text ="Turn OFF fan",command=lambda m="Turn OFF fan": button_pressed(m));
fan_off_button.grid(row=0, column=1, sticky='nesw', padx=1, pady=1);
fan_on_lights_off_button = tk.Button(buttonFrame, text ="Fan ON \nLights OFF",command=lambda m="Fan ON Lights OFF": button_pressed(m));
fan_on_lights_off_button.grid(row=0, column=2, sticky='nesw', padx=1, pady=1);
fan_on_lights_on_button = tk.Button(buttonFrame, text ="Fan ON \nLights ON",command=lambda m="Fan ON Lights ON" : button_pressed(m));
fan_on_lights_on_button.grid(row=1, column=0, sticky='nesw', padx=1, pady=1);
color_picker_button = tk.Button(buttonFrame, text="Change color", command=lambda m="Change Color" : button_pressed(m))
color_picker_button.grid(row=1,column=1, sticky='nesw', padx=1, pady=1);
reset_color_button = tk.Button(buttonFrame, text="Reset color", command=lambda m="Reset Color" : button_pressed(m))
reset_color_button.grid(row=1,column=2, sticky='nesw', padx=1, pady=1);
### END OF BUTTONS ###





### METHODS ###
async def async_turn_on_lights():
    p = SmartPlug("10.0.0.115")
    await p.update()  # Request the update
    await p.turn_on() # Turn the device on
    light1 = SmartBulb("10.0.0.84")
    light2 = SmartBulb("10.0.0.9")
    light3 = SmartBulb("10.0.0.204")

    await light1.update()
    print("light 1 initialized.")
    await light2.update()
    print("light 2 initialized.")
    await light3.update()
    print("light 3 initialized.")

    await light1.turn_on()
    await light2.turn_on()
    await light3.turn_on()
    
    print("All lights turned ON.")
    statusLabel.configure(image=activeImg)
    return "All lights turned ON."
    

async def async_turn_off_lights():

    p = SmartPlug("10.0.0.115")
    await p.update()  # Request the update
    await p.turn_on() # Turn the device on
    light1 = SmartBulb("10.0.0.84")
    light2 = SmartBulb("10.0.0.9")
    light3 = SmartBulb("10.0.0.204")

    await light1.update()
    print("light 1 initialized.")
    await light2.update()  
    print("light 2 initialized.")
    await light3.update()
    print("light 3 initialized.")
    await light1.turn_off()
    await light2.turn_off()
    await light3.turn_off()
    #label["text"]="hello"
    print("All lights turned OFF.")
    statusLabel.configure(image=activeImg)
    return "All lights turned OFF."
    

async def async_turn_off_fan():
    p = SmartPlug("10.0.0.115")
    await p.update()  # Request the update

    light1 = SmartBulb("10.0.0.84")
    light2 = SmartBulb("10.0.0.9")
    light3 = SmartBulb("10.0.0.204")

    await light1.update()
    print("light 1 initialized.")
    await light2.update()  
    print("light 2 initialized.")
    await light3.update()
    print("light 3 initialized.")

    await light1.set_hsv(0, 0, 100);
    await light2.set_hsv(0, 0, 100);
    await light3.set_hsv(0, 0, 100);

    await p.turn_off() #Turn the device off
    print("Turned switch OFF.");
    statusLabel.configure(image=inactiveImg)
    #statusLabel.image=inactiveImg
    return "Switch turned OFF."


async def async_turn_on_fan():
    p = SmartPlug("10.0.0.115")
    await p.update()  # Request the update
    await p.turn_on() #Turn the device off
    print("Turned switch ON.")
    statusLabel.configure(image=activeImg)
    return "Switch turned ON."


def turn_off_fan():
    #B["state"]="disabled"
    #asyncio.run(async_turn_off_fan())
    #B["state"]="enabled"
    label["text"]=asyncio.run(async_turn_off_fan())



def turn_on_fan():
    #B["state"]="disabled"
    #asyncio.run(async_turn_off_fan())
    #B["state"]="enabled"
    label["text"]=asyncio.run(async_turn_on_fan())


def turn_off_lights():
    #B["state"]="disabled"
    #asyncio.run(async_turn_off_fan())
    #B["state"]="enabled"
    
    label["text"]=asyncio.run(async_turn_off_lights())

def turn_on_lights():
    #B["state"]="disabled"
    #asyncio.run(async_turn_off_fan())
    #B["state"]="enabled"
    #label.config(bg="green")
    label["text"]=asyncio.run(async_turn_on_lights())

def hex2rgb(hex_value):
    h = hex_value.strip("#") 
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def rgb2hsv(r, g, b):
 # Normalize R, G, B values
 r, g, b = r / 255.0, g / 255.0, b / 255.0
 
 # h, s, v = hue, saturation, value
 max_rgb = max(r, g, b)    
 min_rgb = min(r, g, b)   
 difference = max_rgb-min_rgb 
 
 # if max_rgb and max_rgb are equal then h = 0
 if max_rgb == min_rgb:
     h = 0
 
 # if max_rgb==r then h is computed as follows
 elif max_rgb == r:
     h = (60 * ((g - b) / difference) + 360) % 360
 
 # if max_rgb==g then compute h as follows
 elif max_rgb == g:
     h = (60 * ((b - r) / difference) + 120) % 360
 
 # if max_rgb=b then compute h
 elif max_rgb == b:
     h = (60 * ((r - g) / difference) + 240) % 360
 
 # if max_rgb==zero then s=0
 if max_rgb == 0:
     s = 0
 else:
     s = (difference / max_rgb) * 100
 
 # compute v
 v = max_rgb * 100
 # return rounded values of H, S and V
 return tuple(map(round, (h, s, v)))


def colorPicker():
    my_color = colorchooser.askcolor();
    red=my_color[0][0] #first [0] only gives us the first part of my_color which is the rgb string
                       #second [0] gives us the first value in that rgb truple
    green=my_color[0][1]
    blue=my_color[0][2]
    
    #my_label = tk.Label(buttonFrame, text=(str(red) + "," + str(green) + "," + str(blue)))
    #rgb=colorsys.rgb_to_hsv(red*360,green*100,blue*100)
    #print(rgb)
    
    print(hex2rgb(my_color[1]))
    print(rgb2hsv(red,green,blue))
    #my_label = tk.Label(buttonFrame, text=my_color)
    #my_label.grid(row=1, column=2, sticky='nesw', padx=1, pady=1);
    
    #print("Color picker button was pressed")
    
    label.configure(bg=my_color[1])
    label["text"]=asyncio.run(async_change_bulb_color(rgb2hsv(red,green,blue)))
    
    
async def async_change_bulb_color(hsv_val):
    light1 = SmartBulb("10.0.0.84")
    light2 = SmartBulb("10.0.0.9")
    light3 = SmartBulb("10.0.0.204")

    await light1.update()
    print("light 1 initialized.")
    await light2.update()
    print("light 2 initialized.")
    await light3.update()
    print("light 3 initialized.")

    h, s, v = hsv_val
    
    await light1.set_hsv(h, s, v);
    await light2.set_hsv(h, s, v);
    await light3.set_hsv(h, s, v);
    
    label["text"]="Changed color to "
    



async def async_reset_bulb_color():
    light1 = SmartBulb("10.0.0.84")
    light2 = SmartBulb("10.0.0.9")
    light3 = SmartBulb("10.0.0.204")

    await light1.update()
    print("light 1 initialized.")
    await light2.update()
    print("light 2 initialized.")
    await light3.update()
    print("light 3 initialized.")
    
    await light1.set_hsv(0, 0, 100);
    await light2.set_hsv(0, 0, 100);
    await light3.set_hsv(0, 0, 100);
    
    label["text"]="Reset color successful."
    label.configure(bg="")



def button_pressed(m):

    if (m == "Turn OFF fan"):
        turn_off_fan()
    elif (m == "Turn ON fan"):
        turn_on_fan()
    elif (m == "Fan ON Lights OFF"):
        turn_off_lights()
    elif (m == "Fan ON Lights ON"):
        #fan_off_button.configure(state="disabled")
        turn_on_lights()
    elif (m == "Change Color"):
        colorPicker()
    elif (m == "Reset Color"):
        asyncio.run(async_reset_bulb_color())
    else:
        print("Button message not defined AK")


    
### END OF METHODS ###






### INIT ###

textFrame.pack(fill=tk.BOTH);
buttonFrame.pack(fill=tk.BOTH);
statusFrame.pack(fill=tk.BOTH);
window.mainloop();

### END OF INIT ###
