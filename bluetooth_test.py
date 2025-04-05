import asyncio
from bleak import BleakClient, BleakScanner
#import config as cfg
import json
from tkinter import colorchooser

with open("config.json") as jsonfile:
    data = json.load(jsonfile) # Reading the file
    print("Read successful from bluetooth_test")
    #print(data["light1"])


characteristic_uuid = data["characteristic_uuid"]
#bt_address = ''



async def details():
    # Device name to be searched for
    my_device_name = data["btDeviceName"]
    # Device Enumeration
    devices = await BleakScanner.discover()
    myDevice = None
    for d in devices:
        if d.name == my_device_name:
            myDevice = d
    if(myDevice != None):
        # Device Connection
        async with BleakClient(str(myDevice.address)) as client:
            print('List of all characteristics: ')
            for characteristic in client.services.characteristics:
                x = client.services.characteristics.get(characteristic)
                print(client.services.get_service(x.service_handle).description, x.service_uuid, 
                       x.description, x.uuid, x.properties)
#asyncio.run(details())



# Bluetooth LE scanner
async def connect():
    myDevice = ''
    devices = await BleakScanner.discover(5.0, return_adv=True)
    for d in devices:
        if(devices[d][1].local_name == data["btDeviceName"]):
            print("Found BT device")
            myDevice = d
    ble_address = myDevice
    print (ble_address)
    data["ble_address"] = ble_address
    with open("config.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    global bt_address 
    bt_address = ble_address
    
    

   
    ##    Service: 00001800-0000-1000-8000-00805f9b34fb (Generic Access Profile)
    ##    Characteristic: 00002a00-0000-1000-8000-00805f9b34fb (Device Name)
    ##    Service: 0000ffd5-0000-1000-8000-00805f9b34fb (Vendor specific)
    ##    Characteristic: 0000ffda-0000-1000-8000-00805f9b34fb (Vendor specific)
    ##    Characteristic: 0000ffd9-0000-1000-8000-00805f9b34fb (Vendor specific)
    ##    Service: 0000ffd0-0000-1000-8000-00805f9b34fb (Vendor specific)
    ##    Characteristic: 0000ffd4-0000-1000-8000-00805f9b34fb (Vendor specific)
    ##    Characteristic: 0000ffd1-0000-1000-8000-00805f9b34fb (Vendor specific)

    ##List of all characteristics: 
    ##Generic Access Profile 00001800-0000-1000-8000-00805f9b34fb Device Name 00002a00-0000-1000-8000-00805f9b34fb ['read']
    ##Vendor specific 0000ffd5-0000-1000-8000-00805f9b34fb Vendor specific 0000ffda-0000-1000-8000-00805f9b34fb ['notify']
    ##Vendor specific 0000ffd5-0000-1000-8000-00805f9b34fb Vendor specific 0000ffd9-0000-1000-8000-00805f9b34fb ['write-without-response', 'write']
    ##Vendor specific 0000ffd0-0000-1000-8000-00805f9b34fb Vendor specific 0000ffd4-0000-1000-8000-00805f9b34fb ['notify']
    ##Vendor specific 0000ffd0-0000-1000-8000-00805f9b34fb Vendor specific 0000ffd1-0000-1000-8000-00805f9b34fb ['write-without-response']

    async with BleakClient(ble_address) as client:
        print("Connected to BLE device")
        print(client.is_connected)
        #await client.start_notify(characteristic_uuid, notification_handler)
        #await asyncio.sleep(10.0)
        #await client.stop_notify(characteristic_uuid)






async def turn_on():
    print(data["ble_address"])
    async with BleakClient(data["ble_address"]) as client:
        print("Connected to BLE device")
        if (client.is_connected):
            lista = [204, 35, 51]
            values = bytearray(lista) 

        await client.write_gatt_char(characteristic_uuid, values, False)
    print("LED lights turned on")



async def turn_off():
    print(data["ble_address"])
    async with BleakClient(data["ble_address"]) as client:
        print("Connected to BLE device")
        if (client.is_connected):
            lista = [204, 36, 51]
            values = bytearray(lista) 

        await client.write_gatt_char(characteristic_uuid, values, False)

        #data = await client.read_gatt_char(characteristic_uuid)
        #print(data)
    print("LED lights turned off")


async def bt_colorPicker():
    try:
        my_color = colorchooser.askcolor();
        red=my_color[0][0] #first [0] only gives us the first part of my_color which is the rgb string
                           #second [0] gives us the first value in that rgb truple
        green=my_color[0][1]
        blue=my_color[0][2]
        
        #my_label = tk.Label(fanButtonFrame, text=(str(red) + "," + str(green) + "," + str(blue)))
        #rgb=colorsys.rgb_to_hsv(red*360,green*100,blue*100)
        #print(rgb)
        
        #print(hex2rgb(my_color[1]))
        #print(rgb2hsv(red,green,blue))
        print(red)
        print(green)
        print(blue)
        
        #print("Color picker button was pressed")

        async with BleakClient(data["ble_address"]) as client:
            print("Connected to BLE device")
            if (client.is_connected):
                lista = [86, red, green, blue, (int(10 * 255 / 100) & 0xFF), 256-16, 256-86]
                values = bytearray(lista)

            await client.write_gatt_char(characteristic_uuid, values, False)
        print("LED lights changed color")

    finally:
        print("done method")





#asyncio.run(connect())
#asyncio.run(turn_on())


