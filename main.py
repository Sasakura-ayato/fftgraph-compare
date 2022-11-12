import wave

import matplotlib.pyplot as plt
import numpy as np
import pyaudio

# Parameter: Recording
StreamResolution = pyaudio.paInt16
channel = 1
SamplingRate = 44100
chunk = 1024 * 50
timer = 3
DeviceNumber = 0
result_file = "./result.wav"
sleep = 0.01


# Parameter: Graph
Line_x = np.linspace(0, SamplingRate, chunk)
chunk_x2 = int(chunk / 2)
Line_x2 = Line_x[0:chunk_x2]

# Initialize
audio = pyaudio.PyAudio()

# Make Stream
def makestream():
    stream = audio.open(
        format=StreamResolution,
        rate=SamplingRate,
        channels=channel,
        input_device_index=DeviceNumber,
        input=True,
        frames_per_buffer=chunk,
    )
    return stream


def killstream(stream):
    stream.stop_stream()
    stream.close()
    stream.terminate()


def makefft(stream):
    # Get Sound Data
    data = stream.read(chunk)
    ndarray = np.frombuffer(data, dtype="int16")

    # calculation FFT
    Line_y = np.abs(np.fft.fft(ndarray))
    Line_y2 = Line_y[0:chunk_x2]

    # Show Graph
    plt.plot(Line_x2, Line_y2)
    plt.draw()
    plt.pause(sleep)
    plt.cla()

if __name__ == "__main__":
    stream1 = makestream()
    while True:
        try:
            makefft(stream1)
        except KeyboardInterrupt:
            break

