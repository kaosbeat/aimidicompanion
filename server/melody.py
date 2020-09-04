#impot midi
import mido
from mido import Message, MidiFile, MidiTrack
import pretty_midi
import note_seq
import time
from io import BytesIO

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

print(' Done!')



inport = mido.open_input('Axoloti Core:Axoloti Core MIDI 1 20:0')
outport = mido.open_output('Axoloti Core:Axoloti Core MIDI 1 20:0')
lasttime = time.time()


mid = MidiFile(type=0)
midmemfile = BytesIO()
track = MidiTrack()
mid.tracks.append(track)


def resetMidiFile():
    global mid
    global track
    mid = MidiFile(type=0)
    # midmemfile = BytesIO()
    track = MidiTrack()
    mid.tracks.append(track)

resetMidiFile()

notes = {}
recording = False
ticks = 0
lastticks = 0

ewiseq = music_pb2.NoteSequence()


def midinotes2noteseq(data):
    midi_data = pretty_midi.PrettyMIDI(BytesIO(b''.join([v.to_bytes(1,'big') for v in values])))


def print_message(msg):
    global ticks
    global lastticks
    global notes
    global recording
    global ewiseq
    global mid
    global track
    notetime = time.time()
    ticks = ticks + 1
    # print(msg)
    if  (msg.type == 'note_on' or msg.type == 'note_off'):
        deltaticks = ticks-lastticks

    if  (msg.type == 'note_on'):
        print(msg)

        notetick = ticks
        if (msg.note == 70 and recording == True):
            recording = False
            print ("STOPPING recording!")
            # mid.save(file=midmemfile)
            # midmemfile.close()
            mid.save('test.mid')
            # print(midmemfile)

            # print(pretty_midi.PrettyMIDI(midmemfile))
            ewiseq = magenta.music.midi_io.midi_file_to_sequence_proto('test.mid')
            print ("generating NOTES")
            startgen = time.time()
            magenta.music.midi_io.sequence_proto_to_midi_file(generatestuff(ewiseq), 'output.mid')
            outputfile = MidiFile('output.mid')

            print ("generating took" + str(time.time() - startgen) + "sec")
            print ("playing notes")
            for msg in outputfile.play():
                outport.send(msg)
            resetMidiFile()



        else:
            recording = True
            print ("recording!")
            ewiseq = music_pb2.NoteSequence()

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


    if  (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)):
        if (recording == True):
            track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=deltaticks ))


        # print ("we're having a " + str(msg.type)  + " note_off")


def generatestuff(input_sequence):

    # Model options. Change these to get different generated sequences! 

    # ewiseq in our case input_sequence = twinkle_twinkle # change this to teapot if you want
    num_steps = 128 # change this for shorter or longer sequences
    temperature = 1.0 # the higher the temperature the more random the sequence.

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
    generated_sequence = melody_rnn.generate(input_sequence, generator_options)
    return generated_sequence
    # output = tempfile.NamedTemporaryFile()
    # magenta.music.midi_io.sequence_proto_to_midi_file(generated_sequence, output.name)
    # output.seek(0)
    # return output




inport.callback = print_message

outport.send(mido.Message('note_on', note=50, velocity=113, time=6.2))



while True:
    # print("awaiting msg")
    
    # for msg in inport.iter_pending():
    #     print(msg)

    # do_other_stuff()

    if recording == True:
        #append notes and delta
        # print("ticks = " + str(ticks))
        pass


# msg = port.receive()


