#!/usr/bin/python3
import sys
import time
import logging
import traceback
import json

from twx.botapi import TelegramBot
from twx.botapi import ReplyKeyboardMarkup
from daemon import daemon
from datasheetFinder import DatasheetFinder

logging.basicConfig(level=logging.INFO)


class specsBot():

    numbers = ["\u0030\u20E3", "\u0031\u20E3", "\u0032\u20E3", "\u0033\u20E3",
               "\u0034\u20E3", "\u0035\u20E3", "\u0036\u20E3", "\u0037\u20E3",
               "\u0038\u20E3", "\u0039\u20E3", "\N{keycap ten}"]
    replykeyboard = ReplyKeyboardMarkup.create(
        [[numbers[1], numbers[2], numbers[3]],
         [numbers[4], numbers[5], numbers[6]],
         [numbers[7], numbers[8], numbers[9]]],
        one_time_keyboard=True
        )

    def handleUpdate(self, update):
        logging.debug("received msg " + update.message.text)
        msg = update.message
        if (msg):
            if (msg.text):
                if (msg.chat in self.db):
                    logging.debug("response")

                    try:
                        choice = specsBot.numbers.index(msg.text)
                        product = self.db[msg.chat]["products"][choice - 1]

                        text = ""

                        for d in product["datasheets"]:
                            text += d["description"] + "\n" + d["url"] + "\n\n"

                        self.bot.send_message(
                            msg.chat, text,
                            reply_to_message_id=msg.message_id
                        )
                        del self.db[msg.chat]
                    except (ValueError, IndexError) as e:
                        self.bot.send_message(
                            msg.chat, "invalid choice " + str(e),
                            reply_markup=specsBot.replykeyboard,
                            reply_to_message_id=msg.message_id
                        )
                else:
                    # TODO: check injection vulnerability
                    products = self.dsf.searchForProducts(msg.text)
                    text = "found %d products\n\n" % len(products)
                    for i, p in enumerate(products):
                        text += "%s %s\n\n" % (specsBot.numbers[i + 1],
                                               p["displayName"])
                    if len(products) > 0:
                        self.db[msg.chat] = {"state": "choosing product",
                                             "products": products}
                        self.bot.send_message(
                            msg.chat, text,
                            reply_markup=specsBot.replykeyboard,
                            reply_to_message_id=msg.message_id
                        )
                    else:
                        self.bot.send_message(
                            msg.chat, text,
                            reply_to_message_id=msg.message_id
                        )

    def get_updates_cont(self):
        """
        Get updates sent to the bot
        """
        currentUpdateId = 0
        while True:
            updates = self.bot.get_updates(offset=currentUpdateId).wait()
            for update in updates:
                print(update)
                if update:
                    currentUpdateId = update.update_id + 1
                    yield update
            time.sleep(0.5)

    def run(self):
        try:
            json_data = open("settings.json").read()
            self.settings = json.loads(json_data)

            """
            Setup the bot
            """
            self.bot = TelegramBot(self.settings["tg-apiKey"])
            self.dsf = DatasheetFinder(self.settings["el14-apiKey"])
            self.bot.update_bot_info().wait()
            self.db = {}
            logging.info("username is %s" % self.bot.username)

            for update in self.get_updates_cont():
                self.handleUpdate(update)

        except KeyboardInterrupt:
            logging.info("halting due to KeyboardInterrupt")


def main():
    daemon = specsBot()
    daemon.run()

if __name__ == "__main__":
    main()
