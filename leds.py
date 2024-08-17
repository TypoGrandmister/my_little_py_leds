


import socket
import pyaudio
import numpy as np
import os

#record
chunk = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 40
thread_count =10
notes={}
prev_notes={}
free=False

def update_notes(list={},key='',val=int):
    if (key in list):
        if list[key]<val:
            list[key]=val
    else:
        list[key]=val



def call(data,frame_cout,time,stat_flag):
    freq_res=RATE/frame_cout
    data_int=[]
    for i in range(frame_cout):
        data_int.append(int.from_bytes(data[(2*i):(2*i)+2],"little",signed=True))

    avg=sum(data_int)/frame_cout
    for i in range(frame_cout):
        data_int[i-1]=data_int[i-1]-avg

    fft_val=np.fft.fft(data_int)
    spectrum=(np.sqrt((fft_val.real*fft_val.real)+(fft_val.imag*fft_val.imag)))
    global notes
    global prev_notes
    global free
    prev_notes=notes
    notes={}
    ma=max(spectrum)
    meh=ma/2
    if (meh>2e4):
        for i in range(int(frame_cout)):
            if (spectrum[i]>meh):
                buf=spectrum[i]/ma
                if (i*freq_res<40):#low bass
                    update_notes(notes,'low_bass',buf)
                if (i*freq_res<75) and (i*freq_res>40):# mid_bass
                    update_notes(notes,'mid_bas',buf)
                if (i*freq_res<120) and (i*freq_res>75):# high_bass
                    update_notes(notes,'high_bass',buf)
                if (i*freq_res<180) and (i*freq_res>120):# B2-F3
                    update_notes(notes,'B2-F3',buf)
                if (i*freq_res<250) and (i*freq_res>180):# F#3-B3
                    update_notes(notes,'F#3-B3',buf)
                if (i*freq_res<320) and (i*freq_res>250):#C4-D#4
                    update_notes(notes,'C4-D#4',buf)
                if (i*freq_res<450) and (i*freq_res>320):#E4-A4
                    update_notes(notes,'E4-A4',buf)
                if (i*freq_res<575) and (i*freq_res>450):#A#4-C#5
                    update_notes(notes,'A#4-C#5',buf)
                if (i*freq_res<750) and (i*freq_res>575):#D5-F#5
                    update_notes(notes,'D5-F#5',buf)
                if (i*freq_res<1150) and (i*freq_res>750):#G5-C#6
                    update_notes(notes,'G5-C#6',buf)
                if (i*freq_res<1600) and (i*freq_res>1150):#D6-G6
                    update_notes(notes,'D6-G6',buf)
                if (i*freq_res<2200) and (i*freq_res>1600):#G#6-C7
                    update_notes(notes,'G#6-C7',buf)
                if (i*freq_res<3750) and (i*freq_res>2200):#C#7-A#7
                    update_notes(notes,'C#7-A#7',buf)
                if (i*freq_res<4600) and (i*freq_res>3750):#B7-C#8
                    update_notes(notes,'B7-C#',buf)
                if (i*freq_res<10000) and (i*freq_res>4600):#high1
                    update_notes(notes,'high1',buf)
                if (i*freq_res>10000):#high2
                    update_notes(notes,'high2',buf)
    free=True
    return('\xff',pyaudio.paContinue)


if __name__=='__main__':

    p = pyaudio.PyAudio()

    def_device=p.get_default_input_device_info()
    device_index = def_device['index']
    print("using:")
    print(def_device['name'])


    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    stream_callback=call,
                    frames_per_buffer=chunk
                    )

    
    try:
        while(1):
            if free:
               free=False
#               print('\n'*235)
               for i in notes:
                   if i in prev_notes:
                        if (notes[i]>prev_notes[i]*1.25):
                            print(i+"is loader!")
                        if (notes[i]<prev_notes[i]*0.75):
                            print(i+"is quiter~")
                   else:
                        print(i+"is new~~")
               for i in prev_notes:
                   if not (i in notes):
                       print(i+"was removed")
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
