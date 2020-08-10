# Macro-Keyboard
Macro Keyboard with adjustable keys

## Features


* Adjust macros what you want to do for each key up to 30 buttons
* Macros saved in EEPROM and it is nonvolatile until the next override
* Hotkey support up to six buttons
* Open for development


## Requirements

### Hardware
* Arduino leonardo or and alternative microcontroller that have internal usb support
* Keypad
* Jumper wires male-male

### Software:

* Arduino ide or Visual Studio Code and PlatformIO add on
* Python and libraries: 
	* [keyboard](https://github.com/boppreh/keyboard) 
	* [pySerial](https://github.com/pyserial/pyserial)
	
* Libraries for arduino development: 
	* [Keypad](https://github.com/Chris--A/Keypad)
	* Arduino platform if you using PlatformIO
	* Keyboard library, EEProm library is pre-installed libraries 


## Features can be added: 

* v-usb support for decrasing cost on microcontroller side.
* Add a bindings valid bit for sending less value on microcontroller.
* Support for accent keys.
* Visual improvements and general improvements on binding application.






