from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TelegramBot.assets.start_constants import *
from pyrogram import Client, filters
from TelegramBot.config import *

START_BUTTON = [
    [
        InlineKeyboardButton("Wallets", callback_data="WALLETS"),
        InlineKeyboardButton("Trades", callback_data="ABOUT_BUTTON"),
        InlineKeyboardButton("Quick Buy", callback_data="COMMAND_BUTTON")
    ],
]


    WALLETS = [
    [
        InlineKeyboardButton("Add wallet", callback_data="ADD_WALLET"),
        InlineKeyboardButton("Withdrawl", callback_data="WITHDRAWAL"),
        InlineKeyboardButton("Balance", callback_data="BALANCE"),
        InlineKeyboardButton("Disconnect Wallet", callback_data="DISCONNECT_WALLET"),
    ],  
    [InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")],
]

    TRADES = [
      [  
        InlineKeyboardButton("New Trades", callback_data="NEW_TRADES"),
        InlineKeyboardButton("Open trades", callback_data="Open_"),
      ],
        [InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")],
    ]  

GOBACK_1_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")]]

GOBACK_2_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="COMMAND_BUTTON")]]


commands = ["start", "help"]
@Client.on_message(filters.command(commands, **prefixes))
async def start(client, message):
    await message.reply_animation(
        animation=START_ANIMATION,
        caption=START_CAPTION,
        reply_markup=InlineKeyboardMarkup(START_BUTTON),
        quote=True)


@Client.on_callback_query(filters.regex("_BUTTON"))
async def botCallbacks(client, CallbackQuery):

    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id
   
    if clicker_user_id != user_id:
    return await CallbackQuery.answer ("This command is not initiated by you.")
   
    if CallbackQuery.data == "ABOUT_BUTTON":
        await CallbackQuery.edit_message_text(ABOUT_CAPTION, reply_markup=InlineKeyboardMarkup(GOBACK_1_BUTTON))

    elif CallbackQuery.data == "START_BUTTON":
        await CallbackQuery.edit_message_text(START_CAPTION, reply_markup=InlineKeyboardMarkup(START_BUTTON))

    elif CallbackQuery.data == "dumb":
        await CallbackQuery.edit_message_text(START_CAPTION, reply_markup=InlineKeyboardMarkup(START_BUTTON))

    elif CallbackQuery.data == "WALLETS":
        await CallbackQuery.edit_message_text(COMMAND_CAPTION, reply_markup=InlineKeyboardMarkup(WALLETS))

    elif CallbackQuery.data == "USER_BUTTON":
        await CallbackQuery.edit_message_text(USER_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON))

