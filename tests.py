from telethon import TelegramClient, sync, events
import time
import unittest
from main import *

conf = Path('config.txt').read_text().split("\n")
API_ID = conf[1]
API_HASH = conf[2]
client = TelegramClient('session', API_ID, API_HASH)
client.start()


class BotTests(unittest.TestCase):
    def send_message(self, msg, length, res):
        client.send_message('@test_bzhu_bot', msg)
        time.sleep(0.5)
        messages = client.get_messages('@test_bzhu_bot')
        for message in client.get_messages('@test_bzhu_bot', limit=1):
            m = message.message
        self.assertEqual(len(messages), length)
        self.assertEqual(m, res)

    def test_start(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)

    def test_full_correct(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)
        self.send_message('Старт', 1, ASK_GENDER_MESSAGE)
        self.send_message('Женский', 1, ASK_AGE_MESSAGE)
        self.send_message('18', 1, ASK_WEIGHT_MESSAGE)
        self.send_message('55', 1, ASK_HEIGHT_MESSAGE)
        self.send_message('160', 1, ASK_ACTIVITY_MESSAGE)
        self.send_message('Минимум/отсутствие физ. нагрузки', 1,
                          "Ваша суточная норма калорий 1620\nИз них:\n486кал белки\n486кал жиры\n648кал углеводы\nВведите /start если хотите пересчитать значения")

    def test_incorrect_gender(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)
        self.send_message('Старт', 1, ASK_GENDER_MESSAGE)
        self.send_message('Трактор', 1, ASK_GENDER_MESSAGE)

    def test_incorrect_age(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)
        self.send_message('Старт', 1, ASK_GENDER_MESSAGE)
        self.send_message('Женский', 1, ASK_AGE_MESSAGE)
        self.send_message('2000', 1, ASK_AGE_MESSAGE)

    def test_incorrect_weight(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)
        self.send_message('Старт', 1, ASK_GENDER_MESSAGE)
        self.send_message('Женский', 1, ASK_AGE_MESSAGE)
        self.send_message('18', 1, ASK_WEIGHT_MESSAGE)
        self.send_message('fffff', 1, ASK_WEIGHT_MESSAGE)

    def test_incorrect_height(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)
        self.send_message('Старт', 1, ASK_GENDER_MESSAGE)
        self.send_message('Женский', 1, ASK_AGE_MESSAGE)
        self.send_message('18', 1, ASK_WEIGHT_MESSAGE)
        self.send_message('55', 1, ASK_HEIGHT_MESSAGE)
        self.send_message('-1', 1, ASK_HEIGHT_MESSAGE)

    def test_incorrect_activity(self):
        self.send_message('/start', 1, WELCOME_MESSAGE)
        self.send_message('Старт', 1, ASK_GENDER_MESSAGE)
        self.send_message('Женский', 1, ASK_AGE_MESSAGE)
        self.send_message('18', 1, ASK_WEIGHT_MESSAGE)
        self.send_message('55', 1, ASK_HEIGHT_MESSAGE)
        self.send_message('160', 1, ASK_ACTIVITY_MESSAGE)
        self.send_message('Да', 1, ASK_ACTIVITY_MESSAGE)


if __name__ == "__main__":
    unittest.main()
