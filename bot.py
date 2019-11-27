#!/usr/bin/python3

### READING CONFIG
exec(open('/home/hououin/airtable_bot/config').read())
#
# INITIALISING TELEGRAM BOT
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

from telegram.ext import Updater
from telegram.ext.filters import Filters
updater = Updater(token = TOKEN, request_kwargs = REQUEST_KWARGS)

### INITIALISING AIRTABLE API

from airtable import Airtable
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt 
airtable = Airtable(base_id, table_name, api_key)

# Use this if you want to write more code
FIELDS = {'Date' : 'Date', 'Total Bot': 'Total Bot', 'Autistic': 'Autistic',
		'Work': 'Work', 'Great relaxation': 'Great relaxation', 'Educational activity': 'Educational activity',
		'^_^': '^_^'}
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
	msg += ". " + df['^_^'][0] + "."
#	if 'Comment' in df.keys():
#		msg += " " + df['Comment'][0]
	print(msg)
	return msg
def generate_detailed_msg_last_record():
        records = airtable.get_all(maxRecords=1, sort='-Date')
        df = pd.DataFrame.from_records((r['fields'] for r in records))
        return df['Date'][0] + ": Бот: " + str(df['Total Bot'][0]) + "/8, Аутирование: " + str(df['Autistic'][0]) + ", Качество: " + df['^_^'][0] + "."
def generate_graph():
	print('generation started')
	x = np.linspace(5, 10, 5)
	y = x ** 2
	plt.figure()
	print('0')
	plt.plot(x,y)
	print('1')
	buf = BytesIO()
	print(1.5)
	plt.savefig(buf, format = 'png')
	print('2')
	buf.seek(0)
	buf.name = 'img.png'
	print('3')
	return buf
### CREATING COMMAND FUNCTIONS
def preview(bot, update):
	bot.send_message(chat_id=USER_ID, text=generate_msg_last_record())
def send(bot, update):
        bot.send_message(chat_id=CHANNEL_ID, text=generate_msg_last_record())
def preview_graph(bot, update):
	bot.send_photo(chat_id=USER_ID, photo=generate_graph())	

	
from telegram.ext import CommandHandler
dispatcher = updater.dispatcher
user_filter = Filters.chat(USER_ID)
dispatcher.add_handler(CommandHandler('preview', preview, filters = user_filter))
dispatcher.add_handler(CommandHandler('send', send, filters = user_filter))
dispatcher.add_handler(CommandHandler('previewgraph', preview_graph, filters = user_filter))

updater.start_polling()
print('started')



