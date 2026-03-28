from aiogram.fsm.state import State, StatesGroup


class EditSponsorsPageDescriptionFSM(StatesGroup):
    description = State()


class AddSponsorFSM(StatesGroup):
    photo = State()
    subtitle = State()
    title = State()
    description = State()
    status = State()


class EditSponsorFSM(StatesGroup):
    """sponsor_id и field хранятся в state.data, здесь только ввод нового value."""
    value = State()

