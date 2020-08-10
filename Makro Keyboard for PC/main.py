from tkinter import *
import tkinter.messagebox
import keyboard
import json
import jsonConfig as j
from deviceConfig import *
import time

pressed_button_list=[]

with open('keybindings.json', 'r+') as f:
    data = json.load(f)
    #print(data)

def anyModifier(keys):
    print("anyModifier(): ")

    for i in keys.split('+'):
        print(i)
        if(keyboard.is_modifier(i)):
            return True
    return False

def buttonPressed(screen,button_number):

    print("{} butonuna basildi".format(button_number))
    S = Scrollbar(screen)
    T = Text(screen, height=7, width=50)
    #S.pack(side=RIGHT,fill=Y)
    #T.pack(side=LEFT, fill=Y)

    S.place(x=(4*button_width-15),y=0,relwidth=0.06, relheight=0.75)
    T.place(x=0,y=0,relwidth=0.949, relheight=0.75)

    S.config(command=T.yview)
    T.config(yscrollcommand=S.set,cursor="none")

    row=int(button_number/4)
    column= int(button_number-4*int(button_number/4))

    print("row= {} column= {}".format(row,column))
    T.insert(END,"{}.button menu: \n".format(button_matrix[row][column]))
    T.insert(END,"_"*30)


    hotkey_flag=False
    for i in j.getBindings(button_number,data):
        if(i==chr(2)):
            hotkey_flag=not hotkey_flag
            if(hotkey_flag== False):
                T.delete('end -2 chars')
                T.insert(END,"\n")

        elif(hotkey_flag==True):
            T.insert(END,j.asciiTransformer(ord(i)) +"+")
        else:
            T.insert(END,i+"\n")


    flag=0
    #keycount=0 #eski değerden kaç tane tusa basildigi cekilecek
    keycount=len(j.getBindings(button_number,data))

    def exitOnMakroMenu():

        flag=1
        global pressed_button_list
        #json ayarlamaları yapılacak
        j.adjustBinding(button_number,pressed_button_list,data)
        j.saveToJson(f,data) #############################

        T.destroy()
        S.destroy()

        #print("Buraya geldi")
        pressed_button_list=[]
        keycount=0

        keyboard.unhook_all()
        screen.switch_frame(StartPage)


    def refresh():

        global pressed_button_list ###################
        nonlocal keycount

        while(flag==0):

            #print('You Pressed {} Key!'.format(keyboard.read_hotkey(suppress=False)))
            key=keyboard.read_hotkey(suppress=False)
            keyboard.release(keyboard.stash_state())
            time.sleep(0.020)

            new_keys_long=len(key.split('+'))

            if(new_keys_long>1):
                new_keys_long+=2
            #40 yazan yer 20 idi
            if(keycount+new_keys_long>30 or new_keys_long>8):
                print("Too much button pressed")
                tkinter.messagebox.showwarning(title="warning",message="Too much button pressed")
            else:
                #key=keyboard.read_key()
                """
                key=keyboard.read_hotkey(suppress=False)
                keyboard.release(keyboard.stash_state())
                time.sleep(0.020)
                """
                #if(len(key)>1):
                    #something
                T.insert(END, key + '\n')
                #keycount+=1
                #pressed_button_list+=key


                keycount+=new_keys_long

                if(new_keys_long>1 or anyModifier(key)):
                    pressed_button_list+=(j.jsonTransformer(key.split('+')))
                else:
                    pressed_button_list+=key

            print("keycount {}".format(keycount))



    def resetBindings():

        global pressed_button_list
        nonlocal keycount
        #print("Ayarlar sıfırlandı")
        j.resetBinding(button_number,data) ########
        T.delete('1.0',END)
        T.insert(END,"{}.button menu: \n".format(button_matrix[row][column]))
        T.insert(END,"_"*30)

        #print("Keycount there: {}".format(keycount))
        keycount=0
        pressed_button_list= []



    button0= Button(screen,text="Save",command= exitOnMakroMenu)
    button0.place(x=(1 * button_width), y=(4 * button_height + 15), width=button_width, height=button_height)

    button1= Button(screen,text="Reset",command =resetBindings)
    button1.place(x=(2 * button_width), y=(4 * button_height + 15), width=button_width, height=button_height)

    keyboard.call_later(refresh, args=(), delay=0.001)




