import re

from pyrogram import filters
from pyrogram.types import Message

from ShizuMusic import bot

# اسم النداء - غيره لو عايز
WAKE_NAMES = ["يا عقرب", "عقرب"]

# الأمر العربي -> الأمر الإنجليزي
AR = {
    "شغل": "play",
    "فيديو": "vplay",
    "تخطي": "skip",
    "سكيب": "skip",
    "ايقاف": "stop",
    "إيقاف": "stop",
    "وقف": "stop",
    "انهاء": "end",
    "مسح": "clear",
    "ايقاف_مؤقت": "pause",
    "مؤقت": "pause",
    "استئناف": "resume",
    "كمل": "resume",
    "تقديم": "seek",
    "رجوع": "seekback",
    "لغة": "language",
    "اللغة": "language",
    "بنج": "ping",
    "مساعدة": "help",
    "ابدأ": "start",
    "تشغيل_تلقائي": "autoplay",
}


def _norm(word: str) -> str:
    return word.replace("أ", "ا").replace("إ", "ا").replace("ة", "ه")


_AR = {_norm(k): v for k, v in AR.items()}


@bot.on_message(filters.group & filters.text, group=-2)
async def arabic_alias(_, message: Message) -> None:
    text = (message.text or "").strip()
    if not text:
        return

    # 1) /شغل اسم الاغنية  أو  /شغل@البوت
    if text.startswith("/"):
        first, _, rest = text[1:].partition(" ")
        first = first.split("@")[0]
        eng = _AR.get(_norm(first))
        if eng:
            message.text = f"/{eng} {rest}".strip()
        return

    # 2) يا عقرب شغل اسم الاغنية
    for name in WAKE_NAMES:
        if text.startswith(name):
            body = text[len(name):].strip()
            if not body:
                return
            first, _, rest = body.partition(" ")
            eng = _AR.get(_norm(first))
            if eng:
                message.text = f"/{eng} {rest}".strip()
            return
