# Programme Sentinelle
## V2
## Here is the Programme Sentinelle
It monitors your computer's statistics and alerts you in case of high usage.  Also monitors the temperature, and warns you in the event of a high temperature.

*****Download the Programme Sentinelle*****

Linux :
* http://51.178.51.166/grise/other/sentinelle (last version : V2)

Windows : 
* hmm. There is not the file for Windows. Please wait some time.

Here is what it do :

* CPU monitoring
* Space left monitoring
* RAM monitoring
* Temperature monitoring (°F and °C)

You can see the current statistics too!
And there is the statistics on one hour. 

there is a boot menu too with :

* Sleep
* Shutdown
* Reboot
* logout

  # Dependencies

  The Programme Sentinelle use Python and need this :

  * Pyside6
  * psutil
 
    ``` pip3 install Pyside6 ```
    ``` pip3 install psutil ```
 
  ## You may want to compile yourself the Programme Sentinelle
  ```pip3 install pyinstaller```

  ```pyinstaller --onefile --noconsole --icon=sentinelle.ico sentinelle.py```

the binarie **will** need the sentinelle.png picture.
# /!\ Please note that the touchscreen option will probably don't work for your computer, and, even if you don't have one, the option will be displayed. For fix that, please wait the next relase.
