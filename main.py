import cv2
import telebot as tb
# import os

token = "6198886108:AAHdFZhy4M-XbVayyZHa1Ez_FrF3JSjACHw"
bot = tb.TeleBot(token)
faces = cv2.CascadeClassifier('faces.xml')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'бот готов к работе, пришлите фото')

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, 'фото загружено /do')

@bot.message_handler(commands=['do'])
def start(message):
    img = cv2.imread('image.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = faces.detectMultiScale(gray, scaleFactor=2, minNeighbors=2)
    for (x, y, w, h) in results:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
    cv2.imwrite('image2.jpg', img)


    if len(results) != 0:
        bot.send_photo(message.chat.id, (open("image2.jpg", "rb")), caption="результат")
    else:
        bot.send_message(message.chat.id, 'лиц на картинке не найдено')

bot.polling(none_stop = True)