import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import PySimpleGUI as sg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -- Variable --

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
Line_x2 = Line_x[100:chunk_x2]
print(len(Line_x2))

# Initialize
audio = pyaudio.PyAudio()

# -- Define --

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


# Kill Stream
def killstream(stream):
    stream.stop_stream()
    stream.close()
    stream.terminate()


# Reload FFT


def reloadfft(stream):
    # Get Sound Data
    data = stream.read(chunk)
    ndarray = np.frombuffer(data, dtype="int16")

    # calculation FFT
    Line_y = np.abs(np.fft.fft(ndarray))
    Line_y2 = Line_y[100:chunk_x2]

    return Line_x2, Line_y2


# Draw Figure
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


Devices = []
for i in range(audio.get_device_count()):
    device = audio.get_device_info_by_index(i)
    Devices.append(device["name"])

layout = [
    [sg.Text("Fast Fourier Converter")],
    [
        sg.Button("波形表示[↑]"),
        sg.Button("波形表示[↓]"),
        sg.Button("波形固定[↑]"),
        sg.Button("波形固定[↓]"),
        sg.Button("終了"),
    ],
    [sg.Text("キャプチャデバイスを選択")],
    [sg.Combo(Devices, default_value=Devices[0])],
    [sg.Text("[Graph 1]")],
    [sg.Canvas(key="-CANVAS1-")],
    [sg.Text("[Graph 2]")],
    [sg.Canvas(key="-CANVAS2-")],
]

window = sg.Window("sample", layout, finalize=True)
event, values = window.read()

stream1 = makestream()
stream2 = makestream()

eventstatus = {"canvas1status": False, "canvas2status": False}

# Initialize figure1
figure1 = plt.figure(figsize=(8, 4))
ax1 = figure1.add_subplot(111)
fig_agg1 = draw_figure(window["-CANVAS1-"].TKCanvas, figure1)

# Initialize figure2
figure2 = plt.figure(figsize=(8, 4))
ax2 = figure2.add_subplot(111)
fig_agg2 = draw_figure(window["-CANVAS2-"].TKCanvas, figure2)


def reloadCanvas1():
    ax1.cla()
    ax1.plot(reloadfft(stream1)[0], reloadfft(stream1)[1])
    fig_agg1.draw()


def reloadCanvas2():
    ax2.cla()
    ax2.plot(reloadfft(stream2)[0], reloadfft(stream2)[1])
    fig_agg2.draw()


def event():
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == "終了":
            break
        elif event == "波形表示[↑]":
            print("↑d")
            eventstatus["canvas1status"] = True
            reloadCanvas1()
        elif event == "波形表示[↓]":
            print("↓d")
            reloadCanvas2()
            eventstatus["canvas2status"] = True
        elif event == "波形固定[↑]":
            print("↑")
            eventstatus["canvas1status"] = False
        elif event == "波形固定[↓]":
            print("↓")
            eventstatus["canvas2status"] = False
        else:
            print("readstatus")

        if eventstatus["canvas1status"] == True:
            reloadCanvas1()
        elif eventstatus["canvas2status"] == True:
            reloadCanvas2()


event()
window.close()
