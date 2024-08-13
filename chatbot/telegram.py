import telepot
from telepot.loop import MessageLoop # 봇 구동
from telepot.namedtuple import InlineKeyboardMarkup as MU # 마크업
from telepot.namedtuple import InlineKeyboardButton as BT

token = '5025918465:AAEik4LzCoJlvVO4UaKfEIy6L5mdP_7CQSA'
mc = '5059790606'
bot = telepot.Bot(token)
bot.sendMessage(mc, 'hi')

btn1 = BT(text = "1. Hello", callback_data = "1")
btn2 = BT(text = "2. Bye", callback_data = "2")
mu = MU(inline_keyboard = [[btn1, btn2]]) # 가로로 배열
mu = MU(inline_keyboard = [[btn1], [btn2]]) # 세로로 배열
bot.sendMessage(mc, "선택하세요", reply_markup = mu)

def btn_show(msg):
    btn1 = BT(text = "1. Hello", callback_data = "1")
    btn2 = BT(text = "2. Bye", callback_data = "2")
    mu = MU(inline_keyboard = [[btn1, btn2]])
    bot.sendMessage(mc, "선택하세요", reply_markup = mu)