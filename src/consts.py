import os
from datetime import datetime

from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

ENV = os.environ.get("ENV")
TELEGRAM_BOT_TOKEN = (
    os.environ.get("TELEGRAM_BOT_TOKEN")
    if ENV != "DEV"
    else os.environ.get("TELEGRAM_BOT_TOKEN_DEV")
)
TELEGRAM_GROUP_URL = os.environ.get("TELEGRAM_GROUP_URL")
TELEGRAM_CHANNEL_USERNAME = os.environ.get("TELEGRAM_CHANNEL_USERNAME")
TELEGRAM_ADMIN_ID = int(os.environ.get("TELEGRAM_ADMIN_ID"))
DATABASE_FILE = os.path.join(PROJECT_ROOT, "database", "pickle_data")
VIDEO_PUBLISHED = datetime.now() > datetime(2024, 10, 28, 2, 0, 0)


class CallbackData:
    YES_START_QUESTION = "yes_start_question"
    NO_START_QUESTION = "no_start_question"
    YES_CONVERT = "yes_convert"
    NO_CONVERT = "no_convert"
    JOINED = "joined"
    NOT_JOINED = "not_joined"


# fmt: off
class Messages:
    START = "🤩 سلام! خوش اومدی! می‌خوای عکست رو تبدیل به عکس لاتاری کنم؟"
    YES = "آره ✅"
    NO = "نه ❌"
    YES_CONVERT = "📷 ایول، عکست رو بفرست"
    BYE = "🫂 بعدا می‌بینمت!" + "\nاگه خواستی دوباره شروع کنی اینجا رو بزن:\n" + "/start"
    NOT_WORKING_IMAGE = (
        "😢 عکس به درستی کار نمی‌کنه و احتمالا مناسب لاتاری نیست، لطفا یک عکس دیگه بفرست"
    )
    HELP_INVITE = "❗️برای دیدن شرایط عکس لاتاری روی /help بزن❗️"
    NOT_GOOD_IMAGE = (
        "💢 نتیجه ممکنه مناسب لاتاری نباشه و بهتره چکش کنی 💢\n" + HELP_INVITE
    )
    SUCCESS = "🎊 اینم عکس لاتاری‌ ت🎊\n" + HELP_INVITE
    RECEIVING_IMAGE = "⌛ یه لحظه وایسا..."
    JOIN_GROUP = (
        "عکست آماده‌ست و فقط باید عضو این کانال تلگرامی بشی تا برات رایگان بفرستم\n"
        + f"❤️[لینک کانال]({TELEGRAM_GROUP_URL})❤️"
    )
    JOIN_GROUP_NOT_JOINED = "عضو نشدی، لطفا دوباره تلاش کن"
    JOINED = "عضو شدم ✅"
    NOT_JOINED = "بی‌خیال ❌"
    DELETED_IMAGE = "ما عکسات رو نگه نمی‌داریم. لطفا دوباره برامون بفرست ❤️"
    REFRENCE = "منبع: [سایت رسمی لاتاری آمریکا](https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/photos/digital-image-requirements.html)"
    REQUIREMENTS = (
        "1\- عکس زیر ۲۴۰ کیلوبایت باشه\n"
        + "2\- رزولوشن عکس بین 600\*600 و 1200\*1200 باشه\n"
        + "3\- عکس مربعی باشه\n"
        + "4\- عکس بدون عینک، با بک‌گراند سفید و فوکوس روی صورت شما باشه\n"
        + "5\- عکس رنگی باشه\n"
        + "6\- عکس تکی از صورت شما باشه\n"
        + "7\- فرمت عکس JPEG باشه\n\n"
        + f"{REFRENCE}"
    )
    HELP = (
        "🤖"
        + "این بات به صورت رایگان عکس تو رو به عکس مناسب لاتاری تبدیل می‌کنه\! شرایط زیر شرایط عکس لاتاری‌ه و پایینش هم لینک خود سایت رو برات گذاشتم، خوبه اگر شک داری، این موارد و سایت رو چک کنی که شانست رو نسوزونی"
        + "😬"
        + "\n\n"
        + "*شرایط عکس لاتاری*"
        + "\n"
        + f"{REQUIREMENTS}"
    )
    INVITE_TO_YOUTUBE_VIDEO = (
        "🎥😍🇺🇸 اینجا برات توضیح دادم که چه جوری فرم لاتاری رو پر کنی، هم موبایل هم کامپیوتر"
        + "\n\n"
        + "💯[لینک آموزش لاتاری](https://youtu.be/HpcM-neM0aU)💯"
    )
# fmt: on


class UserState:
    INITIAL = "initial"
    START_QUESTION = "start_question"
    CONVERT_QUESTION = "convert_question"
