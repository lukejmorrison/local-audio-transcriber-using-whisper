import os  # For file and directory operations
import shutil  # For moving files
import whisper  # For audio transcription
import torch  # Machine learning framework used by Whisper
import warnings  # To suppress warnings
import time  # For timing operations
from pydub import AudioSegment  # For audio file format conversion
from datetime import datetime, timedelta  # For date and time operations
import re  # For regular expression matching
import sys  # For handling command-line arguments

# Script metadata
__appname__ = "Audio Transcriber"
__AppShortDescription__ = "Transcribes audio files into text and SRT subtitles using Open AI Whisper"
__version__ = "0.2"
__author__ = "Luke Morrison/Wizwam"

# Suppress warnings to keep the output clean
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def choose_model(model_number):
    # Map command line option to Whisper model names
    models = ["tiny", "base", "small", "medium", "large"]
    if not (1 <= int(model_number) <= len(models)):
        raise ValueError("Invalid model number. Choose between 1 and 5.")
    return models[int(model_number) - 1]

def convert_audio_to_wav(audio_path):
    # Converts any audio file to WAV format for Whisper compatibility
    audio = AudioSegment.from_file(audio_path)
    wav_path = os.path.splitext(audio_path)[0] + '.wav'
    audio.export(wav_path, format="wav")
    return wav_path

def get_largest_job_number(base_dir):
    # Finds the highest job number in the directory for sequential naming
    job_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_Job(\d+)$')
    max_job = 0
    for folder in os.listdir(base_dir):
        match = job_pattern.match(folder)
        if match:
            job_number = int(match.group(1))
            max_job = max(max_job, job_number)
    return max_job

def create_output_folder(base_dir):
    # Creates a new folder for each transcription job with a unique name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    largest_job = get_largest_job_number(base_dir)
    job_count = largest_job + 1

    while job_count <= largest_job + 1000:  # To prevent infinite loop
        folder_name = f"{timestamp}_Job{job_count}"
        folder_path = os.path.join(base_dir, folder_name)
        try:
            os.makedirs(folder_path)
            return folder_path
        except FileExistsError:
            job_count += 1
        except OSError as e:
            print(f"Error creating directory: {e}")
            job_count += 1

    raise Exception("Could not create a unique folder after 1000 attempts.")

def estimate_transcription_time(audio_duration, model_name):
    # Estimates transcription time based on model size
    estimates = {
        "tiny": 0.5,  # Times faster than real-time
        "base": 1,
        "small": 2,
        "medium": 3,
        "large": 5
    }
    return audio_duration / estimates[model_name]

def transcribe_audio_files(directory, model_name):
    # Main transcription function
    SAMPLE_RATE = 16000  # Whisper expects this sample rate
    output_folder = create_output_folder(directory)

    # Check for GPU availability
    if torch.cuda.is_available():
        gpu_model = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory
        print(f"GPU Model: {gpu_model}")
        print(f"GPU Memory: {gpu_memory / (1024 ** 3):.2f} GB")
    else:
        print("No GPU available, using CPU.")

    # Load Whisper model
    model = whisper.load_model(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)  # Move model to GPU if available

    for filename in os.listdir(directory):
        if filename.endswith((".mp3", ".wav", ".flac", ".ogg", ".aac")):
            file_path = os.path.join(directory, filename)
            wav_path = convert_audio_to_wav(file_path)
            audio = whisper.load_audio(wav_path)
            total_duration = int(audio.shape[0] / SAMPLE_RATE)
            estimated_time = estimate_transcription_time(total_duration, model_name)
            start_time = datetime.now()
            
            print(f"Estimated Transcription Time: {timedelta(seconds=estimated_time)}")

            start_transcription_time = time.time()
            chunk_duration = 30  # Process in 30-second chunks
            transcription = []
            srt_lines = []

            for start in range(0, total_duration, chunk_duration):
                end = min(start + chunk_duration, total_duration)
                audio_chunk = audio[start * SAMPLE_RATE:end * SAMPLE_RATE]
                audio_chunk = whisper.pad_or_trim(audio_chunk)
                
                # Ensure mel spectrogram has 128 frequency bins for large model
                mel = whisper.log_mel_spectrogram(audio_chunk, n_mels=128).to(device)

                options = whisper.DecodingOptions(fp16=False, language="en", task="transcribe")
                result = whisper.decode(model, mel, options)

                current_text = result.text.strip()
                transcription.append(current_text)

                # Generate SRT entry for this chunk
                start_time_str = timedelta(seconds=start)
                end_time_str = timedelta(seconds=end)
                srt_lines.append(f"{len(srt_lines) // 3 + 1}\n")
                srt_lines.append(f"{start_time_str} --> {end_time_str}\n")
                srt_lines.append(f"{current_text}\n")

                print(f"\r>> {current_text} <<", end='', flush=True)  # Display transcription progress

            end_time = time.time()
            processing_time = end_time - start_transcription_time

            # Writing SRT file with UTF-8 encoding for international character support
            srt_filename = f"{os.path.splitext(filename)[0]}.srt"
            srt_path = os.path.join(output_folder, srt_filename)
            with open(srt_path, "w", encoding="utf-8") as f:
                f.writelines(srt_lines)
            
            # Writing TXT file for compatibility
            txt_filename = f"{os.path.splitext(filename)[0]}.txt"
            txt_path = os.path.join(output_folder, txt_filename)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"Estimated Time: {timedelta(seconds=estimated_time)}\n")
                f.write(f"Actual Time: {timedelta(seconds=processing_time)}\n\n")
                f.write("\n".join(transcription))

            shutil.move(file_path, os.path.join(output_folder, filename))
            shutil.move(wav_path, os.path.join(output_folder, os.path.basename(wav_path)))
            print(f"\nTranscription saved to {txt_path}")
            print(f"SRT Subtitles saved to {srt_path} with UTF-8 encoding")

def update_terminal_title(title):
    # Updates the terminal's title with the provided text
    print(f'\33]0;{title}\a', end='', flush=True)

def main():
    # Entry point of the script, handles command-line arguments
    if len(sys.argv) != 2:
        print(f"Usage: python3 {os.path.basename(__file__)} <option>\n"
              f"{__appname__} v{__version__} - {__AppShortDescription__}\n"
              "Where <option> is a number from 1 to 5 to select the Whisper model:\n"
              f"  1. tiny, 2. base, 3. small, 4. medium, 5. large\n\n"
              f"By {__author__}")
        sys.exit(1)

    try:
        model_name = choose_model(sys.argv[1])
        directory = "/mnt/c/Transcribe"  # Path to the directory containing audio files
        start_time = time.time()

        file_count = len([f for f in os.listdir(directory) if f.endswith((".mp3", ".wav", ".flac", ".ogg", ".aac"))])
        
        for idx, filename in enumerate(os.listdir(directory), 1):
            if filename.endswith((".mp3", ".wav", ".flac", ".ogg", ".aac")):
                transcribe_audio_files(directory, model_name)
                elapsed_time = time.time() - start_time
                title = f"Elapsed Time: {timedelta(seconds=elapsed_time)} - {idx}/{file_count} files processed"
                update_terminal_title(title)

        elapsed_time = time.time() - start_time
        final_title = f"Total Elapsed Time: {timedelta(seconds=elapsed_time)}"
        update_terminal_title(final_title)
        print(final_title)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