def saveSettings(selection):

    print("Ayarlar Kaydedildi")
    j.saveToJson(f,data)
    #serial ayarları
    #port numarası , data
    #print("saveSettings(): ")
    #print(selection.get())
    #print(data)
    if(selection.get()=="Port" or selection.get() is None):
        tkinter.messagebox.showwarning('Port not selected','Please select a port')
    else:
        serialConnection(data,selection.get())



def reset():

    print("Ayarlar Sıfırlandı")
    for i in range(16):
        j.resetBinding(i,data)
    j.saveToJson(f,data)



button_width=65
button_height=55

buttons=[]
first_row=["1","2","3","A"]
second_row=["4","5","6","B"]
third_row=["7","8","9","C"]
fourth_row=["*","0","#","D"]
button_matrix=[first_row,second_row,third_row,fourth_row]


def openningScreen(screen):

    def callback(context,k):
        port_select.destroy()
        context.switch_frame2(PageOne,k)

    for i in range(0,4):
        for j in range(0,4):

            button= Button(screen,command=lambda k=((i*4)+j) :callback(screen,k) ,text=button_matrix[i][j])

            if(button_matrix[i][j]>='0' and button_matrix[i][j]<='9' ):
                button.config(bg="#31B1FF")
            else:
                button.config(bg="red2")
            button.config(fg="white", activebackground="gray25")

            button.place(x=(j*(button_width)),y=(i*(button_height)),width=button_width,height=button_height)
            buttons.append(button)



    variable = StringVar(screen)
    variable.set("Port") # default value
    #<Enter> <Leave>

    button= Button(screen,command = lambda k = variable  :saveSettings(k) ,text="Upload")
    button.place(x=(1*(button_width)),y=(4*(button_height)+15),width=button_width,height=button_height)
    button.config(bg="gray25", activebackground="gray76")

    button= Button(screen,command=reset ,text="Reset")
    button.place(x=(2*(button_width)),y=(4*(button_height)+15),width=button_width,height=button_height)
    button.config(bg="gray25", activebackground="gray76")

    def deviceSearch(event):

        nonlocal connected_devices
        nonlocal variable


        connected_devices=getDevices()
        #print("it is here")
        #print(connected_devices)
        menu = port_select.children["menu"]
        menu.delete(0, "end")
        for i in connected_devices:
            menu.add_command(label=i, command=lambda v=i: variable.set(v))

        if len(connected_devices)<1:
            variable.set("Port") # default value


    connected_devices=[" "]

    #print("first get devices:")
    #print(connected_devices)

    port_select = OptionMenu(screen, variable , *(connected_devices) )
    port_select.bind("<Button-1>",deviceSearch)
    port_select.config(bg="gray25",activebackground="gray76",highlightbackground="gray25")
    port_select.place(x=5,y=(4*(button_height)+22),width=button_width-10,height=2*button_height/3)


class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        #----------------------------------#
        self.config(bg="black")
        self.geometry("{}x{}".format((button_width*4), (button_height*5+25)))
        self.resizable(FALSE,FALSE)
        self.title("Makro Keyboard")
        #----------------------------------#
    def switch_frame2(self, frame_class,button_number):
        """Destroys current frame and replaces it with a new one."""
        print("Here with {}".format(button_number))
        new_frame = frame_class(self,button_number)

        if self._frame is not None:
            self._frame.destroy()

        if(new_frame is not None):
            self._frame = new_frame
            self._frame.pack()
        else:
            print("Error on creating class")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()

        if(new_frame is not None):
            self._frame = new_frame
            self._frame.pack()
        else:
            print("Error on creating class")



class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        openningScreen(master)

class PageOne(Frame):
    def __init__(self, master,button_number):
        Frame.__init__(self, master)
        buttonPressed(master,button_number)
        #Button(self, text="Return to start page",command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()
