from tbot.bot import i18n

_ = i18n.gettext

# /start
START_MESSAGE = _("""Hello!
Answer a few questions.
""")

INVALID_START_PAYLOAD_ERROR = _("""Oops..
<b>Your payload is invalid.</b> Please try register manually by typing /register
Error message:
<b>{error_message}</b>
""")

# /register
WELCOME_MESSAGE = _("""All right! Your now registed
Your account data is:
{user_data}
If you would like to update your profile info. Type /update
""")

YOU_ARE_ALREADY_REGISTERED_MESSAGE = _("""You are already registered.
Your account data is:
{user_data}
If you would like to update or full it. Type /update.
""")

ASK_AREA_MESSAGE = _("""Enter your area
""")

ASK_STREET_MESSAGE = _("""Enter your street
""")

ASK_HOUSE_NUMBER_MESSAGE = _("""Enter your house number
""")

NOT_DIGITAL_NUMBER_ERROR = _("""Opps... house number must contain only digits. Please try again
""")

# /update
CMD_UPDATE = _("""Your account data is
{user_data}
Please provide field you wanna and new value seprated by <b>comma-space</b>
Ex. <i>Phone number</i>, <b>+12345678901</b>
For save new data type /exitupdate
""")

CMD_EXITUPDATE = _("""You successfully update your profile data:
{user_data}
""")

UPDATE_ITERATION_SUCCESS = _("""'{field}' successfully updated
Please provide field you wanna and new value seprated by <b>comma-space</b>
<i>Ex. Phone number, +12345678901</i>
For save new data type /exitupdate
""")

UPDATE_ITERATION_FAILED = _("""Oops..
An error has occurred.
Error message:
<b>{error_message}</b>
Please try again
""")

NOT_VALID_FIELD_ERROR = _("""
Field '{field}' is not valid
List of valid fields:
{fields}
""")

SEPERETE_BY_COMMA_ERROR = _("""
Please, seperate value by comma-space
<i>Ex. Phone number, +12345678901</i>
""")

YOU_ARE_NOT_REGISTERED_ERROR = _("""
In order to {action}, you need to have one.
Please Register first. Type /register
""")

# /delete_account
DELETED_ACCOUNT_SUCCESSFULLY = _("""
You are successfully delete your account.
If you want to create new. Type /register
""")
