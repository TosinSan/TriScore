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
    note_frames = {}
    for i in range(len(data)):
        frame_data = noise_filter(data[i], freq_list, level)
        for note in frame_data:
            n_pitch = f2n(note[1])
            n_vol = int(note[0]*100)
            n_time = i
            try:
                note_frames[n_pitch].append((n_time, n_vol))
            except KeyError:
                note_frames[n_pitch] = [(n_time, n_vol)]
    notes = smooth(note_frames, tstep, 10)
    return notes

# Utilizing the Overlapping Note Ansatz:
def smooth(note_book, tstep, sn):
    notes = []
    for pitch in note_book:
        stnote = note_book[pitch][0]
        for i in range(len(note_book[pitch]) - 1):
            if (note_book[pitch][i+1][0] - note_book[pitch][i][0]) > sn \
                    or sn < (note_book[pitch][i][1] - note_book[pitch][i + 1][1]):
                notes.append((pitch, stnote[0], note_book[pitch][i][0] - stnote[0], stnote[1]))
                stnote = note_book[pitch][i+1]
        notes.append((pitch, stnote[0]*tstep, (note_book[pitch][-1][0] - stnote[0])*tstep, stnote[1]))
    return notes


def raw_transcribe(data, fts, freq_axis, f_name):

    mfile = MIDIFile()
    track = 0
    time = 0    # start at the beginning
    mfile.addTrackName(track, time, "Sample Track")
    mfile.addTempo(track, time, 60)
    mfile.addProgramChange(0, 0, 0, 81)

    pdata = frames_to_notes(data, freq_axis, fts)
    channel = 0
    for note in pdata:
        mfile.addNote(track, channel, *note)

    # write it to disk
    with open(f"Output_Audio/{f_name}.mid", 'wb') as file:  # wb is writing to binary? we cool like that
        mfile.writeFile(file)

### Test ###

