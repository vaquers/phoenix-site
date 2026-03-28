import re


def escape_md(text: str) -> str:
    """Экранирует специальные символы MarkdownV2"""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))