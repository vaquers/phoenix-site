from aiogram.fsm.state import State, StatesGroup


class EditBlogPageDescriptionFSM(StatesGroup):
    description = State()


class AddBlogPostFSM(StatesGroup):
    photo = State()
    description = State()


class EditBlogPostFSM(StatesGroup):
    """post_id и field хранятся в state.data, здесь только ввод нового value."""
    value = State()

