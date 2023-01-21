from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters



updater = Updater("5372382311:AAFrQlVahsOy0k4Xgmq7gFgFvLoHS53QIB8",
				use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello senpai!!!, Welcome to the YummyBot.Please write\
		/help to see the commands available.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
	/MAIN - The Main YummyAnime Page
	/TOP100 - To get the 100 the most popular anime
	/Schedule - To get the schedule of ongoing animes
	/StudyAnimeLofi- 24/7 relaxing anime Lofi Radio""")


def MAIN_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"https://yummyanime.org/")


def TOP100_url(update: Update, context: CallbackContext):
	update.message.reply_text("https://yummyanime.org/top-anime-ot-yummyanime.html")


def Schedule_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"https://yummyanime.org/rasspisanie-anime.html")
def StudyAnimeLofi_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"https://www.youtube.com/c/nostalgicmusic/featured")




def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('MAIN', MAIN_url))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('TOP100', TOP100_url))
updater.dispatcher.add_handler(CommandHandler('Schedule', Schedule_url))
updater.dispatcher.add_handler(CommandHandler('StudyAnimeLofi', StudyAnimeLofi_url))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
	Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
