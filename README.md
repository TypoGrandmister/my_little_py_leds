# my_little_py_leds
my little project for controlling leds

the code is split into 2
python FFT for note detection and updating the ESP for new notes/change in volume of tone/note stoped playing
CPP in ESP32 is in charge of the effects
to do:
  ~~add multipule ESPs suppert (more leds require more ESPs), just change the socket sendto to a diffrent IP
  ~~check how stable PWM is, works well enough for the untrained eye, (might have flash banged my self too)
  add loop back without VB cable 
  add low pass step response in the ESP32 effects, maybe pre set effects too? 
  add schamitcs for leds, should i?

fetures so far:
  adding more ESPs is not hard, just change the sendto IP
  software PWM channles, non of that 9 channel limit rubish! (non tested 19 cahnnels so far)
