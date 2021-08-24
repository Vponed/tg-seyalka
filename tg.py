# -*- coding: cp1251 -*-
from telethon import TelegramClient, events,utils,types
from telethon.tl.types import InputPeerUser
import plyer
from audioplayer import AudioPlayer
import json
import asyncio
import json

interval = 60
api_id = 995882
api_hash = 
my_channel_id = 't.me/message_alerter'


def settings_load():
	file = open("telegram.json", "r")
	x = json.load(file)
	file.close()
	return x


json_data1 = settings_load()
client = TelegramClient('Message_Watcher', api_id, api_hash)


@client.on(events.NewMessage())
async def my_event_handler(event):
	if 'json_data' not in globals():
		json_data = json_data1
	try:
		if event.message:
			if str(event.chat.id) in json_data['chats']:
				event.message.message = event.message.message.lower()
				try:
					send_link = json_data['chats'][str(event.chat.id)]['repost_link'][0]
				except KeyError:
					return
				if json_data['chats'][str(event.chat.id)]['all']:
					if event.message.message.__len__() > json_data['chats'][str(event.chat.id)]['letters_count']:
						for i in json_data['chats'][str(event.chat.id)]['blacklist']:
							if i in event.message.message:
								#print("blacklist")
								return

						if json_data['chats'][str(event.chat.id)]['mp3_file'].__len__()>0:
							AudioPlayer(json_data['chats'][str(event.chat.id)]['mp3_file']).play(
							block=True)
						await client.forward_messages(send_link, event.message, from_peer=event.chat)
						print("sended ") #,event.message.text)
						json_data = settings_load()
						return
					pass
				if (event.message.sender.id in json_data['chats'][str(event.chat.id)]['users']) or (str(event.message.sender.username) in json_data['chats'][str(event.chat.id)]['users']):
					for i in json_data['chats'][str(event.chat.id)]['blacklist']:
						if i in event.message.message:
							return
					await client.forward_messages(send_link,
					                              event.message)  # , from_peer=client.get_input_entity(event.chat.id))
					print("sended ")
					sender = await event.get_sender()
					#print(sender.first_name + " " + sender.last_name)
					message_str = "Важное обновление телеграм \n" + str(sender.first_name) + " " + str(sender.last_name) + "\n " + event.message.message
					print(message_str)
					plyer.notification.notify(message=message_str, app_name='Telegram alerter',
					                          title='Ахтунг')
					for i in json_data['chats'][str(event.chat.id)]['whitelist']:
						if i == "": break
						if i in event.message.message:
							print(json_data['chats'][str(event.chat.id)]['whitelist'])
							if json_data['chats'][str(event.chat.id)]['white_list_mp3_file'].__len__()>0:
								AudioPlayer(json_data['chats'][str(event.chat.id)]['white_list_mp3_file']).play(
								block=True)
							return
					AudioPlayer(json_data['chats'][str(event.chat.id)]['mp3_file']).play(
						block=True)
					
			json_data = settings_load()

	except AttributeError:
		pass


client.start()
print("start")
client.run_until_disconnected()
