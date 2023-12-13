# - *- coding: utf- 8 - *-
import telebot, sqlite3, time, datetime, requests, configparser, random
from telebot  import types, apihelper

config = configparser.ConfigParser()
config.read("settings.ini")
token    = config["tgbot"]["token"]
get_id   = config["tgbot"]["admin_id"]
admin_id = []
if "," in get_id:
	get_id = get_id.split(",")
	for a in get_id:
		admin_id.append(int(a))
else:
	try:
		admin_id = [int(get_id)]
	except ValueError:
		admin_id =[0]
		print("*****Вы не указали админ ID*****")

bot = telebot.TeleBot(token)

admin_keyboard = telebot.types.ReplyKeyboardMarkup(True)
admin_keyboard.row("🎁 Harytlar", "ℹ️ EBS")
admin_keyboard.row("ℹ️ EBS üýgetmek 🖍")
admin_keyboard.row("📘 Haryt goşmak", "📙 Haryt aýyrmak")
admin_keyboard.row("📗 Harytlary goşmak", "📕 Harytlary aýyrmak")
admin_keyboard.row("🔏 QIWI gapjygy üýtgetmek", "🔐 QIWI gapjygy barlamak")

user_keyboard = telebot.types.ReplyKeyboardMarkup(True)
user_keyboard.row("🎁 Harytlar", "ℹ️ EBS", "📘 Haryt goşmak", "📙 Haryt aýyrmak", "📗 Harytlary goşmak", "📕 Harytlary aýyrmak")
ignor_command = ["🎁 Harytlar", "ℹ️ EBS", "ℹ️ EBS üýtgetmek 🖍", "📘 Haryt goşmak", "📙 Haryt aýyrmak", "📗 Harytlary goşmak", "📕 Harytlary aýyrmak", "🔏 QIWI gapjygy üýtgetmek", "🔐 QIWI gapjygy barlamak"]
####################################################################################################
#Проверка на существование БД, при отсутствие, создание и настройка
with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
	cur = con.cursor()
#Проверка товаров
	try:
		cur.execute("SELECT * FROM items")
		print("DB was found(1/4)")
	except sqlite3.OperationalError:
		print("DB was not found(1/4)")
		cur.execute("CREATE TABLE items(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price INT, data TEXT )")
		print("DB 1 was create...")
#Проверка FAQ
	try:
		cur.execute("SELECT * FROM faq")
	except sqlite3.OperationalError:
		print("DB was not found(2/4)")
		cur.execute("CREATE TABLE faq(infa TEXT)")
	row = cur.fetchone()
	if row == None:
		cur.execute("DROP TABLE faq")
		cur.execute("CREATE TABLE faq(infa TEXT)")
		cur.execute("INSERT INTO faq VALUES('🔘 Informasiýa. Esasy menýuda üýtgediň.')")
		print("DB 2 was create...")
	else:
		print("DB was found(2/4)")
#Проверка киви
	try:
		cur.execute("SELECT * FROM qiwi")
	except sqlite3.OperationalError:
		print("DB was not found(3/4)")
		cur.execute("CREATE TABLE qiwi(login TEXT, token TEXT)")
	row = cur.fetchone()
	if row == None:
		cur.executemany("INSERT INTO qiwi(login, token) VALUES (?, ?)", [("nomer", "token")])
		print("DB 3 was create...")
	else:
		print("DB was found(3/4)")
#Проверка пополнивших
	try:
		cur.execute("SELECT * FROM buyers")
		print("DB was found(4/4)")
	except sqlite3.OperationalError:
		print("DB was not found(4/4)")
		cur.execute("CREATE TABLE buyers(users TEXT, iditem TEXT, comment TEXT, amount TEXT, receipt TEXT, randomnum, data TEXT)")
		print("DB 4 was create...")
if con:
	con.close()
####################################################################################################


@bot.message_handler(commands=["start"])
def start_message(message):
	if message.from_user.id in admin_id:
		try:
			bot.send_message(message.chat.id, "🔹Bot işe tayyar. 🔹\nEger düwmeler çykmasa şuňa basyň /start", reply_markup = admin_keyboard)
		except requests.exceptions.ConnectionError:
			bot.send_message(message.chat.id, "🔹 Bot işe tayyar. 🔹\nEger düwmeler çykmasa şuňa basyň  /start", reply_markup = admin_keyboard)
	else:
		try:
			bot.send_message(message.chat.id, "🔹 Bot işe tayyar. 🔹\nEger düwmeler çykmasa şuňa basyň  /start", reply_markup = user_keyboard)
		except requests.exceptions.ConnectionError:
			bot.send_message(message.chat.id, "🔹 Bot işe tayyar. 🔹\nEger düwmeler çykmasa şuňa basyň  /start", reply_markup = user_keyboard)

