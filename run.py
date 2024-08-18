import os
import telebot

# Initialize the bot with your token
API_TOKEN = '7075190833:AAHNNUPq7X-YehyUttHnEmnGMzDje-0JyaI'
bot = telebot.TeleBot(API_TOKEN)

# Function to extract URLs
def extract_urls(file_path):
    master_mpd_urls = []
    pdf_urls = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if 'master.mpd' in line:
                master_mpd_urls.append(line.strip())
            elif '.pdf' in line:
                pdf_urls.append(line.strip())
    
    return master_mpd_urls, pdf_urls

# Function to format the URLs into sections
def format_urls(master_mpd_urls, pdf_urls):
    master_section = "### Master.mpd URLs\n" + "\n".join(master_mpd_urls) + "\n"
    pdf_section = "### PDF URLs\n" + "\n".join(pdf_urls) + "\n"
    return master_section + "\n" + pdf_section

# Command to handle the file upload and process
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save the file temporarily
        file_name = message.document.file_name
        file_path = os.path.join("/tmp", file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Extract URLs
        master_mpd_urls, pdf_urls = extract_urls(file_path)
        formatted_urls = format_urls(master_mpd_urls, pdf_urls)
        
        # Send the extracted URLs back to the user
        bot.send_message(message.chat.id, formatted_urls)
        
        # Clean up the temporary file
        os.remove(file_path)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Error processing the file: {str(e)}")

# Start the bot
bot.polling()