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
        "☹ عکس به درستی کار نمی‌کنه و احتمالا مناسب لاتاری نیست، لطفا یک عکس دیگه بفرست"
    )
    NOT_GOOD_IMAGE = "⚠ نتیجه ممکنه مناسب لاتاری نباشه و بهتره چکش کنی"
    SUCCESS = "🎊 اینم عکس لاتاری‌ت"
    RECEIVING_IMAGE = "⌛ یه لحظه وایسا..."
    JOIN_GROUP = (
        "عکست آماده‌ست و فقط باید عضو این کانال تلگرامی بشی تا برات رایگان بفرستم\n"
        + f"❤️[لینک کانال]({TELEGRAM_GROUP_URL})❤️"
    )
    JOIN_GROUP_NOT_JOINED = "عضو نشدی، لطفا دوباره تلاش کن"
    JOINED = "عضو شدم ✅"
    NOT_JOINED = "بی‌خیال ❌"
    DELETED_IMAGE = "ما عکسات رو نگه نمی‌داریم. لطفا دوباره برامون بفرست ❤️"


class UserState:
    INITIAL = "initial"
    START_QUESTION = "start_question"
    CONVERT_QUESTION = "convert_question"
