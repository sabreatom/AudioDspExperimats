import pytest
import morphing_oscillator as mo
import math

SAMPLE_RATE = 44100

def test_angleStepEqual50():
    dut = mo.MorphingOscillator(SAMPLE_RATE, 50)
    assert dut.getAngleStep() == (2 * math.pi * 50 / SAMPLE_RATE)


def test_angleStepEqual1000():
    dut = mo.MorphingOscillator(SAMPLE_RATE, 1000)
    assert dut.getAngleStep() == (2 * math.pi * 1000 / SAMPLE_RATE)


def test_angleStepEqual10000():
    dut = mo.MorphingOscillator(SAMPLE_RATE, 10000)
    assert dut.getAngleStep() == (2 * math.pi * 10000 / SAMPLE_RATE)


def test_generateSquareHigh():
    dut = mo.MorphingOscillator(SAMPLE_RATE, 100)
    assert dut.generateSquare(1.0, 0.0) == 1.0


def test_generateSquareLow():
    dut = mo.MorphingOscillator(SAMPLE_RATE, 100)
    assert dut.generateSquare(1.0, 1.5 * math.pi) == 0.0


def test_generateSquareMultiplePeriod():
    dut = mo.MorphingOscillator(SAMPLE_RATE, 100)
    assert dut.generateSquare(1.0, 11.5 * math.pi) == 0.0