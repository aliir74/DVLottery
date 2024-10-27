import os

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


class CallbackData:
    YES_START_QUESTION = "yes_start_question"
    NO_START_QUESTION = "no_start_question"
    YES_CONVERT = "yes_convert"
    NO_CONVERT = "no_convert"
    JOINED = "joined"
    NOT_JOINED = "not_joined"


class Messages:
    START = "🤩 سلام! خوش اومدی! می‌خوای عکست رو تبدیل به عکس لاتاری کنم؟"
    YES = "آره ✅"
    NO = "نه ❌"
    YES_CONVERT = "📷 ایول، عکست رو بفرست"
    BYE = "🫂 بعدا می‌بینمت!" + "\nاگه خواستی دوباره شروع کنی اینجا رو بزن:\n" + "/start"
    NOT_WORKING_IMAGE = (
        "😢 عکس به درستی کار نمی‌کنه و احتمالا مناسب لاتاری نیست، لطفا یک عکس دیگه بفرست"
    )
    NOT_GOOD_IMAGE = (
        "💢 نتیجه ممکنه مناسب لاتاری نباشه و بهتره چکش کنی\n"
        + "برای دیدن شرایط عکس لاتاری روی /help بزن!"
    )
    SUCCESS = (
        "🎊 اینم عکس لاتاری‌ت\n"
        + "برای دیدن شرایط عکس لاتاری روی /help بزن که مطمئن باشی عکست درسته!"
    )
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


class UserState:
    INITIAL = "initial"
    START_QUESTION = "start_question"
    CONVERT_QUESTION = "convert_question"
