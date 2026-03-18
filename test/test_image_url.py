import pytest
import os
import sys
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
import requests

# Import the module file directly to avoid broken package imports
spec = importlib.util.spec_from_file_location(
    "pyhelpers", 
    str(Path(__file__).parent.parent / "src" / "poly_pyhelpers" / "pyhelpers.py")
)
pyhelpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pyhelpers)

# Get the function
save_image_from_url = pyhelpers.save_image_from_url


class TestSaveImageFromUrl:
    """Tests for save_image_from_url function."""

    def test_successful_image_download(self):
        """Test successful image download and save."""
        # Patch at the module level we imported
        original_requests = pyhelpers.requests
        original_image = pyhelpers.Image
        
        try:
            # Replace with mocks
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'fake_image_data'
            pyhelpers.requests = Mock(get=Mock(return_value=mock_response))
            
            mock_img = Mock()
            pyhelpers.Image = Mock(open=Mock(return_value=mock_img))

            # Call the function
            save_image_from_url("https://example.com/image.png", "/tmp/test_image.png")

            # Verify requests.get was called
            pyhelpers.requests.get.assert_called_once_with("https://example.com/image.png")

            # Verify image was opened from the response content
            pyhelpers.Image.open.assert_called_once()
            call_args = pyhelpers.Image.open.call_args[0][0]
            assert isinstance(call_args, BytesIO)
            assert call_args.getvalue() == b'fake_image_data'

            # Verify image was saved to the expected path
            mock_img.save.assert_called_once_with("/tmp/test_image.png")
        finally:
            # Restore
            pyhelpers.requests = original_requests
            pyhelpers.Image = original_image

    def test_404_error_handling(self):
        """Test 404 error handling."""
        original_requests = pyhelpers.requests
        
        try:
            mock_response = Mock()
            mock_response.status_code = 404
            pyhelpers.requests = Mock(get=Mock(return_value=mock_response))

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                save_image_from_url("https://example.com/notfound.png", "/tmp/image.png")

            output = f.getvalue()
            assert "Failed to download image" in output
            assert "404" in output
        finally:
            pyhelpers.requests = original_requests

    def test_500_error_handling(self):
        """Test 500 error handling."""
        original_requests = pyhelpers.requests

        try:
            mock_response = Mock()
            mock_response.status_code = 500
            pyhelpers.requests = Mock(get=Mock(return_value=mock_response))

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                save_image_from_url("https://example.com/servererror.png", "/tmp/image.png")

            output = f.getvalue()
            assert "Failed to download image" in output
            assert "500" in output
        finally:
            pyhelpers.requests = original_requests

    def test_timeout_handling(self):
        """Test network timeout handling."""
        original_requests = pyhelpers.requests
        
        try:
            pyhelpers.requests = Mock()
            pyhelpers.requests.get.side_effect = requests.Timeout("Connection timed out")

            with pytest.raises(requests.Timeout):
                save_image_from_url("https://example.com/slow.png", "/tmp/image.png")
        finally:
            pyhelpers.requests = original_requests

    def test_invalid_url_none(self):
        """Test handling of None URL."""
        original_requests = pyhelpers.requests
        
        try:
            pyhelpers.requests = Mock()
            
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                save_image_from_url(None, "/tmp/image.png")

            # Should NOT have called requests.get
            pyhelpers.requests.get.assert_not_called()
        finally:
            pyhelpers.requests = original_requests

    def test_invalid_url_empty(self):
        """Test handling of empty URL."""
        original_requests = pyhelpers.requests
        
        try:
            pyhelpers.requests = Mock()
            
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                save_image_from_url("", "/tmp/image.png")

            # Should NOT have called requests.get
            pyhelpers.requests.get.assert_not_called()
        finally:
            pyhelpers.requests = original_requests
