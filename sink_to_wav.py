import numpy as np
from scipy.io.wavfile import write

class SinkToWav:
    def __init__(self, filename, sample_rate):
        self.filename = filename
        self.sample_rate = sample_rate

    def writeWav(self, data):
        data = np.array(data)
        write("{}.wav".format(self.filename), self.sample_rate, data.astype(np.float32))