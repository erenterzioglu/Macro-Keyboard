# Macro Keyboard Microcontroller
Files that here need to upload to microcontroller. There are two ways to upload
it. If you using Arduino IDE you can use "for ArduinoIDE" folder. If you
using PlatformIO you can use "for PlatformIO" folder.

## Functions that used in microcontroller and general information about that

* clearEEPROM(): Clears EEPROM from old values
* writeEEPRom(): Writing new values that comes from PC.
* readEEPROM(): When device starts, takes bindings that lastly remain in keyboard.
* buttonPressed(): When a button press, handles bindings.
* pressButton(): When button is modifier or not it handles. 
