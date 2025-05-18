import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


class TestLogDecorators:
    def test_valid_log_decorator(self, capsys: CaptureFixture[str]) -> None:
        @log()
        def greeting() -> None:
            print("Hello world!")

        greeting()
        captured = capsys.readouterr()
        assert "Hello world!" in captured.out

    def test_except_log_decorator(self) -> None:
        @log()
        def division(x: int, y: int) -> int | float:
            return x / y

        with pytest.raises(Exception):
            assert division(7, 0)

    def test_log_decorator_returns_result(self) -> None:
        @log()
        def multiply(x: int, y: int) -> int:
            return x * y

        assert multiply(3, 5) == 15
