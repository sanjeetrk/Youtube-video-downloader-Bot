import telebot 
import os 
from pytube import YouTube 
 
# Initialize your bot with the Telegram token 
bot = telebot.TeleBot("YOUR_BOT_TOKEN") 
 
# Define your YouTube video download function 
# def download_audio(url, output_dir): 
#     yt = YouTube(url) 
#     audio_stream = yt.streams.filter(only_audio=True).first() 
#     audio_file_path = audio_stream.download(output_dir) 
#     # Change file extension to .mp3 
#     os.rename(audio_file_path, audio_file_path[:-4] + ".mp3") 
#     return audio_file_path[:-4] + ".mp3" 

#below function to download audio in better quality

def download_audio(url, output_dir): 
    yt = YouTube(url) 
    # Get the highest quality audio stream 
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first() 
    audio_file_path = audio_stream.download(output_dir) 
    # Change file extension to .mp3 
    os.rename(audio_file_path, audio_file_path[:-4] + ".mp3") 
    return audio_file_path[:-4] + ".mp3" 
 
 
# Define your Telegram bot message handlers 
@bot.message_handler(commands=['start']) 
def send_welcome(message): 
    bot.reply_to(message, "Send me a YouTube video link and I'll send you back the audio.") 
 
@bot.message_handler(func=lambda message: True) 
def handle_message(message): 
    if message.text.startswith("https"): 
        try: 
            video_url = message.text 
            output_directory = "output/" 
            audio_file_path = download_audio(video_url, output_directory) 
 
            # Send the audio file to the user 
            with open(audio_file_path, 'rb') as audio_file: 
                bot.send_audio(message.chat.id, audio_file) 
 
            # Delete the downloaded audio and video files 
            os.remove(audio_file_path) 
            video_id = YouTube(video_url).video_id 
            # os.remove(os.path.join(output_directory, f"{video_id}.mp4")) 
        except Exception as e: 
            bot.reply_to(message, f"Error occurred: {str(e)}") 
    else: 
        bot.reply_to(message, "Please enter a YouTube link.") 
 
# Run the bot 
bot.polling()
