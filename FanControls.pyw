import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import asyncio
from kasa import SmartPlug, SmartBulb
from tkinter import colorchooser
import colorsys
from bleak import BleakClient, BleakScanner
from threading import Thread
import bluetooth_test
import os
import json


### INIT ###
with open("config.json") as jsonfile:
    data = json.load(jsonfile) # Reading the file
    print("Read successful from FanControls")
    #print(data['light1'])


light1_ip = data["light1"]
light2_ip = data["light2"]
light3_ip = data["light3"]
switch_ip = data["switch"]
bt_address = ''

window = tk.Tk();
window.title("AK Office");

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Menu bar configuration


# Creating Menubar
menubar = Menu(window)

# Adding File Menu and commands
config = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Configuration', menu = config)
config.add_command(label ='Edit Config', command = lambda: os.startfile('config.json'))
#file.add_command(label ='Open...', command = None)
#file.add_command(label ='Save', command = None)
config.add_separator()
config.add_command(label ='Exit', command = window.destroy)

'''
# Adding Edit Menu and commands
edit = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Edit', menu = edit)
edit.add_command(label ='Cut', command = None)
edit.add_command(label ='Copy', command = None)
edit.add_command(label ='Paste', command = None)
edit.add_command(label ='Select All', command = None)
edit.add_separator()
edit.add_command(label ='Find...', command = None)
edit.add_command(label ='Find again', command = None)

# Adding Help Menu
help_ = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Help', menu = help_)
help_.add_command(label ='Tk Help', command = None)
help_.add_command(label ='Demo', command = None)
help_.add_separator()
help_.add_command(label ='About Tk', command = None)
'''

window.config(menu = menubar)

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





fanButtonFrame = tk.Frame(
    master=window,
    #relief=tk.SUNKEN,
    borderwidth=1,
    bd=5
    );

btButtonFrame = tk.Frame(
    master=window,
    #relief=tk.RAISED,
    borderwidth=1,
    bd=5
    );


textFrame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    );

fanLabelFrame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    );

btLabelFrame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    );

