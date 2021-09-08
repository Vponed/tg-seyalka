# -*- coding: UTF-8 -*-
from telethon import TelegramClient, events, utils, types
# from telethon.tl.types import InputPeerUser
import json
import asyncio
import json
import desktop_notify
import subprocess
import os


interval = 60
api_id = 
api_hash = ''
my_channel_id = 't.me/message_alerter'
path_to_app = os.getcwd()

def play_sound(play_command,mp3_file):
	p = subprocess.Popen([play_command, mp3_file], shell=False)
	#, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
	p.wait()
	return


def settings_load():
	file = open("telegram2.json", "r")
	x = json.load(file)
	file.close()
	return x


json_data1 = settings_load()
client = TelegramClient('Message_Watcher', api_id, api_hash)


@client.on(events.NewMessage())
async def my_event_handler(event):
	json_data = settings_load()

	def logger():
		print(event.chat.title)
		print("whitelist:", whitelist)
		print("black_list:", black_list)
		try:
			print(event.message.text)
		except:
			pass
		print(event.message.date)
		return
	
	def inlist_check(list, message):
		x = ""
		for i in list:
			if i == "":
				print("i=0")
				return False
			if i.lower() in message:
				print(i)
				return True
		return False
	
	if 'json_data' not in globals(): json_data = json_data1  # перечитываем настройки
	try:  # основной блок
		if event.message:  # если пришло сообщение
			#print(event.message.date)
			if str(event.chat.id) in json_data['chats']:  # если оно в списке чатов
				if True:
					chat_id = event.chat.id
					message = event.message.message
					check_all = json_data['chats'][str(event.chat.id)]['all']
					letters_count = json_data['chats'][str(event.chat.id)]['letters_count']
					black_list = json_data['chats'][str(event.chat.id)]['blacklist']
					whitelist = json_data['chats'][str(event.chat.id)]['whitelist']
					whitelist_only = json_data['chats'][str(event.chat.id)]['whitelist_only']
					mp3_file = json_data['chats'][str(event.chat.id)]['mp3_file']
					whitelist_mp3_file = json_data['chats'][str(event.chat.id)]['white_list_mp3_file']
					users = json_data['chats'][str(event.chat.id)]['users']
					notify = desktop_notify.aio.Notify("Telegram: " + str(event.chat.title), str(event.message.sender.username) + " " + message)
					notify.set_id(0).set_icon('Telegram.png').set_timeout(5000)
					play_command = json_data["audio_playback_command"]


				message = message.lower()  # приводим к нижнему регистру
				try:  # если есть, получаем из настроек ссылку для репоста
					send_link = json_data['chats'][str(event.chat.id)]['repost_link'][0]
				except KeyError:
					return
				
				if check_all or (event.message.sender.id in users) or (
					str(event.message.sender.username) in users):  # проверяем ВСЕ сообщения
					len_on = message.__len__() >= letters_count
					if len_on:  # сверяем с нужным количеством символов
						# блок проверок
						if True:
							whitelist_on = inlist_check(whitelist, message)
							blacklist_on = inlist_check(black_list, message)
						if whitelist_on:
							if whitelist_only:
								print(whitelist)
								if whitelist_mp3_file.__len__() > 0:
									play_sound(play_command,whitelist_mp3_file)
									pass
								print(event)
								#await client.edit_message(event.message, event.message.message + 'хуй')
								await client.forward_messages(send_link, event.message)
								logger()  # ,event.message.text)
								sender = await event.get_sender()
								message_str = str(sender.first_name) + " " + str(sender.last_name)  # + "\n " + event.message.message
								await notify.show()
								return
						if not whitelist_on and whitelist_only: return
						if blacklist_on: return
						if mp3_file.__len__() > 0:
							play_sound(play_command, mp3_file)
							pass
						logger()
						# await event.message.forward_to(send_link)
						#await client.edit_message(event.message, event.message.message + 'хуй')
						#print(event)
						await client.forward_messages(send_link, event.message)
						# sender = await event.get_sender()
						# message_str = str(sender.first_name) + " " + str(sender.last_name)  # + "\n " + event.message.message
						await notify.show()
						return
					pass

	except AttributeError:
		print("AttributeError")
		#clear = "\n" * 100
		#print(clear)
		pass
	except ValueError:
		print("ValueError")
		#clear = "\n" * 100
		#print(clear)
		pass

try:
	client.start()
	print("start")
	client.run_until_disconnected()
except ConnectionError:
	print("ConnectionError")
