from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from tgbot.buttons.reply import make_reply_button
from tgbot.dispatcher import dp
from tgbot.states import DeveloperForm, CustomerForm


@dp.message(DeveloperForm.main_panel, F.text == __('Back To Register'))
@dp.message(CustomerForm.main_panel, F.text == __('Back To Register'))
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    buttons = _('Developer'), _('Customer'),
    sizes = [2]
    markup = make_reply_button(buttons, sizes)
    await message.answer(_("Hello {}".format(message.from_user.full_name)))
    await message.answer(_("Who are You?"), reply_markup=markup)
