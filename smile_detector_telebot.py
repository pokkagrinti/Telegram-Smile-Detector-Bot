import cv2
import telebot
import time
import requests
import config


TOKEN = config.api_token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome to Smile detector!')
    
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Send a selfie and test it out! For better results, remove your spectacles and do it in a plain background!')


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_id = message.photo[2].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        photo = 'images\\' + file_id + '.jpg'
        with open(photo, 'wb') as f:
            f.write(file.content)
        
        checker = detect_face_and_smile(photo)
        
        if checker == 1:
            bot.reply_to(message, 'Don\'t be shy! You need to show ur face!')
        elif checker == 2:
            bot.reply_to(message, 'Very nice smile! Smile and let everyone know that today, you\'re a lot stronger than you were yesterday!')
        else:
            bot.reply_to(message, 'Try smiling brighter!')
    except Exception:
        bot.reply_to(message, 'Oh noes! The photo can\'t be read... Please try again with a selfie picture!')


def detect_face_and_smile(photo):
    """Detects a face and smile in the photo
    
    @param photo: photo to detect a face and smile in
    
    """
    image = cv2.imread(photo)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(image, 1.3, 5)

    if len(faces) > 0 :
        (fx, fy, fw, fh) = faces[0]
        face_photo = image[fy:fy+fh, fx:fx+fw]
        smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        smiles = smile_cascade.detectMultiScale(face_photo, 1.8, 10)
        if len(smiles) > 0:
            return 2
        else:
            return 3
        
    else:
        return 1
        
    

def main():
    while True:
        try:
            bot.polling(interval=2)
        except Exception:
            time.sleep(5)


if __name__ == "__main__":
    main()
