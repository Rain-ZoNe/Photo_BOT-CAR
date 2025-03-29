import telebot
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
def detect_image(input_path, model):
    np.set_printoptions(suppress=True)
    model = load_model(model, compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(input_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    return index, confidence_score
from telebot.types import Message


bot = telebot.TeleBot('7812894019:AAEbzhuJG9J5PhZvKlWLKvVu7KFYRfJ2RhM')

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, 'Привет! Я ИИ бот уоторый умеет различать 3 модели машин BMW X5, BMW M4, BMW M3 2015 😊')


@bot.message_handler(content_types=['photo'])
def photo(message: Message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Вы не отправили картинку 😑')
    
    file_path = bot.get_file(message.photo[-1].file_id).file_path
    downloaded_file = bot.download_file(file_path)
    with open(f'images/{message.from_user.id}.png', 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, 'Вы отправили картину ✅')

    #return bot.send_message(message.chat.id, 'Если нужно будет сохранить ещё фото, я тут 😊')

    file_path = bot.get_file(message.photo[-1].file_id).file_path
    downloaded_file = bot.download_file(file_path)
    with open(f'images/{message.from_user.id}.png', 'wb') as new_file:
        new_file.write(downloaded_file)
    old = bot.send_message(message.chat.id, 'Картинка отправлена! Подождите немного картинка обрабатывается!')
    index, score = detect_image(f'images/{message.from_user.id}.png', 'keras_model.h5')
    bot.delete_message(old.chat.id, old.message_id)
    bot.send_message(message.chat.id, f'Ваша картинка {index} вероятностью {score * 100}%')

    if index == 0:
        bot.send_message(message.chat.id, f'На вашей картинке BMW X5 вероятностью (score 100]%')
    elif index == 1:
        bot.send_message(message.chat.id, f'На вашей картинке BMW M4 вероятностью (score 108]%')
    else:
        bot.send_message(message.chat.id, f'На вашей картинке BMW M3 2015 вероятностью (score 100]%')




bot.infinity_polling()
        
