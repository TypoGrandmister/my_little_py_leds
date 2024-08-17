


from socket import *
import pyaudio
import numpy as np
import time

#record
chunk = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 40
thread_count =10
notes={}
prev_notes={}
free=False

port=9988
ip_esp='192.168.137.23'

UDP_socket = socket(AF_INET, SOCK_DGRAM)
UDP_socket.bind(("192.168.137.1",9988))

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
                    update_notes(notes,'0',buf)
                if (i*freq_res<75) and (i*freq_res>40):# mid_bass
                    update_notes(notes,'1',buf)
                if (i*freq_res<120) and (i*freq_res>75):# high_bass
                    update_notes(notes,'2',buf)
                if (i*freq_res<180) and (i*freq_res>120):# B2-F3
                    update_notes(notes,'3',buf)
                if (i*freq_res<250) and (i*freq_res>180):# F#3-B3
                    update_notes(notes,'4',buf)
                if (i*freq_res<320) and (i*freq_res>250):#C4-D#4
                    update_notes(notes,'5',buf)
                if (i*freq_res<450) and (i*freq_res>320):#E4-A4
                    update_notes(notes,'6',buf)
                if (i*freq_res<575) and (i*freq_res>450):#A#4-C#5
                    update_notes(notes,'7',buf)
                if (i*freq_res<750) and (i*freq_res>575):#D5-F#5
                    update_notes(notes,'8',buf)
                if (i*freq_res<1150) and (i*freq_res>750):#G5-C#6
                    update_notes(notes,'9',buf)
                if (i*freq_res<1600) and (i*freq_res>1150):#D6-G6
                    update_notes(notes,':',buf)
                if (i*freq_res<2200) and (i*freq_res>1600):#G#6-C7
                    update_notes(notes,';',buf)
                if (i*freq_res<3750) and (i*freq_res>2200):#C#7-A#7
                    update_notes(notes,'<',buf)
                if (i*freq_res<4600) and (i*freq_res>3750):#B7-C#8
                    update_notes(notes,'=',buf)
                if (i*freq_res<10000) and (i*freq_res>4600):#high1
                    update_notes(notes,'>',buf)
                if (i*freq_res>10000):#high2
                    update_notes(notes,'?',buf)
        for i in notes:
            if i in prev_notes:
                if (notes[i]>prev_notes[i]*1.25):
                    UDP_socket.sendto(str.encode(i+"L"),(ip_esp,port))
                if (notes[i]<prev_notes[i]*0.75):
                    UDP_socket.sendto(str.encode(i+"Q"),(ip_esp,port))
            else:
                UDP_socket.sendto(str.encode(i+"N"),(ip_esp,port))
        for i in prev_notes:
            if not (i in notes):
                UDP_socket.sendto(str.encode(i+"R"),(ip_esp,port))
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
            time.sleep(0.1)
    except KeyboardInterrupt:
        stream.stop_stream()
        UDP_socket.close()
        stream.close()
        p.terminate()
