import pytest

import commandline_interface.main as cli_main


@pytest.mark.BUT47
def test_handle_input_int_returns_int_for_numeric_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42")

    result = cli_main.handle_input_int("prompt: ")

    assert result == 42


@pytest.mark.BUT48
def test_handle_input_int_returns_none_for_empty_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = cli_main.handle_input_int("prompt: ")

    assert result is None


@pytest.mark.BUT49
def test_handle_input_int_returns_minus_one_for_invalid_input(monkeypatch):
    printed_messages = []
    monkeypatch.setattr("builtins.input", lambda _: "abc")
    monkeypatch.setattr(cli_main, "effect_bold", lambda message: printed_messages.append(message))

    result = cli_main.handle_input_int("prompt: ")

    assert result == -1
    assert any("Invalid ID 'abc'" in message for message in printed_messages)
