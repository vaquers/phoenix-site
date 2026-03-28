from fastapi import FastAPI, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
import re
import requests
import xml.etree.ElementTree as ET

from config import BOT_TOKEN, SUPER_ADMIN_ID, COMMUNITY_RSS_URL, COMMUNITY_CHANNEL_USERNAME
from db.queries.about_queries import get_about_page
from db.queries.team_queries import get_team_page_description, get_all_team_members, get_team_member
from db.queries.blog_queries import get_blog_page_description, get_all_blog_posts, get_blog_post
from db.queries.sponsor_queries import get_sponsors_page_description, get_all_sponsors, get_sponsor
from db.queries.contact_queries import get_contacts_page, add_contact_message
from db.queries.community_channel_queries import get_last_channel_posts
from db.queries.join_queries import get_join_page_description, add_join_application


app = FastAPI(title="Phoenix Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/about")
def read_about():
    """
    Эндпоинт для фронтенда: отдаёт данные для блока «про нас».
    """
    row = get_about_page()
    if row is None:
        return {
            "description": "",
            "years_in_competitions": 0,
            "team_size": 0,
        }

    description, years, team_size = row
    return {
        "description": description,
        "years_in_competitions": years,
        "team_size": team_size,
    }


@app.get("/api/team")
def read_team():
    """
    Эндпоинт для фронтенда: описание страницы «Команда» и список членов.
    """
    description = get_team_page_description()
    rows = get_all_team_members()
    members = [
        {
            "id": r[0],
            "name": r[1],
            "specialty": r[2],
            "description": r[3],
            "status": r[4],
            # фронт будет ходить по этому URL за картинкой
            "photo_url": f"/api/team/photo/{r[0]}" if r[5] else "",
        }
        for r in rows
    ]
    return {"description": description, "members": members}


