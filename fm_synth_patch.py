import morphing_oscillator as mp
import sink_to_wav as sw
import math
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt

if __name__== "__main__":
    lfo = mp.MorphingOscillator(44100, 5)
    lfo.setWaveformMix(mp.OscWfr.TRIANGLE, 1.0)
    lfo.setAmplitude(1.0)

    dut = mp.MorphingOscillator(44100, 50)
    dut.setWaveformMix(mp.OscWfr.SINE, 1.0)
    dut.setAmplitude(0.8)
    dut.setPmCallback(lfo.generateWaveform)
    dut.setPmAmplitude(math.pi / 2)
    dut.setPmState(True)

    test = dut.generateWaveform(5 * 44100)

    sink_wav = sw.SinkToWav("fm_synth_patch", 44100)
    sink_wav.writeWav(test)

    plt.plot(test)
    plt.show()