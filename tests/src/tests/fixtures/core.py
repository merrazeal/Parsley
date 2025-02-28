import logging
from logging.config import dictConfig

import pytest

from tests.src.core.logger import LOGGING  # type: ignore


@pytest.fixture(scope="session")
def test_logger():
    dictConfig(LOGGING)
    return logging.getLogger("tests")
