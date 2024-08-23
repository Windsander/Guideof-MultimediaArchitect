import tkinter as tk
from tkinter import filedialog
import numpy as np
import soundfile as sf
import pyaudio
import threading
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Audio Player")

        # Initialize pyaudio
        self.pyaudio_instance = pyaudio.PyAudio()

        # Create control buttons frame
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_audio)
        self.stop_button.pack(side=tk.LEFT)

        self.play_pause_button = tk.Button(self.control_frame, text="Play", command=self.toggle_play_pause)
        self.play_pause_button.pack(side=tk.LEFT)

        self.open_button = tk.Button(self.control_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)

        self.playing = False
        self.audio_data = None
        self.fs = None
        self.current_frame = 0
        self.stream = None

        # Create matplotlib figure and axes for waveform display
        self.fig, self.ax_waveform = plt.subplots(figsize=(6, 3.6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create progress bar
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(side=tk.TOP, fill=tk.X)
        self.progress_bar = tk.Scale(self.progress_frame, from_=0, to=1000, orient=tk.HORIZONTAL, showvalue=0)
        self.progress_bar.pack(fill=tk.X, expand=True)

        # Timer to update waveform line
        self.update_interval = 1  # milliseconds

        # Create thread event to stop update thread
        self.update_thread_event = threading.Event()

        # Queue for inter-thread communication
        self.queue = queue.Queue()

        # Flag variable to detect if the progress bar is being dragged
        self.is_seeking = False
        self.was_playing = False  # Mark the playback state when seeking

        # Bind events
        self.progress_bar.bind("<Button-1>", self.on_seek_start)
        self.progress_bar.bind("<ButtonRelease-1>", self.on_seek_end)
        self.progress_bar.bind("<B1-Motion>", self.on_seek)

        # Start thread to update progress bar
        self.root.after(self.update_interval, self.update_progress_bar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac *.mp3")])
        if file_path:
            self.audio_data, self.fs = sf.read(file_path, dtype='float32')
            self.current_frame = 0
            duration = len(self.audio_data) / self.fs
            self.progress_bar.config(to=duration * 1000)  # Set the maximum value of the progress bar to the audio duration in milliseconds
            self.play_pause_button.config(text="Play")
            self.playing = False
            self.plot_waveform()

    def toggle_play_pause(self):
        if self.playing:
            self.play_pause_button.config(text="Play")
            self.playing = False
            self.pause_audio()
            self.update_thread_event.set()  # Stop update thread
        else:
            self.play_pause_button.config(text="Pause")
            self.playing = True
            self.update_thread_event.clear()  # Clear update thread event
            threading.Thread(target=self.play_audio).start()

    def audio_callback(self, in_data, frame_count, time_info, status):
        end_frame = self.current_frame + frame_count
        data = self.audio_data[self.current_frame:end_frame].tobytes()
        self.current_frame = end_frame
        self.queue.put(end_frame / self.fs * 1000)  # Current time (milliseconds)
        if self.current_frame >= len(self.audio_data):
            return (data, pyaudio.paComplete)
        return (data, pyaudio.paContinue)

    def pause_audio(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def play_audio(self):
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paFloat32,
            channels=self.audio_data.shape[1],
            rate=self.fs,
            output=True,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()

    def stop_audio(self):
        self.playing = False
        self.current_frame = 0
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.play_pause_button.config(text="Play")
        # Reset the red line to the beginning
        self.update_thread_event.set()  # Stop update thread
        self.plot_waveform()  # Reset waveform plot
        self.progress_bar.set(0)

    def plot_waveform(self):
        self.ax_waveform.clear()
        time_axis = np.linspace(0, len(self.audio_data) / self.fs, num=len(self.audio_data))
        self.ax_waveform.plot(time_axis, self.audio_data)
        self.ax_waveform.set_title("Waveform")
        self.ax_waveform.set_xlabel("Time (s)")  # Set x-axis label to seconds
        self.ax_waveform.set_ylabel("Amplitude")
        self.canvas.draw()

    def update_progress_bar(self):
        try:
            while not self.queue.empty():
                current_time = self.queue.get_nowait()
                if not self.is_seeking:  # Only update when not dragging the progress bar
                    self.progress_bar.set(current_time)
        except queue.Empty:
            pass
        self.root.after(self.update_interval, self.update_progress_bar)

    def on_seek_start(self, event):
        self.was_playing = self.playing  # Record the playback state when seeking
        if self.playing:
            self.toggle_play_pause()  # Pause playback
        self.is_seeking = True  # Mark that the progress bar is being dragged

    def on_seek(self, event):
        # Update current_frame in real-time
        value = self.progress_bar.get()
        self.current_frame = int(float(value) / 1000 * self.fs)

    def on_seek_end(self, event):
        self.is_seeking = False  # Mark that dragging has ended
        self.plot_waveform()  # Update waveform plot
        if self.was_playing:  # If it was playing before, resume playback
            self.toggle_play_pause()

    def seek(self, value):
        if self.audio_data is not None:
            self.current_frame = int(float(value) / 1000 * self.fs)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()