@app.get("/api/team/photo/{member_id}")
def read_team_photo(member_id: int):
    """
    Отдаёт фото члена команды по Telegram file_id, как обычную картинку для браузера.
    """
    member = get_team_member(member_id)
    if not member or not member[5]:
        raise HTTPException(status_code=404, detail="Photo not found")

    file_id = member[5]

    try:
        info_resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id},
            timeout=10,
        )
        if not info_resp.ok:
            raise HTTPException(status_code=502, detail="Telegram getFile error")
        info_json = info_resp.json()
        file_path = info_json.get("result", {}).get("file_path")
        if not file_path:
            raise HTTPException(status_code=502, detail="Telegram getFile missing file_path")

        file_resp = requests.get(
            f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}",
            timeout=15,
        )
        if not file_resp.ok:
            raise HTTPException(status_code=502, detail="Telegram file download error")

        content_type = file_resp.headers.get("Content-Type", "image/jpeg")
        return Response(content=file_resp.content, media_type=content_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e


@app.get("/api/blog")
def read_blog():
    """
    Эндпоинт для фронтенда: описание страницы «Блог» и список записей.
    """
    description = get_blog_page_description()
    rows = get_all_blog_posts()
    posts = [
        {
            "id": r[0],
            "number": r[1],
            "description": r[2],
            # фронт будет ходить по этому URL за картинкой
            "photo_url": f"/api/blog/photo/{r[0]}" if r[3] else "",
        }
        for r in rows
    ]
    return {"description": description, "posts": posts}


@app.get("/api/blog/photo/{post_id}")
def read_blog_photo(post_id: int):
    """
    Отдаёт фото записи блога по Telegram file_id, как обычную картинку для браузера.
    """
    post = get_blog_post(post_id)
    if not post or not post[3]:
        raise HTTPException(status_code=404, detail="Photo not found")

    file_id = post[3]

    try:
        info_resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id},
            timeout=10,
        )
        if not info_resp.ok:
            raise HTTPException(status_code=502, detail="Telegram getFile error")
        info_json = info_resp.json()
        file_path = info_json.get("result", {}).get("file_path")
        if not file_path:
            raise HTTPException(status_code=502, detail="Telegram getFile missing file_path")

        file_resp = requests.get(
            f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}",
            timeout=15,
        )
        if not file_resp.ok:
            raise HTTPException(status_code=502, detail="Telegram file download error")

        content_type = file_resp.headers.get("Content-Type", "image/jpeg")
        return Response(content=file_resp.content, media_type=content_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e


@app.get("/api/sponsors")
def read_sponsors():
    """
    Эндпоинт для фронтенда: описание страницы «Спонсоры» и список спонсоров.
    """
    description = get_sponsors_page_description()
    rows = get_all_sponsors()
    sponsors = [
        {
            "id": r[0],
            # фронт пойдёт по этому URL за картинкой
            "photo_url": f"/api/sponsors/photo/{r[0]}" if r[1] else "",
            "subtitle": r[2],
            "title": r[3],
            "description": r[4],
            "status": r[5],
        }
        for r in rows
    ]
    return {"description": description, "sponsors": sponsors}


@app.get("/api/sponsors/photo/{sponsor_id}")
def read_sponsor_photo(sponsor_id: int):
    """
    Отдаёт фото спонсора по Telegram file_id, как обычную картинку для браузера.
    """
    sponsor = get_sponsor(sponsor_id)
    if not sponsor or not sponsor[1]:
        raise HTTPException(status_code=404, detail="Photo not found")

    file_id = sponsor[1]

    try:
        info_resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id},
            timeout=10,
        )
        if not info_resp.ok:
            raise HTTPException(status_code=502, detail="Telegram getFile error")
        info_json = info_resp.json()
        file_path = info_json.get("result", {}).get("file_path")
        if not file_path:
            raise HTTPException(status_code=502, detail="Telegram getFile missing file_path")

        file_resp = requests.get(
            f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}",
            timeout=15,
        )
        if not file_resp.ok:
            raise HTTPException(status_code=502, detail="Telegram file download error")

        content_type = file_resp.headers.get("Content-Type", "image/jpeg")
        return Response(content=file_resp.content, media_type=content_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e


@app.get("/api/contacts")
def read_contacts():
    """
    Эндпоинт для фронтенда: описание страницы контактов, почта, телефон, адрес, телеграм.
    """
    row = get_contacts_page()
    if row is None:
        return {
            "description": "",
            "email": "",
            "phone": "",
            "address": "",
            "telegram": "",
        }
    description, email, phone, address, telegram = row
    return {
        "description": description,
        "email": email,
        "phone": phone,
        "address": address,
        "telegram": telegram,
    }


@app.post("/api/contacts/message")
def submit_contact_message(
    name: str = Body(..., embed=True),
    email: str = Body(..., embed=True),
    message: str = Body(..., embed=True),
    telegram: str = Body("", embed=True),
):
    """
    Принять сообщение с сайта: сохранить в БД и отправить в Telegram супер-админу.
    """
    name = (name or "").strip()
    email = (email or "").strip()
    message = (message or "").strip()
    telegram = (telegram or "").strip()
    if not name or not email or not message:
        raise HTTPException(status_code=400, detail="name, email and message are required")

    msg_id = add_contact_message(name, email, message, telegram)
    if msg_id is None:
        raise HTTPException(status_code=500, detail="Failed to save message")

    # Отправить в Telegram супер-админу
    telegram_line = f"\n<b>Telegram:</b> {telegram}" if telegram else ""
    telegram_text = (
        f"📩 <b>Новое сообщение с сайта</b> (#{msg_id})\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Почта:</b> {email}{telegram_line}\n\n"
        f"<b>Текст:</b>\n{message}"
    )
    try:
        send_resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": SUPER_ADMIN_ID,
                "text": telegram_text,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        if not send_resp.ok:
            pass  # сообщение уже в БД
    except Exception:
        pass

    return {"ok": True, "id": msg_id}


# ---------- Страница «Стать участником» ----------


@app.get("/api/join")
def read_join_page():
    """Описание страницы «Стать участником» для фронта."""
    description = get_join_page_description()
    return {"description": description}


@app.post("/api/join")
def submit_join_application(
    full_name: str = Body(..., embed=True),
    grade: str = Body(..., embed=True),
    profile: str = Body(..., embed=True),
    email: str = Body(..., embed=True),
    telegram: str = Body("", embed=True),
    role: str = Body(..., embed=True),
    experience: str = Body(..., embed=True),
    motivation: str = Body(..., embed=True),
):
    """Принять анкету с сайта: сохранить в БД и отправить супер-админу в Telegram."""
    full_name = (full_name or "").strip()
    grade = (grade or "").strip()
    profile = (profile or "").strip()
    email = (email or "").strip()
    telegram = (telegram or "").strip()
    role = (role or "").strip()
    experience = (experience or "").strip()
    motivation = (motivation or "").strip()
    if not full_name or not email or not role or not experience or not motivation:
        raise HTTPException(
            status_code=400,
            detail="full_name, email, role, experience, motivation are required",
        )

    app_id = add_join_application(
        full_name=full_name,
        grade=grade,
        profile=profile,
        email=email,
        telegram=telegram,
        role=role,
        experience=experience,
        motivation=motivation,
    )
    if app_id is None:
        raise HTTPException(status_code=500, detail="Failed to save application")

    telegram_line = f"\n<b>Telegram:</b> {telegram}" if telegram else ""
    telegram_text = (
        f"🧾 <b>Новая анкета</b> #{app_id}\n\n"
        f"<b>ФИО:</b> {full_name}\n"
        f"<b>Параллель:</b> {grade}\n"
        f"<b>Профиль:</b> {profile}\n"
        f"<b>Email:</b> {email}{telegram_line}\n"
        f"<b>Роль:</b> {role}\n\n"
        f"<b>Опыт:</b>\n{experience or '—'}\n\n"
        f"<b>Мотивация:</b>\n{motivation or '—'}"
    )
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": SUPER_ADMIN_ID,
                "text": telegram_text,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
    except Exception:
        pass

    return {"ok": True, "id": app_id}


# Регулярка для post_id: t.me или https://t.me, с /s/ или без, channel/123
_TG_POST_ID_RE = re.compile(
    r"https?://t\.me/s?/?(?P<channel>[^/\s]+)/(?P<post_id>\d+)|t\.me/s?/?(?P<channel2>[^/\s]+)/(?P<post_id2>\d+)",
    re.I,
)
_CHANNEL = "phoenixlbsu"


def _parse_telegram_post_id(text: str, channel: str = _CHANNEL) -> int | None:
    """Из ссылки t.me/phoenixlbsu/123 или https://t.me/s/phoenixlbsu/123 извлекает post_id."""
    if not text:
        return None
    for m in _TG_POST_ID_RE.finditer(text):
        c = m.group("channel") or m.group("channel2")
        pid = m.group("post_id") or m.group("post_id2")
        if c and pid and c.lower() == channel.lower():
            return int(pid)
    return None


def _get_item_text(el: ET.Element) -> str:
    """Собирает весь текст из элемента и дочерних (для поиска ссылки в description/content)."""
    if el.text:
        out = [el.text]
    else:
        out = []
    for child in el:
        out.append(_get_item_text(child))
        if child.tail:
            out.append(child.tail)
    return "".join(out)


def _find_items_root(root: ET.Element) -> list[ET.Element]:
    """Ищет item/entry без привязки к namespace (RSS 2.0, Atom, RSSHub и т.д.)."""
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if tag in ("item", "entry"):
            out.append(el)
    return out


def _item_link_and_title(item: ET.Element) -> tuple[str, str]:
    link = ""
    title = ""
    for el in item:
        tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if tag == "link":
            link = (el.get("href") or (el.text or "").strip()) or link
        elif tag == "title":
            title = (el.text or "").strip() or title
    return link, title


@app.get("/api/community/posts")
def read_community_posts():
    """
    Последние 3 поста канала сообщества для страницы «Сообщество».
    Сначала берём из БД (если бот добавлен в канал и посты приходят в channel_post),
    иначе — из RSS (COMMUNITY_RSS_URL).
    """
    posts = []
    # 1) Посты из БД (бот в канале)
    rows = get_last_channel_posts(COMMUNITY_CHANNEL_USERNAME, limit=3)
    if rows:
        for message_id, link, title in rows:
            posts.append({"post_id": message_id, "link": link or "", "title": title or ""})
        return {"posts": posts}
    # 2) Fallback: RSS
    try:
        resp = requests.get(COMMUNITY_RSS_URL, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = _find_items_root(root)
        for item in items[:3]:
            link, title = _item_link_and_title(item)
            post_id = _parse_telegram_post_id(link)
            if post_id is None:
                full_text = _get_item_text(item)
                post_id = _parse_telegram_post_id(full_text)
            if post_id is not None:
                posts.append({"post_id": post_id, "link": link or "", "title": title})
    except Exception:
        pass
    return {"posts": posts}

