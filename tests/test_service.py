from unittest.mock import patch

import pytest

from src.service import TokenService


@pytest.fixture
def service():
    return TokenService()


def test_generate_token_uses_mocked_time_and_environment(service):
    with patch("src.service.time.time", return_value=1000) as mocked_time:
        with patch("src.service.os.getenv", return_value="10") as mocked_getenv:
            token = service.generate_token("user-42")

    assert token
    mocked_time.assert_called_once_with()
    mocked_getenv.assert_called_once_with("TOKEN_LIFETIME_SEC", "3600")


def test_token_is_valid_immediately_after_generation(service):
    with patch("src.service.time.time", return_value=1000):
        with patch("src.service.os.getenv", return_value="10"):
            token = service.generate_token("user-42")

    with patch("src.service.time.time", return_value=1000):
        assert service.is_token_valid(token) is True


def test_token_expires():
    with patch("src.service.time.time", return_value=1000):
        with patch("src.service.os.getenv", return_value="10"):
            token = TokenService().generate_token("user-42")

    with patch("src.service.time.time", return_value=1005):
        assert TokenService().is_token_valid(token) is True

    with patch("src.service.time.time", return_value=1015):
        assert TokenService().is_token_valid(token) is False


@pytest.mark.parametrize(
    "lifetime, valid_time, expiration_time",
    [
        ("10", 1009, 1010),
        ("60", 1059, 1060),
    ],
)
def test_token_respects_different_environment_values(
    service, lifetime, valid_time, expiration_time
):
    with patch("src.service.time.time", return_value=1000):
        with patch("src.service.os.getenv", return_value=lifetime):
            token = service.generate_token("user-42")

    with patch("src.service.time.time", return_value=valid_time):
        assert service.is_token_valid(token) is True

    with patch("src.service.time.time", return_value=expiration_time):
        assert service.is_token_valid(token) is False


@pytest.mark.parametrize("token", ["not-base64", "", "d3Jvbmc6Zm9ybWF0"])
def test_malformed_token_is_invalid(service, token):
    with patch("src.service.time.time", return_value=1000):
        assert service.is_token_valid(token) is False