import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from librosa import display
import librosa

# Visualize an STFT power spectrum
def spectrogram_plot(sound_path):
    y, sr = librosa.load(sound_path)
    plt.figure(figsize=(12, 8))

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.subplot(4, 2, 1)
    librosa.display.specshow(D, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear-frequency power spectrogram')

    # Or on a logarithmic scale

    plt.subplot(4, 2, 2)
    librosa.display.specshow(D, y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log-frequency power spectrogram')

    # Or use a CQT scale

    CQT = librosa.amplitude_to_db(np.abs(librosa.cqt(y, sr=sr)), ref=np.max)
    plt.subplot(4, 2, 3)
    librosa.display.specshow(CQT, y_axis='cqt_note')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (note)')

    plt.subplot(4, 2, 4)
    librosa.display.specshow(CQT, y_axis='cqt_hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (Hz)')

    # Draw a chromagram with pitch classes

    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    plt.subplot(4, 2, 5)
    librosa.display.specshow(C, y_axis='chroma')
    plt.colorbar()
    plt.title('Chromagram')

    # Force a grayscale colormap (white -> black)

    plt.subplot(4, 2, 6)
    librosa.display.specshow(D, cmap='gray_r', y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear power spectrogram (grayscale)')

    # Draw time markers automatically

    plt.subplot(4, 2, 7)
    librosa.display.specshow(D, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log power spectrogram')

    # Draw a tempogram with BPM markers

    plt.subplot(4, 2, 8)
    Tgram = librosa.feature.tempogram(y=y, sr=sr)
    librosa.display.specshow(Tgram, x_axis='time', y_axis='tempo')
    plt.colorbar()
    plt.title('Tempogram')
    plt.tight_layout()
    plt.show()

    # Draw beat-synchronous chroma in natural time

    # plt.figure()
    # tempo, beat_f = librosa.beat.beat_track(y=y, sr=sr, trim=False)
    # beat_f = librosa.util.fix_frames(beat_f, x_max=C.shape[1])
    # Csync = librosa.util.sync(C, beat_f, aggregate=np.median)
    # beat_t = librosa.frames_to_time(beat_f, sr=sr)
    # ax1 = plt.subplot(2, 1, 1)
    # librosa.display.specshow(C, y_axis='chroma', x_axis='time')
    # plt.title('Chroma (linear time)')
    # ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    # librosa.display.specshow(Csync, y_axis='chroma', x_axis='time',
    #                          x_coords=beat_t)
    # plt.title('Chroma (beat time)')
    # plt.tight_layout()
    # plt.show()


def time_domain_plot(sound_path):
    y, sr = librosa.load(sound_path, duration=10)
    plt.figure()
    plt.subplot(3, 1, 1)
    librosa.display.waveshow(y, sr=sr)
    plt.title('Monophonic')

    # Or a stereo waveform

    y, sr = librosa.load(sound_path, mono=False, duration=10)
    plt.subplot(3, 1, 2)
    librosa.display.waveshow(y, sr=sr)
    plt.title('Stereo')

    # Or harmonic and percussive components with transparency

    y, sr = librosa.load(sound_path, duration=10)
    y_harm, y_perc = librosa.effects.hpss(y)
    plt.subplot(3, 1, 3)
    librosa.display.waveshow(y_harm, sr=sr, alpha=0.25)
    librosa.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5)
    plt.title('Harmonic + Percussive')
    plt.tight_layout()
    plt.show()

def frequency_loudness_at(sound_path, timestamp_at):
    y, sr = librosa.load(sound_path, offset=timestamp_at, duration=0.01)
    stft = librosa.stft(y, n_fft=2048, hop_length=512)
    magnitudes = np.mean(np.abs(stft), axis=1)
    frequencies = librosa.core.fft_frequencies(sr=sr, n_fft=2048)

    # Plot the FRC
    plt.plot(frequencies, magnitudes)
    plt.xlabel("Hz")
    plt.ylabel("SPL (dB)")
    plt.show()

sound_path = 'A440_instruments_A4.wav' #librosa.util.example_audio_file()
#sound_path = 'A440_standard_A4.wav' #librosa.util.example_audio_file()
y, sr = librosa.load(sound_path)
plt.figure()
librosa.display.waveshow(y, sr=sr, color='r')
plt.show()
#spectrogram_plot(sound_path)
#time_domain_plot(sound_path)
frequency_loudness_at(sound_path, 5)
