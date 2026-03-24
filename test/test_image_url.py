
import pytest
import responses
import os
from PIL import Image
from poly_pyhelpers.pyhelpers import save_image_from_url

# Minimal valid 1x1 GIF
GIF_DATA = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_save_image_from_url_success(mocked_responses, tmp_path):
    """Tests successful image download and save."""
    image_url = "http://example.com/image.gif"
    save_path = tmp_path / "image.gif"
    mocked_responses.add(responses.GET, image_url, body=GIF_DATA, status=200, content_type='image/gif')

    result = save_image_from_url(image_url, str(save_path))

    assert result is True
    assert save_path.exists()
    # Verify that the saved file is a valid image with the correct properties
    with Image.open(save_path) as img:
        assert img.size == (1, 1)
        assert img.format == 'GIF'

def test_save_image_from_url_not_found(mocked_responses, tmp_path):
    """Tests handling of a 404 Not Found error."""
    image_url = "http://example.com/not_found.gif"
    save_path = tmp_path / "not_found.gif"
    mocked_responses.add(responses.GET, image_url, status=404)

    result = save_image_from_url(image_url, str(save_path))

    assert result is False
    assert not save_path.exists()

def test_save_image_from_url_invalid_url(tmp_path):
    """Tests handling of a malformed URL."""
    image_url = "not-a-valid-url"
    save_path = tmp_path / "image.gif"

    result = save_image_from_url(image_url, str(save_path))

    assert result is False
    assert not save_path.exists()

def test_save_image_from_url_permission_error(mocked_responses, tmp_path):
    """Tests handling of a file system permission error."""
    image_url = "http://example.com/image.gif"
    # Create a read-only directory
    read_only_dir = tmp_path / "read_only"
    read_only_dir.mkdir()
    save_path = read_only_dir / "image.gif"
    # Make the directory read-only *after* creating the path object
    read_only_dir.chmod(0o555)

    mocked_responses.add(responses.GET, image_url, body=GIF_DATA, status=200, content_type='image/gif')

    result = save_image_from_url(image_url, str(save_path))

    assert result is False
    assert not save_path.exists()
