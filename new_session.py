
from typing import Any
import requests
import telebot

class Session(object):
    def __init__(self, main_bot: telebot.TeleBot) -> None:
        self.main_bot = main_bot
        self.users_taking_exam = dict()

    def next_poll(self, user_id, answer=None) -> Any:
        if user_id in self.users_taking_exam.keys() and self.users_taking_exam[user_id].__len__() > 0:
            qu = self.users_taking_exam[user_id][0]
            pid = None
            if qu.get("media") is not None:
                pid = self.main_bot.send_photo(
                    chat_id=user_id,
                    photo=qu.get("media")
                ).message_id
            stop = telebot.types.InlineKeyboardMarkup(row_width=1)
            stop.add(
                telebot.types.InlineKeyboardButton(text="توقف مبكرا 🛑", callback_data="stop_quiz"),
            )
            self.main_bot.send_poll(
                chat_id=user_id,
                is_anonymous=False,
                type="quiz",
                question=qu.get("question"),
                options=qu.get("choices"),
                correct_option_id=qu.get("answer"),
                reply_markup=stop,
                reply_to_message_id=pid
            )
            del self.users_taking_exam[user_id][0]
            return True
        elif self.users_taking_exam[user_id].__len__() == 0:
            del self.users_taking_exam[user_id]
            return None
        else:
            return False

    def delete_users(self, user_id: int) -> bool:
        try:
            del self.users_taking_exam[user_id]
            return True
        except:
            return False

    def register(self, user_id: int, test_type, q_amount) -> Any:
        if user_id in self.users_taking_exam.keys():
            return False
        qzz: Any = None
        if test_type == "math":
            qzz = self.get_math_ques(q_amount)
        elif test_type == "lang":
            qzz = self.get_lang_ques(q_amount)
        elif test_type == "math_lang":
            new = int(int(q_amount) / 2)
            qzz = self.get_math_ques(new) + self.get_lang_ques(new)
        self.users_taking_exam[user_id] = qzz

    def get_lang_ques(self, amount) -> Any:
        url = "https://swift-time.com/qiaas/json.php/quizquestions/CatID/12398?rand=" + str(amount)
        headers = {
            "Host": "swift-time.com",
            "Accept": "*/*",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "EyadGabbani/28 CFNetwork/1312 Darwin/21.0.0"
        }
        q_info = []
        try:
            s: requests.Response = requests.get(url, headers=headers)
            if s.ok:
                for q in s.json():
                    data = dict()
                    data["question"] = q.get("question")
                    data["choices"] = []
                    data["choices"].append(q.get("option1"))
                    data["choices"].append(q.get("option2"))
                    data["choices"].append(q.get("option3"))
                    data["choices"].append(q.get("option4"))
                    data["answer"] = q.get("answer") - 1
                    if q.get("media_url") != "media/":
                        data["media"] = "https://swift-time.com/qiaas/" + q.get("media_url")
                    q_info.append(data)
                return q_info
        except Exception as e:
            return False

    def get_math_ques(self, amount) -> Any:
        url = "https://swift-time.com/qiaas/json.php/quizquestions/CatID/12399?rand=" + str(amount)
        headers = {
            "Host": "swift-time.com",
            "Accept": "*/*",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "EyadGabbani/28 CFNetwork/1312 Darwin/21.0.0"
        }
        q_info = []
        try:
            s: requests.Response = requests.get(url, headers=headers)
            if s.ok:
                for q in s.json():
                    data = dict()
                    data["question"] = q.get("question")
                    data["choices"] = []
                    data["choices"].append(q.get("option1"))
                    data["choices"].append(q.get("option2"))
                    data["choices"].append(q.get("option3"))
                    data["choices"].append(q.get("option4"))
                    data["answer"] = q.get("answer") - 1
                    if q.get("media_url") != "media/":
                        data["media"] = "https://swift-time.com/qiaas/" + q.get("media_url")
                    q_info.append(data)
                return q_info
        except Exception as e:
            return False