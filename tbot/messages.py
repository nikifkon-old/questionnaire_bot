from tbot.bot import i18n
from tbot.utils import concat_lazy

_ = i18n.lazy_gettext

# /start
START_MESSAGE = _("""
Hello!
Answer a few questions below to use this bot.
""")

INVALID_START_PAYLOAD_ERROR = _("""
Oops..
<b>Your payload is invalid.</b> Please try register manually by typing /register
Error message:
<b>{error_message}</b>
""")

# /register
WELCOME_MESSAGE = _("""
All right! You register successfully.
Your account data is:
{user_data}
If you want to update or add to them, type /update
""")

YOU_ARE_ALREADY_REGISTERED_MESSAGE = _("""
You are already registered.
Your account data is:
{user_data}
If you want to update or add to them, type /update
""")

ASK_AREA_MESSAGE = _("""Enter your area""")

ASK_STREET_MESSAGE = _("""Enter your street""")

ASK_HOUSE_NUMBER_MESSAGE = _("""Enter your house number""")

NOT_DIGITAL_NUMBER_ERROR = _("""
Opps... house number must contain only digits. Please try again
""")

# /update
UPDATE_EXAMPLE = _("""Ex. <i>Phone number, +12345678901</i>""")

UPDATE_HELPER_MESSAGE = concat_lazy(_("""
Please type the field you want to update and the new value for it, separated by a <b>comma and a space</b>
"""), UPDATE_EXAMPLE, _("""
For save new data, type /exitupdate
"""))

CMD_UPDATE = concat_lazy(_("""
Your account data is
{user_data}
"""), UPDATE_HELPER_MESSAGE)


CMD_EXITUPDATE_MESSAGE = _("""
You successfully update your profile data:
{user_data}
""")


UPDATE_ITERATION_SUCCESS_MESSAGE = concat_lazy(_("""
'{field}' successfully updated
"""), UPDATE_HELPER_MESSAGE)


UPDATE_ITERATION_FAILED = _("""
Oops..
An error has occurred.
Error message:
<b>{error_message}</b>
Please try again
""")

NOT_VALID_FIELD_ERROR = _("""
Field '{field}' is does not exist.
List of valid fields:
{fields}
""")

SEPERETE_BY_COMMA_ERROR = concat_lazy(_("""
Please, seperate value by comma-space"""), UPDATE_EXAMPLE)

YOU_ARE_NOT_REGISTERED_ERROR = _("""
In order to {action}, you need to have one.
Please Register first, type /register
""")

# /delete_account
DELETED_ACCOUNT_SUCCESSFULLY = _("""
You are successfully delete your account.
If you want to create new, type /register
""")
