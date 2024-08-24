# my_little_py_leds
my little project for controlling leds

the code is split into 2__
python FFT for note detection and updating the ESP for new notes/change in volume of tone/note stoped playing__
CPP in ESP32 is in charge of the effects__
to do:__
  ~~add multipule ESPs suppert (more leds require more ESPs), just change the socket sendto to a diffrent IP__
  ~~check how stable PWM is, works well enough for the untrained eye, (might have flash banged my self too)__
  add loop back without VB cable __
  add low pass step response in the ESP32 effects, maybe pre set effects too? __
  add schamitcs for leds, should i?__

fetures so far:__
  adding more ESPs is not hard, just change the sendto IP__
  software PWM channles, non of that 9 channel limit rubish! (non tested 19 cahnnels so far)__
