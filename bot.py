import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from app import db, Category, Food, Basket

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
	foods = [food.name for food in Food.query.all()]
	foods = '\n'.join(foods)
	context.bot.send_message(chat_id=update.effective_chat.id, text=foods)
	return add

def delete(update, context):
	food_name = context.args[0]
	Food.query.filter_by(name=food_name).delete()
	db.session.commit()
	context.bot.send_message(chat_id=update.effective_chat.id, text="Товар " + str(food_name)+" удален")
	
def add(update, context):
	food_name = context.args[0]
	food_cat_id = context.args[1]
	food_url = context.args[1]
	food_description = context.args[2]
	food_cost = context.args[3]
	new = Food(name=food_name, category_id=food_cat_id, img_url=food_url, description=food_description, cost=food_cost)
	db.session.add(new)
	db.session.commit()
	context.bot.send_message(chat_id=update.effective_chat.id, text="Товар " + str(food_name)+" добавлен")
	
start_handler = CommandHandler('start', start)
delete_handler = CommandHandler('delete', delete)
add_handler = CommandHandler('add', add)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(add_handler)
updater.start_polling()


