# Sentinelle

## Here is the Programme Sentinelle
It monitors your computer's statistics and alerts you in case of high usage.  Also monitors the temperature, and warns you in the event of a high temperature.

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
 
  ## You may want to compile yourself the Programme Sentnelle

  pip3 install pyinstaller

  pyinstaller --onefile --windowed --icon=sentinelle.ico --add-data "sentinelle.ico;sentinelle.ico" sentinelle.py
