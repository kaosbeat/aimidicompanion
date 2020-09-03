import mido
from mido import MidiFile
# from mido.sockets import PortServer, connect

#

##setup midi server ports
# for message in PortServer('10.0.2.15', 8981):
#     print(message)



##config

## listen for midi
## write buffer to file
## call ai-duet
## read output
## play out over midi device



inport = mido.open_input('Axoloti Core:Axoloti Core MIDI 1 20:0')

def print_message(message):
    if  (message.type == 'note_on'):
        print(message)


inport.callback = print_message


recording = False
while True:
    # print("awaiting msg")
    # for msg in inport.iter_pending():
    #     print(msg)

    # do_other_stuff()
    if recording == True:
        #append notes and delta
        print("deltatime = 0")


# msg = port.receive()



from mido import Message, MidiFile, MidiTrack

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=12, time=0))
track.append(Message('note_on', note=64, velocity=64, time=32))
track.append(Message('note_off', note=64, velocity=127, time=32))

mid.save('new_song.mid')