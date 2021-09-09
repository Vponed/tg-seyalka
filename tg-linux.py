# -*- coding: UTF-8 -*-
from telethon import TelegramClient, events # клиент телеграм
import json									# для разбора json
import desktop_notify						# библиотека уведомлений
import subprocess							#
import os									#

if "init_var":		# определяем переменные
	interval = 60
	api_id = # надо получить api id и hash на сайте телеграм
	api_hash = ''
	my_channel_id = 't.me/message_alerter'
	path_to_app = os.getcwd()

def play_sound(play_command,mp3_file_):
	p = subprocess.Popen([play_command, mp3_file_], shell=False)	#, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
	#p.wait()
	return

def inlist_check(list, message): # функция проверяльщик
	message = message.lower()  # проверяем только в нижнем регистре
	x = ""
	for i in list:
		if i == "":
			print("Лист пуст")
			return False
		if i.lower() in message:
			print(i)
			return True
	return False

	def logger(title, whitelist, blacklist, message_text, datetime):  # title,whitelist,blacklist,message,datetime
		print(title)
		print("whitelist:", whitelist)
		print("black_list:", blacklist)
		try:
			print(message_text)
		except:
			pass
		print(datetime)
		return


def settings_load(): # чтение настроек из файла
	file = open("telegram2.json", "r")
	x = json.load(file)
	file.close()
	return x


json_data1 = settings_load() # читаем настройки в первый раз
client = TelegramClient('Message_Watcher', api_id, api_hash)  # поднимаем клиент


@client.on(events.NewMessage())					# контекст - новое сообщение в клиенте.
async def my_event_handler(event):				# функция-обработчик
	json_data = settings_load()					# читаем настройки

	if 'json_data' not in globals(): json_data = json_data1  # настройки перечитываются в конце, после обработки eventa. Если цикл 1-й, то их еще нет. Берем предварительную переменную
	try:  # основной блок
		if event.message:  # если пришло сообщение
			if str(event.chat.id) in json_data['chats']:  # если оно в списке отслеживаемых чатов
				if "Parse json and tg vars": # блок нужен только для упрощения читаемости. Разбирается json и event Телеграма, и распихивается по переменным
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

					if len(json_data['chats'][str(event.chat.id)]['repost_link'])>0: send_link = json_data['chats'][str(event.chat.id)]['repost_link'][0]
					else: send_link = 0 # адреса для пересылки может и не быть. В таком случае, просто будет выдано исключение уже после логгера и звукового сигнала

				if check_all or (event.message.sender.id in users) or (
					str(event.message.sender.username) in users):  # если стоит опция проверять все сообщения, или отправитель отслеживается, логика одна и та же
					len_on = message.__len__() >= letters_count
					if len_on:  # сверяем с нужным количеством символов. если меньше, то переход к следующему сообщению.
						if "Блок проверок на присутствие в белом и черном списке":
							whitelist_on = inlist_check(whitelist, message)
							blacklist_on = inlist_check(black_list, message)
						if whitelist_on: # Белый список основной
							if whitelist_only: # Если стоит опция только белый список
								if whitelist_mp3_file.__len__() > 0: # играем нужный файл
									play_sound(play_command, whitelist_mp3_file)
									pass
								logger(event.chat.title,whitelist,black_list,event.message.text,event.message.date) 	# печатаем в консоль
								await notify.show()				# кажем уведомление
								await client.forward_messages(send_link, event.message)  # пробуем переслать по ссылке. Если ее нет, сработает исключение. Но вся нужная работа уже выполнена
								return
						if not whitelist_on and whitelist_only: return # если в сообщении нет слов из белого списка, при этом стоит опция что только он и нужен - ждем следующее
						if blacklist_on: return							# если есть слова из черного списка - ждем следующее
						# белый и черный список проверили, это основное, теперь отрабатываем менее ценные ситуации.
						# ситуация, когда стоит отслеживать все сообщения, нет опции только белый список, нет слов из белого списка.
						if mp3_file.__len__() > 0:
							if not whitelist_on: # если не в белом списке
								play_sound(play_command, mp3_file) # играем обычный сигнал
							else: play_sound(play_command, whitelist_mp3_file) # если в белом списке. играем особый. за счет такой слегка сложной логики можно выдавать два разных сигнала
							pass
						logger(event.chat.title,whitelist,black_list,event.message.text,event.message.date) # выводим в консоль
						await notify.show()		# кажем уведомление
						await client.forward_messages(send_link, event.message) # пробуем переслать
						# sender = await event.get_sender()
						# message_str = str(sender.first_name) + " " + str(sender.last_name)  # + "\n " + event.message.message
						return
					pass

	except AttributeError: # это чиста для дебага
		print("AttributeError")
		#clear = "\n" * 100
		#print(clear)
		pass
	except ValueError:
		print("ValueError")
		#clear = "\n" * 100
		#print(clear)
		pass

try: # бывает, не коннектится. для дебага
	client.start()
	print("start")
	client.run_until_disconnected()
except ConnectionError:
	print("ConnectionError")
