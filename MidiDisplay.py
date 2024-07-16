# from visual_midi import Plotter
# from visual_midi import Preset
# from pretty_midi import PrettyMIDI
#
# # Loading a file on disk using PrettyMidi, and show
# pm = PrettyMIDI("Output_Audio/Bob.mid")
# plotter = Plotter()
# plotter.show(pm, "/tmp/example-01.html")

from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

# Using the `Preset` and `Plotter` to customize appearance (smaller plot)
pm = PrettyMIDI("Output_Audio/raw_.mid")
# preset = Preset(plot_width=850)
# plotter = Plotter(preset, plot_max_length_bar=4)
plotter = Plotter()
plotter.show(pm, "example-01.html")
