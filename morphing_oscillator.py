import math
import matplotlib.pyplot as plt
from enum import Enum

class OscWfr(str, Enum):
    SQUARE = "square"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    SINE = "sine"


class MorphingOscillator:
    def __init__(self, sample_rate, frequency):
        self.__config__ = {}
        self.__config__["mix"] = {}
        self.__config__["sample_rate"] = sample_rate
        self.__config__["frequency"] = frequency
        self.__config__["mix"][OscWfr.SQUARE] = 0.0
        self.__config__["mix"][OscWfr.TRIANGLE] = 0.0
        self.__config__["mix"][OscWfr.SAWTOOTH] = 0.0
        self.__config__["mix"][OscWfr.SINE] = 0.0
        self.__config__["detune"] = 0.0
        self.__config__["amplitude"] = 0.0
        self.__config__["pm_is_enabled"] = False
        self.__config__["pm_amplitude"] = 0.0
        
        self.current_step = 0.0

        self.pm_signal_source_callback = None

    def getAngleStep(self):
        return (self.__config__["frequency"] + self.__config__["detune"]) * 2 * math.pi / self.__config__["sample_rate"]

    def getSawtoothAmplitudeStep(self, amplitude):
        return amplitude / ((2 * math.pi) / self.getAngleStep())
    
    def generateSquare(self, amplitude, angle):
        angle = angle % (2 * math.pi)
        
        if angle < math.pi:
            return amplitude
        else:
            return 0.0

    def generateTriangle(self, amplitude, angle):
        angle = angle % (2 * math.pi)
        angle_step = (2 * amplitude) / math.pi

        if angle < math.pi:
            value = angle * angle_step - amplitude
        else:
            value = amplitude - ((angle - math.pi) * angle_step)

        return value
        
    def generateSawtooth(self, amplitude, angle):
        angle = angle % (2 * math.pi)
        angle_step = amplitude / math.pi

        return angle * angle_step - amplitude

    def generateSine(self, amplitude, angle):
        angle = angle % (2 * math.pi)
        return amplitude * math.sin(angle)
    
    def generateWaveform(self, buffer_size):
        #calculate single waveform amplitudes:
        waveform_amplitudes = {}
        total_amplitude = 0.0
        buffer = [0] * buffer_size
        
        for key in self.__config__["mix"]:
            if self.__config__["mix"][key] > 0.0:
                waveform_amplitudes[key] = self.__config__["mix"][key]
                total_amplitude += self.__config__["mix"][key]

        if total_amplitude > 0.0:
            scale_value = self.__config__["amplitude"] / total_amplitude

        if self.__config__["pm_is_enabled"]:
            pm_signal = self.pm_signal_source_callback(buffer_size)

        #generate samples for buffer:
        for key in waveform_amplitudes:
            waveform_amplitudes[key] *= scale_value
            if key == OscWfr.SQUARE:
                sample_generator = self.generateSquare
                print("Square amplitude is {}".format(waveform_amplitudes[OscWfr.SQUARE]))
            elif key == OscWfr.TRIANGLE:
                sample_generator = self.generateTriangle
                print("Triangle amplitude is {}".format(waveform_amplitudes[OscWfr.TRIANGLE]))
            elif key == OscWfr.SAWTOOTH:
                sample_generator = self.generateSawtooth
                print("Sawtooth amplitude is {}".format(waveform_amplitudes[OscWfr.SAWTOOTH]))
            elif key == OscWfr.SINE:
                sample_generator = self.generateSine
                print("Sine amplitude is {}".format(waveform_amplitudes[OscWfr.SINE]))
            else:
                print("[ERROR] Unknown waveform type detected during generation")
                return None

            for i in range(buffer_size):
                if self.__config__["pm_is_enabled"]:
                    phase = self.current_step + i * self.getAngleStep() + pm_signal[i] * self.__config__["pm_amplitude"]
                else:
                    phase = self.current_step + i * self.getAngleStep()

                buffer[i] += sample_generator(waveform_amplitudes[key], phase)

        self.current_step += buffer_size * self.getAngleStep()

        return buffer

    def setWaveformMix(self, waveform, value):
        if value > 1.0:
            value = 1.0
            print("[WARNING] Mix value larger then 1.0")

        if waveform in OscWfr:
            self.__config__["mix"][waveform] = value
        else:
            print("[ERROR] Unknown waveform")

    def setAmplitude(self, amplitude):
        self.__config__["amplitude"] = amplitude

    def setPmState(self, isEnabled):
        self.__config__["pm_is_enabled"] = isEnabled

    def setPmCallback(self, callback):
        self.pm_signal_source_callback = callback

    def setPmAmplitude(self, amplitude):
        self.__config__["pm_amplitude"] = amplitude


if __name__== "__main__":
    lfo = MorphingOscillator(44100, 5)
    lfo.setWaveformMix(OscWfr.SINE, 1.0)
    lfo.setAmplitude(1.0)

    dut = MorphingOscillator(44100, 50)
    dut.setWaveformMix(OscWfr.SINE, 1.0)
    dut.setAmplitude(1.0)
    dut.setPmCallback(lfo.generateWaveform)
    dut.setPmAmplitude(math.pi / 2)
    dut.setPmState(False)

    test = dut.generateWaveform(44100)

    plt.plot(test)
    plt.show()