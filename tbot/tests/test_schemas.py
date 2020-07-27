import pytest

from pydantic import ValidationError

from tbot.schemas import BaseEvent, EventTarget


def test_event_must_contain_house_if_target_is_house(event_data):
    event_data["target"] = EventTarget.HOUSE
    event_data["house"] = None
    with pytest.raises(ValidationError):
        BaseEvent(**event_data)


def test_event_must_contain_area_if_target_is_area(event_data):
    event_data["target"] = EventTarget.AREA
    event_data["area"] = None
    with pytest.raises(ValidationError):
        BaseEvent(**event_data)
