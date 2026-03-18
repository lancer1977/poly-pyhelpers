"""Test fixtures and configuration for poly-pyhelpers."""
import pytest
from pathlib import Path
from unittest.mock import MagicMock
import sys

# Ensure src is in path for imports
SRC_PATH = Path(__file__).parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def mock_response():
    """Provide a mock HTTP response object."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {}
    response.text = ""
    response.content = b""
    return response


@pytest.fixture
def sample_image_bytes():
    """Provide sample image bytes for testing."""
    # Minimal valid PNG (1x1 transparent)
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"


@pytest.fixture
def src_path():
    """Provide the path to the src directory."""
    return SRC_PATH