@bot.message_handler(content_types=["text"])
def send_text(message):
	idss = []
	name = []
	if message.text == "🎁 Harytlar":
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			row = cur.fetchall()
			for i in row:
				idss.append(i[0])
				name.append(i[1])
			x = 0
			if len(idss) >= 1:
				with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
					cur = con.cursor()
					cur.execute("SELECT * FROM items")
					while True:
						x += 1
						row = cur.fetchone()
						if row == None:
							break
						if x <= 10:
							keyboard.add(types.InlineKeyboardButton(text = (str(row[1]) + " - " + str(row[3]) + " руб"), callback_data = "b_select_item_" + str(row[0]) + "|0"))
				if len(idss) > 10:
					keyboard.add(types.InlineKeyboardButton(text = "➡️Далее➡️", callback_data = "b_nextPage|10"))
				try:
					bot.send_message(message.chat.id, "🎁 Haryt saýlaň", reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.send_message(message.chat.id, "🎁 Haryt saýlaň", reply_markup = keyboard)
			else:
				try:
					bot.send_message(message.chat.id, "🎁 Bagşlaň, harytlar şu wagt ýok.", reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.send_message(message.chat.id, "🎁 Bagşlaň, harytlar şu wagt ýok.", reply_markup = keyboard)
	elif message.text == "ℹ️ EBS":
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM faq")
			row = cur.fetchall()
		try:
			bot.send_message(message.chat.id, row[0])
		except requests.exceptions.ConnectionError:
			bot.send_message(message.chat.id, row[0])
	elif message.text == "🔐 QIWI gapjygy barlamak":
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM qiwi")
			checkQiwi = cur.execute("SELECT * FROM qiwi").fetchall()[0]
		request = requests.Session()
		request.headers["authorization"] = "Bearer " + checkQiwi[1]
		parameters = {"rows": 5, "operation" : "IN"}
		selectQiwi = request.get("https://edge.qiwi.com/payment-history/v2/persons/" + checkQiwi[0] + "/payments", params = parameters)
		if selectQiwi.status_code == 200:
			try:
				bot.send_message(message.from_user.id, "✅ QIWI gapjyk doly we dogry işleýär")
			except requests.exceptions.ConnectionError:
				bot.send_message(message.from_user.id, "✅ QIWI gapjyk doly we dogry işleýär")
		else:
			try:
				bot.send_message(message.from_user.id, "❗️  QIWI gapjyk işlänok!\nHäziriň özünde çalşyň")
			except requests.exceptions.ConnectionError:
				bot.send_message(message.from_user.id, "❗️  QIWI gapjyk işlänok!\nHäziriň özünde çalşyň")
	elif message.text == "ℹ️ EBS":
		try:
			bot.send_message(message.from_user.id, "🔘 EBS üçin täze tekstiňizi ýazyň")
			bot.register_next_step_handler(message, change_faq)
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "🔘 EBS üçin täze tekstiňizi ýazyň")
			bot.register_next_step_handler(message, change_faq)
	elif message.text == "📘 Haryt goşmak":
		try:
			bot.send_message(message.from_user.id, "📘 Harydyň adyny ýazyň")
			bot.register_next_step_handler(message, add_item_name)
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📘 Harydyň adyny ýazyň")
			bot.register_next_step_handler(message, add_item_name)
	elif message.text == "📗 Harytlary goşmak":
		try:
			bot.send_message(message.from_user.id, "📗 Harytlaryň adyny ýazyň")
			bot.register_next_step_handler(message, add_items_name)
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📗 Harytlaryň adyny ýazyň")
			bot.register_next_step_handler(message, add_items_name)
	elif message.text == "📙 Haryt aýyrmak":
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			row = cur.fetchall()
			for i in row:
				idss.append(i[0])
				name.append(i[1])
			x = 0
			if len(idss) >= 1:
				with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
					cur = con.cursor()
					cur.execute("SELECT * FROM items")
					while True:
						x += 1
						row = cur.fetchone()
						if row == None:
							break
						if x <= 10:
							keyboard.add(types.InlineKeyboardButton(text = (str(row[1]) + " - " + str(row[3]) + " rub"), callback_data = "r_select_item_" + str(row[0]) + "|0"))
				if len(idss) > 10:
					keyboard.add(types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "r_nextPage|10"))
				try:
					bot.send_message(message.chat.id, "🎁 Aýyrjak harydyňyzy saýlaň : ", reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.send_message(message.chat.id, "🎁 Aýyrjak harydyňyzy saýlaň: ", reply_markup = keyboard)
			else:
				try:
					bot.send_message(message.chat.id, "🎁 Harytlar ýok.", reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.send_message(message.chat.id, "🎁 Harytlar ýok.", reply_markup = keyboard)
	elif message.text == "📕 Harytlary aýyrmak":
		keyboard = types.InlineKeyboardMarkup()
		yes_key = types.InlineKeyboardButton(text = "❌ Hawa, aýyrmak", callback_data = "r_yes_del_all_item_")
		no_key  = types.InlineKeyboardButton(text = "✅ Ýok, aýyrma", callback_data = "r_no_del_all_item_")
		keyboard.add(yes_key, no_key)
		bot.send_message(message.from_user.id, "📕 Harytlaryň aýrylmagyna razymy:", reply_markup = keyboard)
	elif message.text == "🔏 QIWI gapjygy üýtgetmek":
		try:
			bot.send_message(message.from_user.id, "🥝 QIWI gapjygyň login(nomerini) ýazyň ")
			bot.register_next_step_handler(message, change_qiwi_number)
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "🥝 QIWI gapjygyň login(nomerini) ýazyň ")
			bot.register_next_step_handler(message, change_qiwi_number)
####################################################################################################

@bot.callback_query_handler(func = lambda call:True)
def callback_inline(call):
	idss 	= []
	name 	= []
	amounts = []
	try:
		remover = call.data.split("|")
		remover = int(remover[1])
		if remover < 0:
			remover = 0
	except:
		pass
####################################################################################################
#Удаление товаров
	if call.data == "r_nextPage|" + str(remover):
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				idss.append(row[0])
				name.append(row[1])
				amounts.append(row[3])
			try:
				x = 0
				for a in range(remover, len(idss)):
					if x < 10:
						keyboard.add(types.InlineKeyboardButton(text = (str(name[a]) + " - " + str(amounts[a]) + " руб"), callback_data = "r_select_item_" + str(idss[a]) + "|" + str(remover)))
					x += 1
				if remover + 9 >= len(idss):
					keyboard.add(types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "r_previousPage|" + str(remover - 10)))
				else:
					next_keyboard = types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "r_nextPage|" + str(remover + 10))
					number_keyboard = types.InlineKeyboardButton(text = str(remover)[:1], callback_data = ".....")
					previous_keyboard = types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "r_previousPage|" + str(remover - 10))
					keyboard.add(previous_keyboard, number_keyboard, next_keyboard)
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Aýyrmak üçin haryt saýlaň: ",
									reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Aýyrmak üçin haryt saýlaň: ",
									reply_markup = keyboard)
			except IndexError:
				pass
		if con:
			con.close()
	elif call.data == "r_previousPage|" + str(remover):
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				idss.append(row[0])
				name.append(row[1])
				amounts.append(row[3])
			try:
				x = 0
				for a in range(remover, len(idss)):
					if x < 10:
						keyboard.add(types.InlineKeyboardButton(text = (str(name[a]) + " - " + str(amounts[a]) + " rub"), callback_data = "r_select_item_" + str(idss[a]) + "|" + str(remover)))
					x += 1
				if remover <= 0:
					keyboard.add(types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "r_nextPage|" + str(remover + 10)))
				else:
					next_keyboard = types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "r_nextPage|" + str(remover + 10))
					number_keyboard = types.InlineKeyboardButton(text = str(remover)[:1], callback_data = ".....")
					previous_keyboard = types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "r_previousPage|" + str(remover - 10))
					keyboard.add(previous_keyboard, number_keyboard, next_keyboard)
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Aýyrmak üçin haryt saýlaň: ",
						reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Aýyrmak üçin haryt saýlaň: ",
						reply_markup = keyboard)
			except IndexError:
				pass
		if con:
			con.close()
	elif "r_select_item_" in call.data:
		msg = call.data[14:]
		msg = msg.split("|")
		remover = msg[1]
		msg = int(msg[0])
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				if row[0] == msg:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text = "📙 Haryt aýyrmak", callback_data = "r_del_item_" + str(row[0])))
					keyboard.add(types.InlineKeyboardButton(text = "⬅️ Yza", callback_data = "r_list_back_" + remover))
					try:
						bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🏷 *Harydyň ady:* `{0}`\n💵 *Harydyň bahasy:* `{1}`\n📜 *Harydyň mazmuny:* `{2}`\n💾 *Harydyň özi:* `{3}`".format(row[1], row[3], row[2], row[4]),
							reply_markup = keyboard, parse_mode = "MARKDOWN")
					except requests.exceptions.ConnectionError:
						bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🏷 *Harydyň ady:* `{0}`\n💵 *Harydyň bahasy:* `{1}`\n📜 *Harydyň mazmuny:* `{2}`\n💾 *Harydyň özi:* `{3}`".format(row[1], row[3], row[2], row[4]),
							reply_markup = keyboard, parse_mode = "MARKDOWN")
		if con:
			con.close()
	elif "r_list_back_" in call.data:
		remover = int(call.data[12:])
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				idss.append(row[0])
				name.append(row[1])
				amounts.append(row[3])
			try:
				x = 0
				for a in range(remover, len(idss)):
					if x < 10:
						keyboard.add(types.InlineKeyboardButton(text = (str(name[a]) + " - " + str(amounts[a]) + " руб"), callback_data = "r_select_item_" + str(idss[a]) + "|" + str(remover)))
					x += 1
				if remover <= 0 and len(idss) >= 10:
					keyboard.add(types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "r_nextPage|" + str(remover + 10)))
				elif remover <= 0 and len(idss) <= 10:
					pass
				elif remover + 9 >= len(idss):
					keyboard.add(types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "r_previousPage|" + str(remover - 10)))
				elif remover >= 10 and len(idss) >= 10:
					next_keyboard = types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "r_nextPage|" + str(remover + 10))
					number_keyboard = types.InlineKeyboardButton(text = str(remover)[:1], callback_data = ".....")
					previous_keyboard = types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "r_previousPage|" + str(remover - 10))
					keyboard.add(previous_keyboard, number_keyboard, next_keyboard)
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Aýyrmak üçin haryt saýlaň: ",
									reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Aýyrmak üçin haryt saýlaň: ",
									reply_markup = keyboard)
			except IndexError:
				pass
		if con:
			con.close()
	elif "r_no_del_all_item_" in call.data:
		try:
			bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "📕 Siz harytlary aýyrmadyňyz.")
		except requests.exceptions.ConnectionError:
			bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "📕 Siz harytlary aýyrmadyňyz.")
	elif "r_yes_del_all_item_" in call.data:
		with sqlite3.connect("shopBD.sqlite") as con:
			cur = con.cursor()
			all_items = cur.execute("SELECT * FROM items").fetchall()
			x = 0
			for row in all_items:
				cur.execute("DELETE FROM items WHERE id = ?", (row[0],))
				con.commit()
				x += 1
			try:
				bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "📕 Pozuldy `{0}` товаров.".format(x), parse_mode = "MARKDOWN")
			except requests.exceptions.ConnectionError:
				bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "📕 Pozuldy `{0}` товаров.".format(x), parse_mode = "MARKDOWN")
		if con:
			con.close()
	elif "r_del_item_" in call.data:
		msg = int(call.data[11:])
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("DELETE FROM items WHERE id = ?", (msg,))
			con.commit()
		if con:
			con.close()
		try:
			bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "✅ Haryt aýryldy.")
		except requests.exceptions.ConnectionError:
			bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "✅ Haryt aýryldy.")
