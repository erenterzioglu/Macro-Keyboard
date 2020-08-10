from serial import *
import serial.tools.list_ports
#import serial.tools.list_ports
import jsonConfig as j
import time
#connected_devices=[""]

def serialConnection(values,device):
    print("hi ")
    print("serialConnection()")
    print("values: {} , port: {}".format(values,device))

    #c_number=getDeviceComNumber(device)
    #print(c_number)
    print("port is going to open")
    port = serial.Serial(getDeviceComNumber(device), 9600, timeout=1) #serialport değşecek
    time.sleep(3)

    if(port is not None):
        print("port openned")
        for i in range(16):
            binding_str= ''.join(j.getBindings(i,values))
            print("str value: {} str type: {}".format(binding_str, type(binding_str)))
            time.sleep(0.001)

            if(len(binding_str)>-1):

                port.write(bytes("{}".format(chr(i)),encoding="ascii"))
                while(port.inWaiting()<1):
                    time.sleep(0.1)
                    print("Waiting data")
                time.sleep(0.1)
                print("Data comes: ")
                print(port.readline().decode('ascii'))


                port.write(bytes("{}".format(chr(len(binding_str))),encoding="ascii"))
                while(port.inWaiting()<1):
                    time.sleep(0.1)
                    print("Waiting data")
                #time.sleep(0.1)
                print("Data need to send lenght: ")
                print(port.readline().decode('ascii'))


                #port.write(bytes(binding_str,encoding="ascii"))
                print(binding_str.encode('iso8859_9'))
                port.write(binding_str.encode('iso8859_9'))
                while(port.inWaiting()<len(binding_str)):
                    time.sleep(0.1)
                    print("Waiting data")
                time.sleep(0.1)
                print("Data comes: ")
                print(port.readline().decode('iso8859_9'))

            else:
                print("Bindings of the key error ")

        port.close()

    else:
        print("Device cannot found")

def getDevices():

    connected_devices=[]
    connected_devices=serial.tools.list_ports.comports()
    #print("connected_devices:")
    #print(connected_devices)
    #for i in connected_devices:
    #    print(i)
    return connected_devices



def getDeviceComNumber(device):
    number= device.split(' ')
    #print(number[0])
    return number[0]
