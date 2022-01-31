
from telebot import TeleBot, logger
from telebot.types import Message,CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, PollAnswer
from re import findall
from new_session import Session
token: str = "TOKEN"

class QuizBot(object):
    def __init__(self):
        self.bot = TeleBot(token=token, parse_mode="MarkDown")
        self.back = InlineKeyboardButton(text="رجوع ⬅", callback_data="back")
        self.session = Session(self.bot)
        self.message_hundler()
        self.callback_hundler()
        self.polls_answers_hundler()

    def main_page(self, chat_id, message_id, **kwargs):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(text="كمي 🧮", callback_data="math"),
            InlineKeyboardButton(text="لفظي 📜", callback_data="lang"),
            InlineKeyboardButton(text="لفظي و كمي ⚙", callback_data="math_lang")
        )
        self.bot.edit_message_text(
            chat_id=chat_id,
            text="*بوت كويز قدرات بسيط*⭐️‍️🎉\n\n*اختر نوع الاختبار: * ",
            message_id=message_id,
            reply_markup=markup,
            **kwargs
        )

    def message_hundler(self):
        @self.bot.message_handler(func=lambda c: True)
        def message(m: Message):
            if m.text == "/start":
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(
                    InlineKeyboardButton(text="كمي 🧮", callback_data="math"),
                    InlineKeyboardButton(text="لفظي 📜", callback_data="lang"),
                    InlineKeyboardButton(text="لفظي و كمي ⚙", callback_data="math_lang")
                )
                self.bot.reply_to(
                    m,
                    "* كويز قدرات بسيط*⭐️🎉\n\n*اختر نوع الكويز: * ",
                    reply_markup=markup
                )

    def generate_qus_numbers(self, type, count = None, rw = 1):
        nums: list = []
        if count is not None and isinstance(count, list):
            for i in count:
                nums.append(i.__str__())
        else:
            nums.append("10")
            nums.append("30")
            nums.append("50")
        markup = InlineKeyboardMarkup(row_width=rw)
        for num in nums:
            markup.add(InlineKeyboardButton(text=num, callback_data=type + "_{}%".format(num)))
        markup.add(self.back)
        return markup

    def register_user(self, chat_id, amount, test_type):
        reg = self.session.register(
            user_id=chat_id,
            test_type=test_type,
            q_amount=amount,
        )
        if reg is not False:
            self.session.next_poll(chat_id)
        else:
            self.session.delete_users(chat_id)
            self.session.register(
                user_id=chat_id,
                test_type=test_type,
                q_amount=amount,
            )
            self.session.next_poll(chat_id)

    def polls_answers_hundler(self):
        @self.bot.poll_answer_handler()
        def poll(p: PollAnswer):
            next_ = self.session.next_poll(p.user.id, answer=p.option_ids[0])
            if next_ is None:
                self.bot.send_message(
                    chat_id=p.user.id,
                    text="*تهانينا لقد انهيت الكويز ✔*"
                )
                self.session.delete_users(p.user.id)

    def callback_hundler(self):
        @self.bot.callback_query_handler(func=lambda c: True)
        def call(c: CallbackQuery):
            chat_id = c.message.chat.id
            message_id = c.message.message_id
            if c.data == "math":
                markup = self.generate_qus_numbers(type="math")
                self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="*نوع الكويز: كمي*\n"
                         "*يرجى اختيار عدد اسئلة الكويز*📍:",
                    reply_markup=markup
                )
            elif "math_" in c.data and "math_lang" not in c.data:
                amount = findall("math_(.*?)%", c.data)[0]
                self.register_user(
                    chat_id=chat_id,
                    amount=amount,
                    test_type="math"
                )
            elif c.data == "lang":
                markup = self.generate_qus_numbers(type="lang")
                self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="*نوع الكويز: لفظي*\n"
                         "*يرجى اختيار عدد اسئلة الكويز*📍:",
                    reply_markup=markup
                )
            elif "lang_" in c.data and "math_lang" not in c.data:
                amount = findall("lang_(.*?)%", c.data)[0]
                self.register_user(
                    chat_id=chat_id,
                    amount=amount,
                    test_type="lang"
                )
            elif c.data == "math_lang":
                markup = self.generate_qus_numbers(type="math_lang")
                self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="*نوع الكويز: لفظي و كمي*\n"
                         "*يرجى اختيار عدد اسئلة الكويز*📍:",
                    reply_markup=markup
                )
            elif "math_lang_" in c.data:
                amount = findall("math_lang_(.*?)%", c.data)[0]
                self.register_user(
                    chat_id=chat_id,
                    amount=amount,
                    test_type="math_lang"
                )
            elif c.data == "back":
                self.main_page(chat_id=chat_id, message_id=message_id)
            elif c.data == "stop_quiz":
                self.bot.send_message(
                    chat_id=chat_id,
                    text="*لقد أوقفت الكويز ✔*"
                )
                self.session.delete_users(chat_id)

    def run(self):
        while True:
            try:
                self.bot.polling(True)
            except Exception as e:
                logger.critical(e)


if __name__ == '__main__':
    bot: QuizBot = QuizBot()
    bot.run()