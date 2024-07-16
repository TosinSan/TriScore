from midiutil.MidiFile import MIDIFile
import numpy as np

def f2n(f):
    f = max(f, 1)
    return int(12 * (np.log(f / 220) / (np.log(2))) + 57)


def noise_filter(raw_data, freq_list, level):
    pdata = []
    for i in range(len(raw_data)):
        if raw_data[i] > level:
            pdata.append((raw_data[i], freq_list[i]))  # Maybe multiplication instead
    return pdata


def frames_to_notes(data, freq_list, tstep, level=0.5):
    note_frames = []
    for i in range(len(data)):
        frame_data = noise_filter(data[i], freq_list, level)
        for note in frame_data:
            n_pitch = f2n(note[1])
            n_vol = int(note[0]*100)
            n_time = i*tstep
            note_frames.append([n_pitch, n_time, 1*tstep, n_vol])
    return note_frames


def raw_transcribe(data, fs, freq_axis, f_name):

    mfile = MIDIFile()
    track = 0
    time = 0    # start at the beginning
    mfile.addTrackName(track, time, "Sample Track")
    mfile.addTempo(track, time, 1)
    mfile.addProgramChange(0, 0, 0, 81)

    pdata = frames_to_notes(data, freq_axis, 1/fs)
    channel = 0
    for note in pdata:
        mfile.addNote(track, channel, *note)

    # write it to disk
    with open(f"Output_Audio/{f_name}.mid", 'wb') as file:  # wb is writing to binary? we cool like that
        mfile.writeFile(file)

### Test ###

