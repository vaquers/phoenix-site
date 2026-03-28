from aiogram.fsm.state import State, StatesGroup


class EditContactsPageFSM(StatesGroup):
    """Поле для редактирования хранится в state.data (contacts_edit_field)."""
    value = State()
