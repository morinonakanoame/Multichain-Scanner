from aiogram import (
    types,
    Router
)

from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.filters import Command

from aiogram.enums import (
    ChatAction, 
    ParseMode
)

import aiogram

router = Router() 

@router.message(Command('start', prefix='/!.'))
async def handler_greet_message(
    msg: types.Message
) -> None:
    chat_id = msg.from_user.id
    keyboard = InlineKeyboardMarkup(
        inlines=[
            [
                InlineKeyboardButton(
                    text='Track',
                    callback_data=None
                ),
                InlineKeyboardButton(
                    text='Untrack',
                    callback_data=None
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Wallets',
                    callback_data=None
                )
            ]
        ]
    )
    await msg.bot.send_chat_action(
        action=ChatAction.TYPING,
        chat_id=chat_id
    )
    text = f"test"
    return await msg.answer(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    