statusFrame = tk.Frame(
    master=window,
    #relief=tk.RAISED,
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

btDisconnectedImg = Image.open("resources/images/bt-disconnected1.png"); 
btDisconnectedImgResized = btDisconnectedImg.resize((70, 70), Image.LANCZOS);
btDisconnectedImg = ImageTk.PhotoImage(btDisconnectedImgResized)

btConnectedImg = Image.open("resources/images/bt-connected.png"); 
btConnectedImgResized = btConnectedImg.resize((70, 70), Image.LANCZOS);
btConnectedImg = ImageTk.PhotoImage(btConnectedImgResized)
### END OF Resizing the Image

statusLabel = tk.Label(statusFrame, text="Status: ", font="Times 11 bold", image=activeImg, compound="right");
statusLabel.pack();


fanLabel = tk.Label(fanLabelFrame, text="Fan Controls", font="Times 12 bold");
fanLabel.pack(fill = tk.BOTH);

btLabel = tk.Label(btLabelFrame, text="BT Controls", font="Times 12 bold");
btLabel.pack(fill = tk.BOTH);
### END OF INIT ###






### BUTTONS ###
fan_on_button = tk.Button(fanButtonFrame, text ="Fan ON", width=15, height=2,command=lambda m="Turn ON fan" : button_pressed(m));
fan_on_button.grid(row=0, column=0, sticky='nesw', padx=1, pady=1);
fan_off_button = tk.Button(fanButtonFrame, text ="Fan OFF",width=15, height=2,command=lambda m="Turn OFF fan": button_pressed(m));
fan_off_button.grid(row=0, column=1, sticky='nesw', padx=1, pady=1);
fan_on_lights_off_button = tk.Button(fanButtonFrame, text ="Lights OFF",width=15, height=2, command=lambda m="Fan ON Lights OFF": button_pressed(m));
fan_on_lights_off_button.grid(row=0, column=2, sticky='nesw', padx=1, pady=1);
fan_on_lights_on_button = tk.Button(fanButtonFrame, text ="Lights ON", width=15, height=2,command=lambda m="Fan ON Lights ON" : button_pressed(m));
fan_on_lights_on_button.grid(row=1, column=0, sticky='nesw', padx=1, pady=1);
color_picker_button = tk.Button(fanButtonFrame, text="Change color", width=15, height=2, command=lambda m="Change Color" : button_pressed(m))
color_picker_button.grid(row=1,column=1, sticky='nesw', padx=1, pady=1);
reset_color_button = tk.Button(fanButtonFrame, text="Reset color", width=15, height=2, command=lambda m="Reset Color" : button_pressed(m))
reset_color_button.grid(row=1,column=2, sticky='nesw', padx=1, pady=1);
brightness_up = tk.Button(fanButtonFrame, text="Up", width=15, height=2, command=lambda m="up" : button_pressed(m))
brightness_up.grid(row=2,column=0, sticky='nesw', padx=1, pady=1);
brightness_label= tk.Label(fanButtonFrame, text="Brightness: \n 2% ");
brightness_label.grid(row=2, column=1, sticky='nesw', padx=1, pady=1);
brightness_down = tk.Button(fanButtonFrame, text="Down", width=15, height=2, command=lambda m="down" : button_pressed(m))
brightness_down.grid(row=2,column=2, sticky='nesw', padx=1, pady=1);

bt_connect = tk.Button(btButtonFrame, text="Connect", width=15, height=2, command=lambda m="bt_connect" : button_pressed(m))
bt_connect.grid(row=0,column=0, sticky='nesw', padx=1, pady=1);
bt_label= tk.Label(btButtonFrame, text="Not Connected", width=15, height=2);
bt_label.grid(row=0, column=1, rowspan=2, sticky='nesw', padx=1, pady=1);
bt_on = tk.Button(btButtonFrame, text="On", width=15, height=2, command=lambda m="bt_on" : button_pressed(m))
bt_on.grid(row=1,column=0, sticky='nesw', padx=1, pady=1);
bt_off = tk.Button(btButtonFrame, text="Off", width=15, height=2, command=lambda m="bt_off" : button_pressed(m))
bt_off.grid(row=1,column=2, sticky='nesw', padx=1, pady=1);
bt_img_label= tk.Label(btButtonFrame, text="Not Connected", width=15, height=2);
bt_img_label.grid(row=0, column=1, rowspan=2, sticky='nesw', padx=1, pady=1);
bt_disconnect = tk.Button(btButtonFrame, text="Disconnect", width=15, height=2, command=lambda m="bt_disconnect" : button_pressed(m))
bt_disconnect.grid(row=0,column=2, sticky='nesw', padx=1, pady=1);

### END OF BUTTONS ###





### METHODS ###
async def async_turn_on_lights():
    p = SmartPlug(switch_ip)
    await p.update()  # Request the update
    await p.turn_on() # Turn the device on
    light1 = SmartBulb(light1_ip)
    light2 = SmartBulb(light2_ip)
    light3 = SmartBulb(light3_ip)

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

    p = SmartPlug(switch_ip)
    await p.update()  # Request the update
    await p.turn_on() # Turn the device on
    light1 = SmartBulb(light1_ip)
    light2 = SmartBulb(light2_ip)
    light3 = SmartBulb(light3_ip)

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
    p = SmartPlug(switch_ip)
    await p.update()  # Request the update

    await p.turn_off() #Turn the device off
    print("Turned switch OFF.");
    statusLabel.configure(image=inactiveImg)
    #statusLabel.image=inactiveImg
    return "Switch turned OFF."


async def async_turn_on_fan():
    p = SmartPlug(switch_ip)
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
    brightness_label["text"]="Brightness \n Unavailable" 



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
    try:
        my_color = colorchooser.askcolor();
        red=my_color[0][0] #first [0] only gives us the first part of my_color which is the rgb string
                           #second [0] gives us the first value in that rgb truple
        green=my_color[0][1]
        blue=my_color[0][2]
        
        #my_label = tk.Label(fanButtonFrame, text=(str(red) + "," + str(green) + "," + str(blue)))
        #rgb=colorsys.rgb_to_hsv(red*360,green*100,blue*100)
        #print(rgb)
        
        print(hex2rgb(my_color[1]))
        print(rgb2hsv(red,green,blue))
        #my_label = tk.Label(fanButtonFrame, text=my_color)
        #my_label.grid(row=1, column=2, sticky='nesw', padx=1, pady=1);
        
        #print("Color picker button was pressed")
        
        label.configure(bg=my_color[1])
        label["text"]=asyncio.run(async_change_bulb_color(rgb2hsv(red,green,blue)))
    except Exception:
        print("No color chosen")
    
    
async def async_change_bulb_color(hsv_val):
    light1 = SmartBulb(light1_ip)
    light2 = SmartBulb(light2_ip)
    light3 = SmartBulb(light3_ip)

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
    light1 = SmartBulb(light1_ip)
    light2 = SmartBulb(light2_ip)
    light3 = SmartBulb(light3_ip)

    await light1.update()
    await light2.update()
    await light3.update()
    
    await light1.set_hsv(0, 0, 100);
    await light2.set_hsv(0, 0, 100);
    await light3.set_hsv(0, 0, 100);
    
    await light1.set_brightness(50);
    await light2.set_brightness(50);
    await light3.set_brightness(50);

    await light1.update()
    await light2.update()
    await light3.update()
    
    label["text"]="Reset color successful."
    brightness_label["text"]="Brightness \n" + str(light1.brightness) + "%"
    print("Brightness is: " + str(light1.brightness))
    #label.configure(bg="")


def brightness_up():
    brightness_label["text"]=asyncio.run(async_brightness_up())


async def async_brightness_up():
    light1 = SmartBulb(light1_ip)
    light2 = SmartBulb(light2_ip)
    light3 = SmartBulb(light3_ip)
    await light1.update()
    brightness = light1.brightness
    if (brightness < 100):
        try:
            await light1.update()
            await light1.set_brightness(brightness + 10);
            await light1.update()
            print("light 1 initialized.")
            await light2.update()
            await light2.set_brightness(brightness + 10);
            await light2.update()
            print("light 2 initialized.")
            await light3.update()
            await light3.set_brightness(brightness + 10);
            await light3.update()
            print("light 3 initialized.")
            print("Brightness is: " + str(light1.brightness))
        except ValueError:
            await light1.update()
            await light1.set_brightness(100);
            await light1.update()
            await light2.update()
            await light2.set_brightness(100);
            await light2.update()
            await light3.update()
            await light3.set_brightness(100);
            await light3.update()
            print("Error Caught: Value was above 100")
    
    return "Brightness \n" + str(light1.brightness) + "%"
    

def brightness_down():
    brightness_label["text"]=asyncio.run(async_brightness_down())

async def async_brightness_down():
    light1 = SmartBulb(light1_ip)
    light2 = SmartBulb(light2_ip)
    light3 = SmartBulb(light3_ip)
    
    await light1.update()
    brightness = light1.brightness
    if (brightness >= 0):
        try:
            await light1.update()
            await light1.set_brightness(brightness - 10);
            await light1.update()
            print("light 1 initialized.")
            await light2.update()
            await light2.set_brightness(brightness - 10);
            await light2.update()
            print("light 2 initialized.")
            await light3.update()
            await light3.set_brightness(brightness - 10);
            await light3.update()
            print("light 3 initialized.")
            print("Brightness is: " + str(light1.brightness))
        except ValueError:
            await light1.update()
            await light1.set_brightness(0);
            await light1.update()
            await light2.update()
            await light2.set_brightness(0);
            await light2.update()
            await light3.update()
            await light3.set_brightness(0);
            await light3.update()
            print("Error Caught: Value dropped below 0")
    
    return "Brightness \n" + str(light1.brightness) + "%"
    

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                ## BT Controls


        #refer to bluetooth_test.py

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                ## Main Control

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
    elif (m == "up"):
        brightness_up()
    elif (m == "down"):
        brightness_down()
    elif (m == "bt_connect"):
        try:
            from bleak.backends.winrt.util import allow_sta
            # tell Bleak we are using a graphical user interface that has been properly
            # configured to work with asyncio
            allow_sta()
            asyncio.run(bluetooth_test.connect())
            bt_img_label["image"]=btConnectedImg
            label["text"] = "Connected!"
        except ImportError:
            # other OSes and older versions of Bleak will raise ImportError which we
            # can safely ignore
            pass
    elif (m == "bt_on"):
        try:
            from bleak.backends.winrt.util import allow_sta
            allow_sta()
            asyncio.run(bluetooth_test.turn_on())
            label["text"] = "Lights turned on"
        except ImportError:
            pass
    elif (m == "bt_off"):
        try:
            from bleak.backends.winrt.util import allow_sta
            allow_sta()
            asyncio.run(bluetooth_test.turn_off())
            label["text"] = "Lights turned off"
        except ImportError:
            pass
        
    elif (m == "bt_disconnect"):
        label["text"] = "Disconnect not implemented"
        print("disconnecting...")
    else:
        print("Button message not defined AK")



async def init_method():
    if (data["ble_address"]!=""):
        bt_img_label["image"]=btConnectedImg
    else:
        bt_img_label["image"]=btDisconnectedImg
    p = SmartPlug(switch_ip)
    await p.update()  # Request the update
    if(p.is_on):
        light1 = SmartBulb(light1_ip)
        await light1.update()
        statusLabel["image"]=activeImg
        print("Brightness is: " + str(light1.brightness))
        return str(light1.brightness) + "%"
    else:
        statusLabel["image"]=inactiveImg
        return ("Unavailable")
    
### END OF METHODS ###



### INIT ###
brightness_label["text"]="Brightness \n " + asyncio.run(init_method())
textFrame.pack(fill=tk.BOTH);
fanLabelFrame.pack(fill=tk.BOTH);
fanButtonFrame.pack(fill=tk.BOTH);
statusFrame.pack(fill=tk.BOTH);
btLabelFrame.pack(fill=tk.BOTH);
btButtonFrame.pack(fill=tk.BOTH);


window.resizable(0, 0)
window.mainloop();

### END OF INIT ###
