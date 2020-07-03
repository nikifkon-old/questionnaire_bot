from typing import Callable, Any

from telebot import types
from tbot import get_bot
from tbot.core.utils import get_yes_or_no_keyboard

bot = get_bot()


class Questionnaire:
    """
    Class for creating questionnaires based on Models
    """
    class Meta:
        model = None
        fields = ()

    def __init__(self, chat_id: int, instance: Meta.model,
                 next_step_handler: Callable[[], Meta.model],
                 is_empty: bool = False,
                 is_model_fields_empty: bool = False):
        self.chat_id = chat_id
        self.instance = instance
        self.next_step_handler = next_step_handler
        self.callbacks = [None] * (len(self.Meta.fields) + 1)
        self._generate_callbacks()
        self.is_empty = is_empty
        self.is_model_fields_empty = is_model_fields_empty

    def _generate_callbacks(self) -> None:
        fields_len = len(self.Meta.fields)
        for i in range(fields_len):
            # 0-th callback is entry point
            self.callbacks[i] = self._generate_ask_for_i(i)
        # last callback is exit point
        self.callbacks[-1] = self._call_next_step_handler

    def _generate_ask_for_i(self, i: int) -> Callable[[], None]:
        def callback() -> None:
            field = self.Meta.fields[i]
            if hasattr(self, field) and hasattr(getattr(self, field), "run"):
                questionnaire_class = getattr(self, field)
                instance = getattr(self.instance, field)
                model_callback = self._generate_callback_for_model_field(
                    field, self.callbacks[i+1])
                questionnaire = questionnaire_class(
                    self.chat_id,
                    instance,
                    model_callback,
                    is_empty=self.is_model_fields_empty)
                getattr(questionnaire, "run")()
            else:
                AskField(chat_id=self.chat_id,
                         field=field,
                         instance=self.instance,
                         callback=self.callbacks[i+1])()
        return callback

    def _generate_callback_for_model_field(self, field: str,
                                           next_callback: Callable[[], None])\
            -> Callable[[Any], None]:
        def callback(instance:
                     getattr(self, field).Meta.model) -> None:
            self._set_value(field, instance)
            next_callback()
        return callback

    def _call_next_step_handler(self) -> None:
        self.next_step_handler(self.instance)

    def _ask_wanna_update_model(self) -> None:
        text = "Wanna update %s. It actual value is:\n%s" % (
            self.Meta.model.__name__, self.instance)
        keyboard = get_yes_or_no_keyboard()
        bot.send_message(
            self.chat_id,
            text,
            reply_markup=keyboard
        )
        bot.register_next_step_handler_by_chat_id(
            self.chat_id, self._wanna_update_model_handler)

    def _wanna_update_model_handler(self, message: types.Message) -> None:
        chat_id = message.chat.id
        if message.text == "Yes":
            self.run_update()
        elif message.text == "No":
            bot.send_message(chat_id, "Ok")
            self._call_next_step_handler()
        else:
            self._ask_wanna_update_model()

    def run(self) -> None:
        if not self.is_empty:
            self._ask_wanna_update_model()
        else:
            self.run_update()

    def run_update(self) -> None:
        self.callbacks[0]()

    def _set_value(self, field: str, value: Any) -> None:
        setattr(self.instance, field, value)


class AskField:
    """
    Class for create ask message in Questionnaire
    """

    def __init__(self, chat_id: int, field: str, instance: Any,
                 callback: Callable[[], None]):
        self.chat_id = chat_id
        self.field = field
        self.instance = instance
        self.actual_value = getattr(instance, field)
        self.callback = callback

    def __call__(self) -> None:
        if self.actual_value is None:
            self._ask_value()
        else:
            self._ask_wanna_update()

    def _ask_wanna_update(self) -> None:
        text = "Do you wanna udpate %s field. It actual value is %s?" % (
            self.field, self.actual_value)
        keyboard = get_yes_or_no_keyboard()
        bot.send_message(self.chat_id, text, reply_markup=keyboard)
        bot.register_next_step_handler_by_chat_id(
            self.chat_id, self._wanna_update_handler)

    def _wanna_update_handler(self, message: types.Message) -> None:
        if message.text == "Yes":
            self._ask_value()
        elif message.text == "No":
            bot.send_message(self.chat_id, "ok")
            self.callback()
        else:
            self._ask_wanna_update()

    def _ask_value(self) -> None:
        text = "Enter new value of %s" % self.field
        bot.send_message(self.chat_id, text)
        bot.register_next_step_handler_by_chat_id(
            self.chat_id, self._ask_value_handler)

    def _ask_value_handler(self, message: types.Message) -> None:
        setattr(self.instance, self.field, message.text)
        self.callback()
