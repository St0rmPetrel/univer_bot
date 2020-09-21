#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

from telegram.ext import Updater, ConversationHandler
import os

from markups import (MAIN_MENU, HELP, REGISTING, TIME_TABLE, 
                     MAIN_MENU, HELP, REGISTING, TIME_TABLE,
                     DAY, FORMAT, WEEK_NUM, UPDATE, ADMIN, UPDATE_GROUP)

from help_handlers import (help_main_handler, help_timetable_handler, 
                          help_week_handler, help_update_handler, 
                          help_admin_handler)

from timetable_handlers import (timetable_main_handler, timetable_week_handler, 
                                timetable_day_handler, days_handler,
                                format_handler, week_num_handler)

from update_handlers import (update_main_handler, update_group_handler, 
                             update_week_handler, update_group_regist_handler)

from atom_handlers import (back_main_menu_handler, week_handler,
                           start_handler, cancel_handler, registing_handler,
                           admin_main_handler)

PORT = int(os.environ.get('PORT', 5000))
def main():
    TOKEN = "1125707144:AAE2J9E4td-5AggyDNdXxx-r5CnVEJUmSJc"
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[start_handler],

        states={
            REGISTING : [registing_handler],
            #>>> main menu stuff >>>
            MAIN_MENU: [help_main_handler, timetable_main_handler,
                        update_main_handler, admin_main_handler,
                        week_handler],
                HELP: [help_timetable_handler, help_week_handler,
                       help_update_handler, help_admin_handler,
                       back_main_menu_handler],
                #>>> timetable stuff >>>
                TIME_TABLE: [timetable_week_handler, # Через контекст скорее всего както можно
                             timetable_day_handler,
                             back_main_menu_handler],
                    DAY: [days_handler, 
                          back_main_menu_handler],
                    FORMAT: [format_handler,
                             back_main_menu_handler],
                    WEEK_NUM: [week_num_handler,
                               back_main_menu_handler],
                #<<< timetable stuff <<<
                UPDATE: [update_group_handler, update_week_handler,
                         back_main_menu_handler],
                    UPDATE_GROUP: [update_group_regist_handler],
                ADMIN: [back_main_menu_handler] # В будущем надеюсь доделать
            #<<< main menu stuff <<<
        },

        fallbacks=[cancel_handler]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://stormy-falls-05476.herokuapp.com/' + TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
