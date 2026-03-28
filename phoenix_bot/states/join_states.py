from aiogram.fsm.state import State, StatesGroup


class EditJoinPageDescriptionFSM(StatesGroup):
    description = State()
