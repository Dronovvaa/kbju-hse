from distutils import command
from pathlib import Path
import telebot
from telebot import types

WELCOME_MESSAGE = "Привет!\nЯ бот который поможет вам следить за собой.\nДайте ответы на несколько моих вопросов и я назову вашу суточноу норму КБЖУ.\nЧтобы начать нажмите на кнопку Старт"
ASK_GENDER_MESSAGE = "Укажите свой пол"
ASK_AGE_MESSAGE = "Сколько вам лет?"
ASK_WEIGHT_MESSAGE = "Укажите желаемый вес(кг)"
ASK_HEIGHT_MESSAGE = "Укажите свой рост(см)"
ASK_ACTIVITY_MESSAGE = "Как часто вы занимаетесь?"

MALE = 0
FEMALE = 1

LITTLE_ACTIVITY = 0
NORMAL_ACTIVITY = 1
REGULAR_ACTIVITY = 2


token = Path('config.txt').read_text().split("\n")[0]
bot = telebot.TeleBot(token)
users = {}


class User:
    '''
    User object
    '''
    gender = FEMALE
    age = 0
    weight = 0
    height = 0
    activity = 0
    question = 0

    def count_kbju(self):
        """
        Calculates KBJU

        :return: Ready text for the user with all the data
        """
        if self.gender == FEMALE:
            k = 6.25*self.height + 10*self.weight - 4.92*self.age - 161
        else:
            k = 6.25*self.height + 10*self.weight - 4.92*self.age + 5
        # print(k)
        if self.activity == LITTLE_ACTIVITY:
            k *= 1.2
        elif self.activity == NORMAL_ACTIVITY:
            k *= 1.375
        else:
            k *= 1.6375
        k = int(k)
        b = int(0.3 * k)
        zh = int(0.3 * k)
        u = int(0.4 * k)
        return "Ваша суточная норма калорий {}\nИз них:\n{}кал белки\n{}кал жиры\n{}кал углеводы\nВведите /start если хотите пересчитать значения".format(k, b, zh, u)


def ask_gender(m):
    """
    Asks the gender of the user

    :param m: telebot Message object
    """
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Мужской")
    item2 = types.KeyboardButton("Женский")
    markup.add(item1)
    markup.add(item2)
    return bot.send_message(m.chat.id, ASK_GENDER_MESSAGE, reply_markup=markup)


def read_gender(m):
    """
    Reads the user's gender and checks it for correctness

    :param m: telebot Message object
    :return: is the read data correct(True/False)
    """
    ID = m.from_user.id
    if m.text.strip() == "Мужской":
        users[ID].gender = MALE
        return True
    elif m.text.strip() == "Женский":
        users[ID].gender = FEMALE
        return True
    else:
        return False


def ask_age(m):
    """
    Asks the age of the user

    :param m: telebot Message object
    """
    bot.send_message(m.chat.id, ASK_AGE_MESSAGE)


def read_age(m):
    """
    Reads the user's age and checks it for correctness

    :param m: telebot Message object
    :return: is the read data correct(True/False)
    """
    ID = m.from_user.id
    age = m.text.strip()
    if not age.isnumeric() or int(age) <= 0 or int(age) > 130:
        return False
    else:
        users[ID].age = int(age)
        return True


def ask_weight(m):
    """
    Asks the user's weight

    :param m: telebot Message object
    """
    bot.send_message(m.chat.id, ASK_WEIGHT_MESSAGE)


def read_weight(m):
    """
    Reads the user's weight and checks it for correctness

    :param m: telebot Message object
    :return: is the read data correct(True/False)
    """
    ID = m.from_user.id
    weight = m.text.strip()
    if not weight.isnumeric() or int(weight) <= 0 or int(weight) > 300:
        return False
    else:
        users[ID].weight = int(weight)
        return True


def ask_height(m):
    """
    Asks the user's height

    :param m: telebot Message object
    :return: telebot Message object
    """
    bot.send_message(m.chat.id, ASK_HEIGHT_MESSAGE)


def read_height(m):
    """
    Reads the user's height and checks it for correctness

    :param m: telebot Message object
    :return: is the read data correct(True/False)
    """
    ID = m.from_user.id
    height = m.text.strip()
    if not height.isnumeric() or int(height) <= 0 or int(height) > 250:
        return False
    else:
        users[ID].weight = int(height)
        return True


def ask_activity(m):
    """
    Asks how often the user plays sports

    :param m: telebot Message object
    """
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Минимум/отсутствие физ. нагрузки")
    item2 = types.KeyboardButton("Легкая нагрузка 1-3 раза в неделю")
    item3 = types.KeyboardButton("Тренировки ежедневно")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(m.chat.id, ASK_ACTIVITY_MESSAGE, reply_markup=markup)


def read_activity(m):
    """
    Reads the user's activity and checks it for correctness

    :param m: telebot Message object
    :return: is the read data correct(True/False)
    """
    ID = m.from_user.id
    if m.text.strip() == "Минимум/отсутствие физ. нагрузки":
        users[ID].activity = LITTLE_ACTIVITY
        return True
    elif m.text.strip() == "Легкая нагрузка 1-3 раза в неделю":
        users[ID].activity = NORMAL_ACTIVITY
        return True
    elif m.text.strip() == "Тренировки ежедневно":
        users[ID].activity = REGULAR_ACTIVITY
        return True
    else:
        return False


@bot.message_handler(commands=["start"])
def start(m):
    """
    A command that starts a dialogue with the user

    :param m: telebot Message object
    """
    user = User()
    users[m.from_user.id] = user

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Старт")
    markup.add(item1)
    bot.send_message(m.chat.id, WELCOME_MESSAGE, reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(m):
    """
    Handler that conducts a dialogue with the user

    :param m: telebot Message object
    """
    ID = m.from_user.id
    if users[ID].question == 0:
        ask_gender(m)
        users[ID].question += 1
    elif users[ID].question == 1:
        if read_gender(m):
            ask_age(m)
            users[ID].question += 1
        else:
            ask_gender(m)
    elif users[ID].question == 2:
        if read_age(m):
            ask_weight(m)
            users[ID].question += 1
        else:
            ask_age(m)
    elif users[ID].question == 3:
        if read_weight(m):
            ask_height(m)
            users[ID].question += 1
        else:
            ask_weight(m)
    elif users[ID].question == 4:
        if read_height(m):
            ask_activity(m)
            users[ID].question += 1
        else:
            ask_height(m)
    elif users[ID].question == 5:
        if read_activity(m):
            users[ID].question += 1
            bot.send_message(m.chat.id, users[ID].count_kbju())
        else:
            ask_activity(m)
    else:
        bot.send_message(m.chat.id, "Введите /start чтобы пройти опрос снова")

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
