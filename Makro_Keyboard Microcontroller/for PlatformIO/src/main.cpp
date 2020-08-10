#include <Arduino.h>
#include<EEPROM.h>
#include <Keyboard.h>
#include<Keypad.h>


char button_bindings[16][21];
String tmp_keys;
uint8_t button_number;
const uint8_t button_limit=30;/////////
uint8_t number_of_buttons;

struct modifiers{
  String button_name;
  unsigned char button_value;
}modifier_keys[35]={
{.button_name= "KEY_LEFT_CTRL", .button_value= 0x80},
{.button_name= "KEY_LEFT_SHIFT", .button_value= 0x81},
{.button_name= "KEY_LEFT_ALT", .button_value= 0x82},
{.button_name= "KEY_LEFT_GUI", .button_value= 0x83},
{.button_name= "KEY_RIGHT_CTRL", .button_value= 0x84},
{.button_name= "KEY_RIGHT_SHIFT", .button_value= 0x85},
{.button_name= "KEY_RIGHT_ALT", .button_value= 0x86},
{.button_name= "KEY_RIGHT_GUI", .button_value= 0x87},
{.button_name= "KEY_UP_ARROW", .button_value= 0xDA},
{.button_name= "KEY_DOWN_ARROW", .button_value= 0xD9},
{.button_name= "KEY_LEFT_ARROW", .button_value= 0xD8},
{.button_name= "KEY_RIGHT_ARROW", .button_value= 0xD7},
{.button_name= "KEY_BACKSPACE", .button_value= 0xB2},
{.button_name= "KEY_TAB", .button_value= 0xB3},
{.button_name= "KEY_RETURN", .button_value= 0xB0},
{.button_name= "KEY_ESC", .button_value= 0xB1},
{.button_name= "KEY_INSERT", .button_value= 0xD1},
{.button_name= "KEY_DELETE", .button_value= 0xD4},
{.button_name= "KEY_PAGE_UP", .button_value= 0xD3},
{.button_name= "KEY_PAGE_DOWN", .button_value= 0xD6},
{.button_name= "KEY_HOME", .button_value= 0xD2},
{.button_name= "KEY_END", .button_value= 0xD5},
{.button_name= "KEY_CAPS_LOCK", .button_value= 0xC1},
{.button_name= "KEY_F1", .button_value= 0xC2},
{.button_name= "KEY_F2", .button_value= 0xC3},
{.button_name= "KEY_F3", .button_value= 0xC4},
{.button_name= "KEY_F4", .button_value= 0xC5},
{.button_name= "KEY_F5", .button_value= 0xC6},
{.button_name= "KEY_F6", .button_value= 0xC7},
{.button_name= "KEY_F7", .button_value= 0xC8},
{.button_name= "KEY_F8", .button_value= 0xC9},
{.button_name= "KEY_F9", .button_value= 0xCA},
{.button_name= "KEY_F10", .button_value= 0xCB},
{.button_name= "KEY_F11", .button_value= 0xCC},
{.button_name= "KEY_F12", .button_value= 0xCD}
};




const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns

char hexaKeys[ROWS][COLS] = {
  {48,49,50,51},
  {52,53,54,55},
  {56,57,58,59},
  {60,61,62,63}
};

