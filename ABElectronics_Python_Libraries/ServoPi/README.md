AB Electronics UK Servo Pi Python Library
=====

Python Library to use with Servo Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/ServoPi/demos  

### Downloading and Installing the library

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

To install the python library navigate into the ABElectronics_Python_Libraries folder and run:  

For Python 2.7:
```
sudo python setup.py install
```
For Python 3.4:
```
sudo python3 setup.py install
```

If you have PIP installed you can install the library directly from github with the following command:

For Python 2.7:
```
sudo python2.7 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

For Python 3.4:
```
sudo python3.4 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

The Servo Pi library is located in the ServoPi directory

The library requires python-smbus to be installed.  
For Python 2.7:
```
sudo apt-get install python-smbus
```
For Python 3.4:
```
sudo apt-get install python3-smbus
```

# Class: PWM #

The PWM class provides control over the pulse-width modution outputs on the PCA9685 controller.  Functions include setting the frequency and duty cycle for each channel.  

Initialise with the I2C address for the Servo Pi.

```
pwmobject = PWM(0x40)
```

Functions:
----------

```
set_pwm_freq(freq) 
```
Set the PWM frequency  
**Parameters:** freq - required frequency  
**Returns:** null  

```
set_pwm(channel, on, off) 
```
Set the output on single channels  
**Parameters:** channel - 1 to 16, on - time period, off - time period  
**Returns:** null  


```
set_all_pwm( on, off) 
```
Set the output on all channels  
**Parameters:** on - time period, off - time period  
**Returns:** null  

```
output_disable()
```
Disable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
output_enable()
```
Enable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
set_allcall_address(address)
```
Set the I2C address for the All Call function  
**Parameters:** address  
**Returns:** null  

```
enable_allcall_address()
```
Enable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

```
disable_allcall_address()
```
Disable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

# Class: Servo #

The Servo class provides functions for controlling the position of servo motors commonly used on radio control models and small robots.  The Servo class initialises with a default frequency of 50Hz and low and high limits of 1ms and 2ms.

Initialise with the I2C address for the Servo Pi.

```
servo_object = Servo(0x40)
```
**Optional Parameters:**  
low_limit = Pulse length in milliseconds for the lower servo limit.  
high_limit = Pulse length in milliseconds for the upper servo limit.  

Functions:
----------

```
move(channel, position, steps=250) 
```
Set the servo position  
**Parameters:** 
channel - 1 to 16  
position - value between 0 and the maximum number of steps.  
steps (optional) - The number of steps between the the low and high servo limits.  This is preset at 250 but can be any number between 0 and 4095.  On a typical RC servo a step value of 250 is recommended.  
**Returns:** null  

```
set_low_limit(low_limit)
```
Set the pulse length for the lower servo limits.  Typically around 1ms.  
**Parameters:** low_limit - Pulse length in milliseconds for the lower servo limit.  
**Returns:** null  
```
set_high_limit(high_limit)
```
Set the pulse length for the upper servo limits.  Typically around 1ms.  
**Parameters:** high_limit - Pulse length in milliseconds for the upper servo limit.  
**Returns:** null  
```
set_frequency(freq) 
```
Set the PWM frequency  
**Parameters:** freq - required frequency for the servo.  
**Returns:** null  

```
output_disable()
```
Disable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
output_enable()
```
Enable the output via OE pin  
**Parameters:** null  
**Returns:** null  

Usage
====

To use the Servo Pi library in your code you must first import the library:
```
from ServoPi import PWM
```
Next you must initialise the ServoPi object:
```
pwm = PWM(0x40)
```
Set PWM frequency to 60 Hz
```
pwm.set_pwm_freq(60)  
pwm.output_enable()  
```
Set three variables for pulse length
```
servoMin = 250  # Min pulse length out of 4096
servoMed = 400  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096
```
Loop to change the duty cycle on pin 1 between three points
```
while True:
  pwm.set_pwm(1, 0, servoMin)
  time.sleep(0.5)
  pwm.set_pwm(1, 0, servoMed)
  time.sleep(0.5)
  pwm.set_pwm(1, 0, servoMax)
  time.sleep(0.5)