####################################################################################################
#Покупка товаров
	elif call.data == "b_nextPage|" + str(remover):
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				idss.append(row[0])
				name.append(row[1])
				amounts.append(row[3])
			try:
				x = 0
				for a in range(remover, len(idss)):
					if x < 10:
						keyboard.add(types.InlineKeyboardButton(text = (str(name[a]) + " - " + str(amounts[a]) + " руб"), callback_data = "b_select_item_" + str(idss[a]) + "|" + str(remover)))
					x += 1
				if remover + 9 >= len(idss):
					keyboard.add(types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "b_previousPage|" + str(remover - 10)))
				else:
					next_keyboard = types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "b_nextPage|" + str(remover + 10))
					number_keyboard = types.InlineKeyboardButton(text = str(remover)[:1], callback_data = ".....")
					previous_keyboard = types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "b_previousPage|" + str(remover - 10))
					keyboard.add(previous_keyboard, number_keyboard, next_keyboard)
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Haryt saýlaň: ",
									reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Haryt saýlaň: ",
									reply_markup = keyboard)
			except IndexError:
				pass
		if con:
			con.close()
	elif call.data == "b_previousPage|" + str(remover):
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				idss.append(row[0])
				name.append(row[1])
				amounts.append(row[3])
			try:
				x = 0
				for a in range(remover, len(idss)):
					if x < 10:
						keyboard.add(types.InlineKeyboardButton(text = (str(name[a]) + " - " + str(amounts[a]) + " руб"), callback_data = "b_select_item_" + str(idss[a]) + "|" + str(remover)))
					x += 1
				if remover <= 0:
					keyboard.add(types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "b_nextPage|" + str(remover + 10)))
				else:
					next_keyboard = types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "b_nextPage|" + str(remover + 10))
					number_keyboard = types.InlineKeyboardButton(text = str(remover)[:1], callback_data = ".....")
					previous_keyboard = types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "b_previousPage|" + str(remover - 10))
					keyboard.add(previous_keyboard, number_keyboard, next_keyboard)
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Haryt saýlaň: ",
									reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Haryt saýlaň: ",
									reply_markup = keyboard)
			except IndexError:
				pass
		if con:
			con.close()
	elif "b_select_item_" in call.data:
		msg = call.data[14:]
		msg = msg.split("|")
		remover = msg[1]
		msg = int(msg[0])
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				if row[0] == msg:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text = "💰 Harydy satyn almak", callback_data = "buy_item_" + str(row[0])))
					keyboard.add(types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "b_list_back_" + remover))
					try:
						bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🏷 *Harydyň ady:* `{0}`\n💵 *Harydyň bahasy:* `{1}`\n📜 *Harydyň mazmuny:* `{2}`".format(row[1], row[3], row[2]),
							reply_markup = keyboard, parse_mode = "MARKDOWN")
					except requests.exceptions.ConnectionError:
						bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🏷 *Harydyň ady:* `{0}`\n💵 *Harydyň bahasy:* `{1}`\n📜 *Harydyň mazmuny:* `{2}`".format(row[1], row[3], row[2]),
							reply_markup = keyboard, parse_mode = "MARKDOWN")
		if con:
			con.close()
	elif "b_list_back_" in call.data:
		remover = int(call.data[12:])
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				idss.append(row[0])
				name.append(row[1])
				amounts.append(row[3])
			try:
				x = 0
				for a in range(remover, len(idss)):
					if x < 10:
						keyboard.add(types.InlineKeyboardButton(text = (str(name[a]) + " - " + str(amounts[a]) + " руб"), callback_data = "b_select_item_" + str(idss[a]) + "|" + str(remover)))
					x += 1
				if remover <= 0 and len(idss) >= 10:
					keyboard.add(types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "b_nextPage|" + str(remover + 10)))
				elif remover <= 0 and len(idss) <= 10:
					pass
				elif remover + 9 >= len(idss):
					keyboard.add(types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "b_previousPage|" + str(remover - 10)))
				elif remover >= 10 and len(idss) >= 10:
					next_keyboard = types.InlineKeyboardButton(text = "➡️Öňe➡️", callback_data = "b_nextPage|" + str(remover + 10))
					number_keyboard = types.InlineKeyboardButton(text = str(remover)[:1], callback_data = ".....")
					previous_keyboard = types.InlineKeyboardButton(text = "⬅️Yza⬅️", callback_data = "b_previousPage|" + str(remover - 10))
					keyboard.add(previous_keyboard, number_keyboard, next_keyboard)
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Haryt saýlaň: ",
									reply_markup = keyboard)
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "🎁 Haryt saýlaň: ",
									reply_markup = keyboard)
			except IndexError:
				pass
		if con:
			con.close()
	elif "buy_item_" in call.data:
		msg = int(call.data[9:])
		IdItems = 0
		randomChar = [random.randint(1, 9)]
		randomFake = [random.randint(9999, 999999999999)]
		randomNumber = [random.randint(9999, 999999999999)]
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM qiwi")
			sendNumber = cur.execute("SELECT * FROM qiwi").fetchall()[0][0]
		if con:
			con.close()
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM items")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				if msg == row[0]:
					sendItemsAmmo = row[3]
					IdItems = row[0]
		if con:
			con.close()
		if IdItems != 0: 
			sendComment  = "{0}|{1}.{2}.{3}.{4}".format(call.from_user.id, IdItems, randomNumber[0], randomChar[0], randomFake[0])
			sendRequests = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={0}&amountInteger={1}&amountFraction=0&extra%5B%27comment%27%5D={2}&currency=643&blocked%5B0%5D=sum&blocked%5B1%5D=comment&blocked%5B2%5D=account".format(sendNumber, sendItemsAmmo, sendComment)
			sendMessage  = "📦 *Harydyň satyn alynmagy*\n🥝 Tölegini etmek üçin aşakdaky düwmä basyň.\n*🥝 Hiç zady üýtgetmek gerek däl*, diňe tölegini etmeli.\n`(Ssylkany brauzerda açmaly, qiwi programmasynda däl)`\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🔅 *Nomer:* `{0}`\n🔅 *Kommentariýa:* `{1}`\n🔅 *Bahasy(diňe san):* `{2}`\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🔄 Töleginizi edeniňizden soňra `Tölegi barla` düwmä basyň".format(sendNumber, sendComment, sendItemsAmmo)
			check_keyboard = types.InlineKeyboardMarkup()
			check_keyboard.add(types.InlineKeyboardButton(text = "🌐 Tölegi etmek", url = sendRequests))
			check_keyboard.add(types.InlineKeyboardButton(text = "🔄 Tölegi barlamak", callback_data = f"checkPay|{randomNumber[0]}|{sendItemsAmmo}"))
			try:
				if len(str(sendNumber)) < 10:
					try:
						bot.send_message(call.message.chat.id, "❌ Bagşlaň, şu wagt tölegi edip bolanok,\nwagtlaýynça işlänok.", parse_mode = "MARKDOWN")
						if len(admin_id) > 1:
							for a in range(len(admin_id)):
								try:
									bot.send_message(admin_id[a], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
								except requests.exceptions.ConnectionError:
									bot.send_message(admin_id[a], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
						else:
							try:
								bot.send_message(admin_id[0], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
							except requests.exceptions.ConnectionError:
								bot.send_message(admin_id[0], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
					except requests.exceptions.ConnectionError:
						bot.send_message(call.message.chat.id, "❌ Bagşlaň, şu wagt tölegi edip bolanok,\nwagtlaýynça işlänok.", parse_mode = "MARKDOWN")
						if len(admin_id) > 1:
							for a in range(len(admin_id)):
								try:
									bot.send_message(admin_id[a], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
								except requests.exceptions.ConnectionError:
									bot.send_message(admin_id[a], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
						else:
							try:
								bot.send_message(admin_id[0], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
							except requests.exceptions.ConnectionError:
								bot.send_message(admin_id[0], "❗️ Töleg edip bolanok, taze qiwi gapjyk goý ❗️")
				else:
					try:
						bot.send_message(call.message.chat.id, sendMessage, parse_mode = "MARKDOWN", reply_markup = check_keyboard)
					except requests.exceptions.ConnectionError:
						bot.send_message(call.message.chat.id, sendMessage, parse_mode = "MARKDOWN", reply_markup = check_keyboard)
			except ValueError:
				try:
					bot.send_message(call.message.chat.id, "❌ Bagşlaň, şu wagt tölegi edip bolanok,\nwagtlaýynça işlänok.", parse_mode = "MARKDOWN")
				except requests.exceptions.ConnectionError:
					bot.send_message(call.message.chat.id, "❌ Bagşlaň, şu wagt tölegi edip bolanok,\nwagtlaýynça işlänok.", parse_mode = "MARKDOWN")
		else:
			try:
				bot.send_message(call.message.chat.id, "❗️ Haryt tapylmady.", parse_mode = "MARKDOWN", reply_markup = admin_keyboard)
			except requests.exceptions.ConnectionError:
				bot.send_message(call.message.chat.id, "❗️ Haryt tapylmady.", parse_mode = "MARKDOWN", reply_markup = admin_keyboard)
	elif call.data.startswith("checkPay"):
		msg = call.data[9:]
		msg = msg.split("|")
		getCommentQiwi	= []
		getAmountQiwi	= []
		getReceintQiwi	= []
		getDateQiwi		= []
		getNomerQiwi	= []
		getItems		= 0
		sendBuy			= 0
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			checkQiwi = cur.execute("SELECT * FROM qiwi").fetchall()[0]
		if con:
			con.close()
		request = requests.Session()
		request.headers["authorization"] = "Bearer " + checkQiwi[1]
		parameters = {"rows": 10, "operation" : "IN"}
		selectQiwi = request.get("https://edge.qiwi.com/payment-history/v2/persons/" + checkQiwi[0] + "/payments", params = parameters)
		selectQiwi = selectQiwi.json()["data"]
		for a in range(len(selectQiwi)):
			getCommentQiwi.append(selectQiwi[a]["comment"])
			getAmountQiwi.append(selectQiwi[a]["sum"]["amount"])
			getReceintQiwi.append(selectQiwi[a]["txnId"])
			getDateQiwi.append(selectQiwi[a]["date"])
			getNomerQiwi.append(selectQiwi[a]["personId"])
		allCheck   = False
		yesOrNo    = True
		howChar    = 0
		getBalance = 0
		for b in range(len(getCommentQiwi)):
			if str(msg[0]) in str(getCommentQiwi[b]) and str(msg[1]) in str(getAmountQiwi[b]):
				howChar = b
				allCheck = True
				getPayer      = getCommentQiwi[b].split("|")
				getIdPayer    = getPayer[0]
				getDataPayer  = []
				tempDataPayer = getPayer[1].split(".")
				getDataPayer.append(tempDataPayer[0])
				getDataPayer.append(tempDataPayer[1])
				break
		if allCheck:
			splitComment = getCommentQiwi[b].split("|")
			with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
				cur = con.cursor()
				getBuyers = cur.execute("SELECT * FROM buyers").fetchall()
			if con:
				con.close()
			for c in range(len(getBuyers)):
				if str(getIdPayer) in str(getBuyers[c][0]) and str(splitComment[1]) in str(getBuyers[c][1]):
					yesOrNo = False
			if yesOrNo:
				with sqlite3.connect("shopBD.sqlite") as con:
					cur = con.cursor()
					getItems = cur.execute("SELECT * FROM items").fetchall()
				if con:
					con.close()
				for c in range(len(getItems)):
					if str(getDataPayer[0]) == str(getItems[c][0]):
						sendBuy = str(getItems[c][4])
				with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
					cur = con.cursor()
					cur.executemany("INSERT INTO buyers(users, iditem, comment, amount, receipt, randomnum, data) VALUES (?, ?, ?, ?, ?, ?, ?)", [(splitComment[0], splitComment[1], getCommentQiwi[howChar], getAmountQiwi[howChar], getReceintQiwi[howChar], getDataPayer[1], getDateQiwi[howChar])])
				if con:
					con.close()
				with sqlite3.connect("shopBD.sqlite") as con:
					cur = con.cursor()
					cur.execute("DELETE FROM items WHERE id = ?", (int(getDataPayer[0]),))
				try:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "✅ Söwdaňyz üçin sagboluň. Ýenede dolanyp geliň.\n`{0}`".format(sendBuy))
					if len(admin_id) > 1:
						for a in range(len(admin_id)):
							bot.send_message(admin_id[a], f"💰 @{call.from_user.username} ulanyjy, şu bahadan {getAmountQiwi[howChar]} руб, haryt satyn aldy")
					else:
						bot.send_message(admin_id[0], f"💰 @{call.from_user.username} ulanyjy, şu bahadan {getAmountQiwi[howChar]} руб, haryt satyn aldy")
				except requests.exceptions.ConnectionError:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "✅ Söwdaňyz üçin sagboluň. Ýenede dolanyp geliň.\n`{0}`".format(sendBuy))
					if len(admin_id) > 1:
						for a in range(len(admin_id)):
							bot.send_message(admin_id[a], f"💰 @{call.from_user.username} ulanyjy, şu bahadan {getAmountQiwi[howChar]} руб, haryt satyn aldy")
					else:
						bot.send_message(admin_id[0], f"💰 @{call.from_user.username} ulanyjy, şu bahadan {getAmountQiwi[howChar]} руб, haryt satyn aldy")
			else:
				try:
					bot.send_message(call.from_user.id, "❗️ Siziň satyn alan harydyňyz tapylmady ýa-da eýýäm berildi.")
				except requests.exceptions.ConnectionError:
					bot.send_message(call.from_user.id, "❗️ Siziň satyn alan harydyňyz tapylmady ýa-da eýýäm berildi.")
		else:
			try:
				bot.send_message(call.from_user.id, "❗️ Pul gelmedi.\nTäzeden synanyşyň.")
			except requests.exceptions.ConnectionError:
				bot.send_message(call.from_user.id, "❗️ Pul gelmedi.\nTäzeden synanyşyň.")
####################################################################################################
#Добавление одиночных товаров
def add_item_name(message):
	global itemName
	itemName = message.text
	if itemName not in ignor_command:
		try:
			bot.send_message(message.from_user.id, "📘 Harydyň mazmunyny giriziň")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📘 Harydyň mazmunyny giriziň")
		bot.register_next_step_handler(message, add_item_discription)

def add_item_discription(message):
	global itemDiscription
	itemDiscription = message.text
	if itemDiscription not in ignor_command:
		try:
			bot.send_message(message.from_user.id, "📘 Harydyň bahasyny giriziň")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📘 Harydyň bahasyny giriziň")
		bot.register_next_step_handler(message, add_item_price)

def add_item_price(message):
	global itemPrice
	itemPrice = message.text
	if itemPrice not in ignor_command:
		try:
			bot.send_message(message.from_user.id, "📘 Harydyň özüni giriziň")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📘 Harydyň özüni giriziň")
		bot.register_next_step_handler(message, add_item_data)

def add_item_data(message):
	global itemData
	itemData = message.text
	if itemData not in ignor_command:
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			cur.executemany("INSERT INTO items (name, description, price, data) VALUES (?, ?, ?, ?)", [(itemName, itemDiscription, itemPrice, itemData)])
		if con:
			con.close()
		try:
			bot.send_message(message.from_user.id, "📘 Haryt üstünlikli goşuldy")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📘 Haryt üstünlikli goşuldy")
		
####################################################################################################
#Добавление массовых товаров
def add_items_name(message):
	global itemNames
	itemNames = message.text
	if itemNames not in ignor_command:
		try:
			bot.send_message(message.from_user.id, "📗 Harytlaryň mazmunlaryny giriziň")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📗 Harytlaryň mazmunlaryny giriziň")
		bot.register_next_step_handler(message, add_items_discription)

def add_items_discription(message):
	global itemDiscriptions
	itemDiscriptions = message.text
	if itemDiscriptions not in ignor_command:
		try:
			bot.send_message(message.from_user.id, "📗 Harytlaryň bahalaryny giriziň")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📗 Harytlaryň bahalaryny giriziň")
		bot.register_next_step_handler(message, add_items_price)

def add_items_price(message):
	global itemPrices
	itemPrices = message.text
	if itemPrices not in ignor_command:
		try:
			bot.send_message(message.from_user.id, "📗 Harytlaryň özüni aşaklygyna ýazyň. Meselem:\n`login:password`\n`login:password`\n`login:password`", parse_mode = "MARKDOWN")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, "📗 Harytlaryň özüni aşaklygyna ýazyň. Meselem:\n`login:password`\n`login:password`\n`login:password`", parse_mode = "MARKDOWN")
		bot.register_next_step_handler(message, add_items_data)

def add_items_data(message):
	global itemDatas
	itemDatas = str(message.text)
	itemDatas = itemDatas.split("\n")
	counter	  = 0
	if itemDatas not in ignor_command:
		with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
			cur = con.cursor()
			for a in range(len(itemDatas)):
				cur.executemany("INSERT INTO items (name, description, price, data) VALUES (?, ?, ?, ?)", [(itemNames, itemDiscriptions, itemPrices, itemDatas[a])])
				counter += 1
		if con:
			con.close()
		try:
			bot.send_message(message.from_user.id, f"📘 {counter} harytlar üstünlikli goşuldy.")
		except requests.exceptions.ConnectionError:
			bot.send_message(message.from_user.id, f"📘 {counter} harytlar üstünlikli goşuldy.")
####################################################################################################
#Смена текста FAQ
def change_faq(message):
	with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM faq")
		while True:
			row = cur.fetchone()
			if row == None:
				break
			cur.execute("UPDATE faq SET infa = ? WHERE infa = ?", (message.text, row[0]))
	if con:
		con.close()
	try:
		bot.send_message(message.from_user.id, "🔘 EBS täzelendi")
	except requests.exceptions.ConnectionError:
		bot.send_message(message.from_user.id, "🔘 EBS täzelendi")
####################################################################################################
#Смена киви данных
def change_qiwi_number(message):
	try:
		bot.send_message(message.from_user.id, "🥝 QIWI API token giriziň")
	except requests.exceptions.ConnectionError:
		bot.send_message(message.from_user.id, "🥝 QIWI API token giriziň")
	bot.register_next_step_handler(message, change_qiwi_token)
	global qiwi_login
	qiwi_login = message.text

def change_qiwi_token(message):
	try:
		bot.send_message(message.from_user.id, "🥝 Ýazylan QIWI maglumatlary barlagy...")
	except requests.exceptions.ConnectionError:
		bot.send_message(message.from_user.id, "🥝 Ýazylan QIWI maglumatlary barlagy...")
	time.sleep(2)
	try:
		request = requests.Session()
		request.headers["authorization"] = "Bearer " + message.text  
		parameters = {"rows": 5, "operation" : "IN"}
		selectQiwi = request.get("https://edge.qiwi.com/payment-history/v2/persons/" + qiwi_login + "/payments", params = parameters)
		if selectQiwi.status_code == 200:	
			with sqlite3.connect("shopBD.sqlite", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM qiwi")
				while True:
					row = cur.fetchone()
					if row == None:
						break
					cur.execute("UPDATE qiwi SET login = ?, token = ? WHERE login = ?", (qiwi_login, message.text, row[0]))
			if con:
				con.close()
			try:
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
				bot.send_message(message.from_user.id, "✅ QIWI token üstünlikli üýtgedildi")
			except requests.exceptions.ConnectionError:
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
				bot.send_message(message.from_user.id, "✅ QIWI token üstünlikli üýtgedildi")
		else:
			try:
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
				bot.send_message(message.from_user.id, "❌ QIWI token barlagdan geçmedi. Ýalňyşlyk kod: " + str(selectQiwi.status_code))
			except requests.exceptions.ConnectionError:
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
				bot.send_message(message.from_user.id, "❌ QIWI token barlagdan geçmedi. Ýalňyşlyk kod: " + str(selectQiwi.status_code))
	except:
		try:
			bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
			bot.send_message(message.from_user.id, "❌ QIWI token barlagdan geçmedi.\nBerlen maglumatlar ýalňyş")
		except requests.exceptions.ConnectionError:		
			bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
			bot.send_message(message.from_user.id, "❌ QIWI token barlagdan geçmedi.\nBerlen maglumatlar ýalňyş")
####################################################################################################
#Запуск бота с обработкой вылетов
if __name__ == "__main__":
	while True:
		try:
			print("BOT işe başlady!")
			bot.polling(none_stop = True, interval = 0)
		except requests.exceptions.ConnectionError:
			print("Skriptyň birikme ýalňyşlygy ýüze çykdy 'ConnectionError'")
			time.sleep(10)
