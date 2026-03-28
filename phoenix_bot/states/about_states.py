from aiogram.fsm.state import State, StatesGroup


class EditAboutFSM(StatesGroup):
    description = State()
    years_in_competitions = State()
    team_size = State()
