#!/usr/bin/python3
import sys
import time
import logging

from twx.botapi import TelegramBot
from daemon import daemon

logging.basicConfig(filename='specsbot.log', level=logging.INFO)


class specsBot(daemon):
    def handleUpdate(self, update):
        logging.info("received msg " + update.message.text)

    def run(self):
        """
        Setup the bot
        """
        bot = TelegramBot('123583045:AAGMWlb3lhn-BDB4QV42T_Uyw4vpzq3nWeQ')
        bot.update_bot_info().wait()
        print(bot.username)

        currentUpdateId = 0
        while True:
            """
            Get updates sent to the bot
            """
            logging.debug("currentUpdateId: " + str(currentUpdateId))
            updates = bot.get_updates(offset=currentUpdateId).wait()
            logging.debug("received %d updates", len(updates))
            for update in updates:
                currentUpdateId = update.update_id + 1
                self.handleUpdate(update)
            time.sleep(1)


def main():
    daemon = specsBot('/tmp/daemon-specsbot.pid')
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print("Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)


if __name__ == "__main__":
    main()
