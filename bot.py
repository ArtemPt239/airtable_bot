#!/usr/bin/python3

### READING CONFIG
exec(open('/home/hououin/airtable_bot/config').read())
### INITIALISING TELEGRAM BOT
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

from telegram.ext import Updater
from telegram.ext.filters import Filters
updater = Updater(token = TOKEN, request_kwargs = REQUEST_KWARGS)

### INITIALISING AIRTABLE API

from airtable import Airtable
import pandas as pd
airtable = Airtable(base_id, table_name, api_key)

def generate_msg_last_record():
	records = airtable.get_all(maxRecords=1, sort='-Date')
	df = pd.DataFrame.from_records((r['fields'] for r in records))
	msg = df['Date'][0] + ": Бот: " + str(df['Total Bot'][0]) + "/8"
	if 'Work' in df.keys():
                msg += ", из них работа: " + str(df['Work'][0])
	if 'Autistic' in df.keys():
		msg += ", Аутирование: " + str(df['Autistic'][0]) 
	if 'Great relaxation' in df.keys():
		msg += ", Продуктивный отдых: " +  str(df['Great relaxation'][0]) 
	if 'Educational activity' in df.keys():
		msg += ", прочее саморазвитие: " + str(df['Educational activity'][0])
	msg += ", Норм поботали? : " + df['^_^'][0] + "."
	if 'Comment' in df.keys():
		msg += " " + df['Comment'][0]
	print(msg)
	return msg
def generate_detailed_msg_last_record():
        records = airtable.get_all(maxRecords=1, sort='-Date')
        df = pd.DataFrame.from_records((r['fields'] for r in records))
        return df['Date'][0] + ": Бот: " + str(df['Total Bot'][0]) + "/8, Аутирование: " + str(df['Autistic'][0]) + ", Качество: " + df['^_^'][0] + "."



### CREATING COMMAND FUNCTIONS
def preview(bot, update):
	bot.send_message(chat_id=USER_ID, text=generate_msg_last_record())
	
	print(update.effective_chat.id)
def send(bot, update):
        bot.send_message(chat_id=CHANNEL_ID, text=generate_msg_last_record())


	
from telegram.ext import CommandHandler
dispatcher = updater.dispatcher
user_filter = Filters.chat(USER_ID)
dispatcher.add_handler(CommandHandler('preview', preview, filters = user_filter))
dispatcher.add_handler(CommandHandler('send', send, filters = user_filter))

updater.start_polling()
print('started')



