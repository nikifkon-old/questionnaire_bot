# /start
WELCOME_MESSAGE = """All right! Your now registed
Your account data is:
{user_data}
"""

YOU_ARE_ALREADY_REGISTERED_MESSAGE = """You are already registered.
Your account data is:
{user_data}
If you would like to update or full it. Type /update.
"""


# /update
CMD_UPDATE = """Your account data is
{user_data}
Please provide field you wanna and new value seprated by <b>comma-space</b>
Ex. <i>Phone number</i>, <b>+12345678901</b>
For save new data type /exitupdate
"""

CMD_EXITUPDATE = """You successfully update your profile data:
{user_data}
"""

UPDATE_ITERATION_SUCCESS = """'{field}' successfully updated
Please provide field you wanna and new value seprated by <b>comma-space</b>
<i>Ex. Phone number, +12345678901</i>
For save new data type /exitupdate
"""

UPDATE_ITERATION_FAILED = """Oops..
An error has occurred.
Error message:
<b>{error_message}</b>
Please try again
"""

NOT_VALID_FIELD_ERROR = """
Field '{field}' is not valid
List of valid fields:
{fields}
"""

SEPERETE_BY_COMMA_ERROR = """
Please, seperate value by comma-space
<i>Ex. Phone number, +12345678901</i>
"""