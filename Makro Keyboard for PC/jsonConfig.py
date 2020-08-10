import json

def saveToJson(jfile,data):
    print(data)
    if(jfile.closed):
        jfile=open('keybindings.json', 'r+')

    jfile.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, jfile, indent=4)
    jfile.truncate()     # remove remaining part

def resetBinding(button_number,data):
    for btn in data['buttons']:
        #print(btn)
        if(btn["button_num"]==("{}".format(button_number))):
            print("found")
            btn["button_attributes"]=[]
            #btn["button_attributes"]+=("{}".format(word))
            print(btn)



def adjustBinding(button_number,word,data):
    for btn in data['buttons']:
        #print(btn)
        if(btn["button_num"]==("{}".format(button_number))):
            print("found {}".format(btn["button_num"]))
            btn["button_attributes"]+=word
            #btn["button_attributes"]+=("{}".format(word))
            print(btn)
            break

def getBindings(button_number,data):
    for btn in data['buttons']:
        if(btn["button_num"]==("{}".format(button_number))):
            print("found")
            print(btn)
            return btn["button_attributes"]

def getBindingsForSerial(button_number,data):
    serial_str=[]
    for i in getBindings(button_number,data):
        if(i!=chr(0)):
            serial_str+=i
    return serial_str

keys_longer_than_byte={
"ctrl":0x80,
"shift":0x81,
"alt":0x82 ,
"windows":0x83 ,
"right ctrl":0x84,
"right shift":0x85,
"alt gr":0x86,
"menu":0x87,
"up":0xda,
"down":0xd9,
"left":0xd8,
"right":0xd7,
"backspace":0xb2,
"tab":0xb3,
"enter":0xb0,
"esc":0xb1,
"insert":0xd1,
"delete":0xd4,
"page up":0xd3,
"page down":0xd6,
"home":0xd2,
"end":0xd5,
"caps lock":0xc1,
"f1":0xc2,
"f2":0xc3,
"f3":0xc4,
"f4":0xc5,
"f5":0xc6,
"f6":0xc7,
"f7":0xc8,
"f8":0xc9,
"f9":0xca,
"f10":0xcb,
"f11":0xcc,
"f12":0xcd,
"space":0x20
}


def asciiTransformer(value):
    #It can be used when reading the json
    for i in keys_longer_than_byte:
        #print(i)
        #print(keys_longer_than_byte[i])
        if(keys_longer_than_byte[i]==value):
            #print("found")
            return i

    return chr(value)

def jsonTransformer(keys):
    # Same with func but it recieves parsed list
    new_keys=[]
    new_keys+=chr(2)
    for key in keys:
        if(len(key)>1):
            new_keys+= chr(keys_longer_than_byte[key])
        else:
            new_keys+=key
    new_keys+=chr(2)
    print(new_keys)
    return new_keys
