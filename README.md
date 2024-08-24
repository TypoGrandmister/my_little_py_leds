# my_little_py_leds
my little project for controlling leds

the code is split into 2<br />
python FFT for note detection and updating the ESP for new notes/change in volume of tone/note stoped playing<br />
CPP in ESP32 is in charge of the effects<br />
to do:<br />
  ~~add multipule ESPs suppert (more leds require more ESPs), just change the socket sendto to a diffrent IP<br />
  ~~check how stable PWM is, works well enough for the untrained eye, (might have flash banged my self too)<br />
  add loop back without VB cable <br />
  add low pass step response in the ESP32 effects, maybe pre set effects too?<br />
  add schamitcs for leds, should i?<br /><br />

fetures so far:<br />
  adding more ESPs is not hard, just change the sendto IP<br />
  software PWM channles, non of that 9 channel limit rubish! (non tested 19 cahnnels so far)<br />
