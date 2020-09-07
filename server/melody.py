#impot midi
import mido
from mido import Message, MidiFile, MidiTrack
import pretty_midi
import note_seq
import time
from io import BytesIO
from random import randint
import math
from pyfiglet import Figlet
global f
f = Figlet(font='slant')


import magenta
from magenta import music
# Import dependencies.
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2

# Initialize the model.
print("Initializing Melody RNN...")
bundle = sequence_generator_bundle.read_bundle_file('basic_rnn.mag')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()
global temperature
temperature = 1.0

print(' Done!')

inport = mido.open_input('Axoloti Core:Axoloti Core MIDI 1 20:0')
# inport = mido.open_input('Midi Through:Midi Through Port-0 14:0')
outport = mido.open_output('Axoloti Core:Axoloti Core MIDI 1 20:0')
# outport = mido.open_output('Midi Through:Midi Through Port-0 14:0')
lasttime = time.time()

global mid
global track
global  ticks
global recording

mid = MidiFile(type=0)
# midmemfile = BytesIO()
track = MidiTrack()
mid.tracks.append(track)
recording = False
currentnote = 0
lastticks = 0
ticks =0
# ewiseq = music_pb2.NoteSequence()
currentscene = 'idlescreen'

def resetMidiFile():
    print("resetting midi")
    global mid
    global track
    global ticks
    # global ewiseq
    mid = MidiFile(type=0)
    # midmemfile = BytesIO()
    track = MidiTrack()
    mid.tracks.append(track)
    ticks = 0
    # ewiseq = music_pb2.NoteSequence()

resetMidiFile()






def print_message(msg):
    global ticks
    global lastticks
    global notes
    global recording
    # global ewiseq
    global mid
    global track
    global currentnote
    global currentscene
    global f
    global temperature
    notetime = time.time()
    ticks = ticks + 1
    if (msg.type == 'control_change'):
        print(msg)
        if (msg.control == 1):
            temperature = float(msg.value)


    if  (msg.type == 'note_on' or msg.type == 'note_off'):
        deltaticks = ticks-lastticks

    if  (msg.type == 'note_on'):
        # print(msg)
        notetick = ticks
        if (msg.note == 70 and recording == True):
            recording = False
            print ("STOPPING recording!")
            print(mid)
            mid.save('test.mid')
            ewiseq = magenta.music.midi_io.midi_file_to_sequence_proto('test.mid')
            # print(len(ewiseq.notes))
            # print ("generating NOTES")
            startgen = time.time()
            magenta.music.midi_io.sequence_proto_to_midi_file(generatestuff(ewiseq), 'output.mid')
            outputfile = MidiFile('output.mid')
            print ("generating took" + str(time.time() - startgen) + "sec")
            print (f.renderText('Playing AI notes'))
            print ("playing notes")
            for msg in outputfile.play():
                outport.send(msg)
            resetMidiFile()
            print (f.renderText('Gimme some input'))



        else:
            recording = True
            # print ("recording!")
            # ewiseq = music_pb2.NoteSequence() 
            currentscene = 'recording'
            # print(currentscene + 'from midievent')
            starttime = time.time()
            starttick = ticks

        if (recording == True):
            # if (starttime - lasttime < 3 ):
            #     #add to tempseq
            #     ewiseq.notes.add(pitch=msg.note, start_time=notetime-starttime, end_time=notetime-starttime+0.5, velocity=msg.velocity)
            #     lasttime = notetime
            #     print("about time")
            # else:
            #     #send out seq and start a new one
            #     print (ewiseq)
            #     print("sending out")
            #     # Ask the model to continue the sequence.
            #     sequence = melody_rnn.generate(ewiseq, generator_options)
            track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=deltaticks))
            currentnote = msg.note 



    if  (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)):
        if (recording == True):
            track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=deltaticks ))


        # print ("we're having a " + str(msg.type)  + " note_off")


def generatestuff(input_sequence):
    global temperature
    # Model options. Change these to get different generated sequences! 

    # ewiseq in our case input_sequence 
    num_steps = 128 # change this for shorter or longer sequences
    # temperature = 1.0 # the higher the temperature the more random the sequence.

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
                    if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm 
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step
    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
    start_time=last_end_time + seconds_per_step,
    end_time=total_seconds)

        # generate the output sequence
    try:
        generated_sequence = melody_rnn.generate(input_sequence, generator_options)
        return generated_sequence

    except magenta.models.shared.events_rnn_model.EventSequenceRnnModelError as e:
        print ('caught something' )
        print (' lower num_steps' + str(total_seconds ))
        resetMidiFile()





inport.callback = print_message
outport.send(mido.Message('note_on', note=50, velocity=113, time=6.2))





while True:

    pass






