import pytest

from tbot.utils import deep_setter


class C():
    pass


class B():
    c = C()


class A():
    b = B()


def test_deep_setter_ok():
    a = A()
    deep_setter(a, ["b", "c"], "haha")
    assert a.b.c == "haha"


def test_deep_setter_attribute_error():
    a = A()
    with pytest.raises(AttributeError):
        deep_setter(a, ["b", "c", "d"], "ooops")


def test_deep_setter_one():
    a = A()
    deep_setter(a, ["b"], "one")


def test_deep_setter_not_list():
    a = A()
    with pytest.raises(TypeError):
        deep_setter(a, "b", "haha")


def test_deep_setter_empty_list():
    a = A()
    with pytest.raises(ValueError):
        deep_setter(a, [], "haha")


def test_deep_setter_contian_dots():
    a = A()
    with pytest.raises(ValueError):
        deep_setter(a, ["b.c"], "haha")