byte rowPins[ROWS] ={9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {5,4, 3, 2}; //connect to the column pinouts of the keypad


Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void clearEEPROM();
void writeEEPRom(String keys, uint8_t i);
void readEEPROM();
void buttonPressed(char button_value);
void pressButton(char button);



void getBindings(){
  /*This function control your bindings if you 
  faced with some errors*/
  Serial.println("getBindings(): ");
  uint8_t j;
  for (int i=0;i<16;i++){
    j=0;
    Serial.println(i);
    while(j<button_limit && button_bindings[i][j]!=0){
       Serial.print(int(button_bindings[i][j]));
       Serial.print(" ");
        j++;
    }
    Serial.println(" ");
  }
    
}

void setup() {

  Serial.begin(9600);

  while(!Serial){
    delay(1);
  }
  /* If your microcontroller supports USB you need to open line of code to the bottom  */
  Keyboard.begin();
  
  
  /*If you need to reset your EEPROM, you can use this function;
  but do not forget take to the comment after resetting. 
  If you forget it always deletes last bindings last values*/
  //clearEEPROM();
  
  /* Taking last values that left on the EEProm */
  readEEPROM();
  
  /*You can control your bindings that on your matrix with this function*/
  //getBindings();
}

void loop() {
  
  /* 
  If some data comes to the controller read that
  data= Pin number (1 byte), Key values (40 bytes )
  */
  /////////////////////////////////////////////////////////////////////
  char customKey = customKeypad.getKey();
  
  if (customKey){
    Serial.print("Button pressed: ");
    Serial.println(customKey);
    buttonPressed(customKey);
  }
  //////////////////////////////////////////////////////////////////////////

  if(Serial.available()>0){

       
    button_number=Serial.read();
    Serial.print("Comming value: ");
    //Serial.print(button_number);
    
    delay(100);
    //Serial.flush();

    while(Serial.available()<=0){
      delay(1);
    }
    number_of_buttons=Serial.read();
    Serial.print(number_of_buttons);
   
     while(Serial.available()<number_of_buttons){
      delay(1);
    }
    //delay(150);

    tmp_keys =Serial.readString();
    
   
    writeEEPRom(tmp_keys,button_number);

    Serial.print("Keys: ");
    Serial.print(tmp_keys);
    


  }
  delay(100);/////////////////
}


void readEEPROM(){
  /*
  When device started it takes the bindings
  from EEPROM 
  */

  int j;
  int address;

  for(int i=0; i<16;i++){

    j=0;

    while(j<button_limit){

      address= (i*button_limit)+j;
      button_bindings[i][j]= EEPROM.read(address);
      //Serial.print(button_bindings[i][j]);

      if(button_bindings[i][j]==0){
        j=button_limit;
      }
      else{
        j++;
      }

    }

    /*
    Serial.print(" Fetched data: ");
    j=0;
    while(j<button_limit && button_bindings[i][j]!=0 ){
      
      Serial.print(int(button_bindings[i][j]));
      Serial.println(" ");
      j++;

    }
    Serial.println(" ");
    */


  }
}

void writeEEPRom(String keys, uint8_t i){
  /* 
  If some data comes to the microcontroller  
    that means new bindings come and all of the data 
    saved into the EEProm permenantly 
    (not permenant, EEProm's lifetime actually :) )
  */

  int j;
  int address;
  j=0;

  //Serial.print(" Saving keys: ");

  // 0 yerine NULL yazıyordu
  while(keys[j]!=0){

    address= (i*button_limit)+j ;
    EEPROM.update(address,keys[j]);
    button_bindings[i][j]=keys[j];
    
    //Serial.print(button_bindings[i][j]);
    //Serial.println(int(keys[j]));

    j++;
  }

  if(j<button_limit-1){
    EEPROM.write(address+1,0);
    button_bindings[i][j]=0;
  }

  //Serial.print("button_bindings: ");
  //Serial.println(button_bindings[i]);
  //Serial.println(i);
}


void clearEEPROM(){
  /*
  If you start your application for the first time you can reset
  your EEProm and post Null characters for a good start 
  */
  int j;
  int address;
  for(int i=0; i<16; i++){
    j=0;
    while(j<button_limit){
      address= (i*button_limit)+j ;
      EEPROM.update(address,0); /////////////////
      j++;
    }
  }
}

void buttonPressed(char button_value){
  uint8_t j=0;
  bool hotkey_flag=false;

  //Serial.print("Button value: ");
  //Serial.println(button_value);


  //Serial.print("Data need to write: ");
  //Serial.println(button_bindings[button_value-48]);

  while(button_bindings[button_value-48][j]!=0 && j<button_limit){
    
    if(button_bindings[button_value-48][j]==2){
      hotkey_flag = !hotkey_flag;

      if(hotkey_flag==false){
        Keyboard.releaseAll();
      }
      
    }


    if(button_bindings[button_value-48][j]!=2 && hotkey_flag== false){
      
      Keyboard.releaseAll();
      //Serial.print(button_bindings[button_value-48][j]);
      //Keyboard.press(button_bindings[button_value-48][j]); 
      pressButton(button_bindings[button_value-48][j]);
    }
    else if(button_bindings[button_value-48][j]!=2 ){
      //Serial.print(button_bindings[button_value-48][j]);
      //Keyboard.press(button_bindings[button_value-48][j]);
      pressButton(button_bindings[button_value-48][j]);
    }

    j++;
    delay(10); // You can extend the time 
  }
  Keyboard.releaseAll();

}

void pressButton(char button){

   unsigned char tmp2= unsigned(button);
  /*
  if(button<modifier_keys[0].button_value){
    Serial.println("Pressed there");
    Keyboard.press(button);
  }

  else{
    */

   //Serial.println(int(button));
   //Serial.println(int(tmp2));

    for(int i =0; i<35;i++){
      //Serial.println(modifier_keys[i].button_value);
      //Serial.println(modifier_keys[i].button_name);
      if(tmp2==modifier_keys[i].button_value){
        
          //Serial.print("Pressed button: ");
          //Serial.println(modifier_keys[i].button_name.c_str());
          //Serial.println(int(modifier_keys[i].button_value));

          char* tmp=(char*) modifier_keys[i].button_value;
          Keyboard.press(tmp);
          return;
      }
    }
    //Serial.print("Non modifier key");
    Keyboard.press(button);
  //}
}

