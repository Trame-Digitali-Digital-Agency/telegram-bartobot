from gtts import gTTS
# from pydub import AudioSegment
import subprocess

text = """ciao a tutti, questo è il primo test!"""
tts = gTTS(text=text, lang='it', slow=False)
source_path_audio = "audio/parola_del_barto.mp3"
tts.save(source_path_audio)
print("tutto fatto, file salvato!\n")
# mp3_audio = AudioSegment.from_file(source_path_audio, format="mp3")
# destination_path_audio = "audio/parola_del_barto.ogg"
# mp3_audio.export(destination_path_audio, format="ogg")
# print("tutto fatto, file convertito!\n")