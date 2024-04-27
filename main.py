import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import numpy as np
import simpleaudio as sa

def generate_binaural_beats(base_freq, beat_freq, duration_ms,file_name, volume=0.5):
    # Define sample rate and duration
    sample_rate = 44100  # Standard CD quality sample rate
    duration_s = duration_ms / 1000.0
    
    # Calculate the frequency for each ear
    freq_left = base_freq - beat_freq / 2
    freq_right = base_freq + beat_freq / 2
    
    # Generate sample index
    samples = np.arange(duration_s * sample_rate) / sample_rate
    
    # Generate sine wave for the left and right channels
    wave_left = np.sin(2 * np.pi * freq_left * samples) * (2**15 - 1) * volume
    wave_right = np.sin(2 * np.pi * freq_right * samples) * (2**15 - 1) * volume
    
    # Ensure the wave is in 16-bit format
    audio_left = wave_left.astype(np.int16)
    audio_right = wave_right.astype(np.int16)

    # Stereo audio
    stereo_wave = np.vstack((audio_left, audio_right)).T
    
    # Convert numpy array to bytes
    stereo_sound = stereo_wave.tobytes()

    # Create pydub audio segment from the raw audio data
    audio_segment = AudioSegment(
        stereo_sound,
        frame_rate=sample_rate,
        sample_width=audio_left.itemsize,
        channels=2
    )
    
    # Export to a WAV file using the provided file name
    audio_segment.export(file_name, format="wav")
    
    # Play the sound
    # wave_obj = sa.WaveObject(audio_segment.raw_data, num_channels=2, bytes_per_sample=audio_segment.sample_width, sample_rate=audio_segment.frame_rate)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()

    return file_name

def save_file():
    # Get the values from the input fields
    base_freq = float(base_freq_entry.get())
    beat_freq = float(beat_freq_entry.get())
    duration_ms = int(duration_ms_entry.get())
    file_name = file_name_entry.get().strip()

    # Validate and modify file_name
    if not file_name:
        file_name = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            title="Save as"
        )
        if not file_name:  # If the user cancelled the save dialog
            return
    else:
        # Ensure the file name ends with .wav
        if not file_name.lower().endswith('.wav'):
            file_name += '.wav'

    # Call the generate function with the provided file name
    actual_file_name = generate_binaural_beats(base_freq, beat_freq, duration_ms, file_name)
    print(f"Generated binaural beats saved as {actual_file_name}")

def playTest():
    generate_binaural_beats(base_freq, beat_freq, duration_ms, '')


# Create the main window
root = tk.Tk()
root.title("Binaural Beats Generator")

# Create and pack the widgets
tk.Label(root, text="Base Frequency (Hz):").pack()
base_freq_entry = tk.Entry(root)
base_freq_entry.pack()

tk.Label(root, text="Beat Frequency (Hz):").pack()
beat_freq_entry = tk.Entry(root)
beat_freq_entry.pack()

tk.Label(root, text="Duration (milliseconds):").pack()
duration_ms_entry = tk.Entry(root)
duration_ms_entry.pack()

tk.Label(root, text="File Name:").pack()
file_name_entry = tk.Entry(root)
file_name_entry.pack()

save_button = tk.Button(root, text="Generate and Save", command=save_file)
save_button.pack()
save_button = tk.Button(root, text="PlayTest", command=save_file)
save_button.pack()

# Run the event loop
root.mainloop()
