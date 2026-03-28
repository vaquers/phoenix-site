from aiogram.fsm.state import State, StatesGroup


class AddTeamMemberFSM(StatesGroup):
    name = State()
    photo = State()
    specialty = State()
    status = State()
    description = State()


class EditTeamMemberFSM(StatesGroup):
    """member_id и field хранятся в state.data, здесь только ввод нового value."""
    value = State()


class EditTeamPageDescriptionFSM(StatesGroup):
    description = State()
