from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiomysql import Pool


from storage.db import init_receipt_row
from keyboards.keyboard import (
    blockchain_keyboard,
    data_action_keyboard,
    back_menu_keyboard
)

seed_router = Router()

@seed_router.callback_query(lambda callback: callback.data in {'track', 'my_wallets'})
async def track_back(
    pl: Pool,
    callback: CallbackQuery, 
    state: FSMContext
    ) -> None: 
    
    client_id = callback.from_user.id
    if callback.data == 'track':
        last_stage = await state.get_data()
        about_stage = last_stage.get('action')
        async with pl.acquire() as cnn:
            async with cnn.cursor() as cr:
                raw_rows = await cr.execute('SELECT rows FROM Table_1 WHERE client_id = %s', (client_id, ))
                if raw_rows != None:
                    rows = await cr.fetchall()
        if len(rows) >= 5:
            text = f'📚 You have too many addresses!'
            markup = back_menu_keyboard
        else:
            text = f'<b>Select blockchain</b>'
            markup = blockchain_keyboard
        await callback.bot.edit_message_text(
            text=text,
            chat_id=client_id,
            message_id=about_stage,
            reply_markup=markup,
            parse_mode=ParseMode.HTML
        )
    elif callback.data == 'my_wallets':
        data = await init_receipt_row(
            client=client_id
            )
        if data != None:
            rows = '\n\n'.join(
                f'{i}. {row}'
                for i, row in enumerate(
                    data,
                    start=1)
            )
            last_stage = await state.get_data()
            about_stage = last_stage.get('action')
            text = (f'<b>📋 Your addresses at moment:</b>\n\n\n'
                    f'<code>{rows}</code>')
            markup = data_action_keyboard
        else:
            text = f'🤷‍♀️ You not have addresses it yet, added them!'
            markup = back_menu_keyboard
            await state.clear()
        await callback.bot.edit_message_text(
            text=text,
            chat_id=client_id,
            message_id=about_stage,
            reply_markup=markup,
            parse_mode=ParseMode.HTML
        )
