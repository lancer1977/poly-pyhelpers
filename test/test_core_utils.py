import pytest
import os
import sys
import importlib.util
from pathlib import Path

# Import the module file directly to avoid broken package imports
spec = importlib.util.spec_from_file_location(
    "pyhelpers", 
    str(Path(__file__).parent.parent / "src" / "poly_pyhelpers" / "pyhelpers.py")
)
pyhelpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pyhelpers)

# Get the functions
set_working_directory_to_exe_location = pyhelpers.set_working_directory_to_exe_location
get_matching_or_first = pyhelpers.get_matching_or_first
clipString = pyhelpers.clipString
clipSting = pyhelpers.clipSting


class TestSetWorkingDirectoryToExeLocation:
    """Tests for set_working_directory_to_exe_location function."""

    def test_uses_script_directory_when_not_frozen(self, monkeypatch):
        """Non-frozen execution should switch to the module directory."""
        captured = []
        monkeypatch.delattr(sys, "frozen", raising=False)
        monkeypatch.setattr(pyhelpers.os, "chdir", captured.append)

        set_working_directory_to_exe_location()

        assert captured == [str(Path(pyhelpers.__file__).resolve().parent)]

    def test_uses_executable_directory_when_frozen(self, monkeypatch):
        """Frozen execution should switch to the executable directory."""
        captured = []
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.setattr(sys, "executable", "/tmp/poly-pyhelpers/app.exe", raising=False)
        monkeypatch.setattr(pyhelpers.os, "chdir", captured.append)

        set_working_directory_to_exe_location()

        assert captured == ["/tmp/poly-pyhelpers"]


class TestGetMatchingOrFirst:
    """Tests for get_matching_or_first function."""

    def test_returns_first_matching_item(self):
        """Test that first matching item is returned."""
        items = [1, 2, 3, 4, 5]
        result = get_matching_or_first(items, lambda x: x > 2)
        assert result == 3

    def test_returns_first_item_when_no_match(self):
        """Test that first item is returned when no predicate matches."""
        items = [1, 2, 3, 4, 5]
        result = get_matching_or_first(items, lambda x: x > 10)
        assert result == 1

    def test_returns_none_for_empty_list(self):
        """Test that None is returned for empty list."""
        result = get_matching_or_first([], lambda x: x > 0)
        assert result is None

    def test_works_with_strings(self):
        """Test matching with string items."""
        items = ["apple", "banana", "cherry", "date"]
        result = get_matching_or_first(items, lambda s: s.startswith("c"))
        assert result == "cherry"

    def test_string_fallback_returns_first(self):
        """Test string fallback when no match."""
        items = ["apple", "banana", "cherry"]
        result = get_matching_or_first(items, lambda s: s.startswith("z"))
        assert result == "apple"

    def test_works_with_dicts(self):
        """Test matching with dictionary items."""
        items = [
            {"name": "alice", "age": 30},
            {"name": "bob", "age": 25},
            {"name": "charlie", "age": 35},
        ]
        result = get_matching_or_first(items, lambda d: d["age"] > 30)
        assert result == {"name": "charlie", "age": 35}

    def test_dict_fallback_returns_first(self):
        """Test dict fallback when no match."""
        items = [{"name": "alice"}, {"name": "bob"}]
        result = get_matching_or_first(items, lambda d: d["name"] == "charlie")
        assert result == {"name": "alice"}


class TestClipSting:
    """Tests for clipString and clipSting compatibility."""

    def test_clipstring_and_alias_match(self):
        """clipString and legacy clipSting should return identical values."""
        assert clipString("hello world", 5) == "hello..."
        assert clipSting("hello world", 5) == "hello..."


    def test_returns_empty_string_for_none(self):
        """Test that None returns empty string."""
        result = clipSting(None, 10)
        assert result == ""

    def test_returns_empty_string_for_empty_string(self):
        """Test that empty string returns empty string."""
        result = clipSting("", 10)
        assert result == ""

    def test_returns_unchanged_when_under_max(self):
        """Test string unchanged when under max length."""
        result = clipSting("hello", 10)
        assert result == "hello"

    def test_clips_when_at_max_length(self):
        """Test string clipped when at max length."""
        result = clipSting("hello", 5)
        assert result == "hello"

    def test_clips_with_ellipsis_when_over_max(self):
        """Test string clipped with ellipsis when over max."""
        # The function clips to max chars then adds "..."
        # "hello world" (11 chars) with max=8 -> "hello wo" + "..." = "hello wo..."
        result = clipSting("hello world", 8)
        assert result == "hello wo..."

    def test_respects_various_max_lengths(self):
        """Test clipping with various max lengths."""
        assert clipSting("abcdefghij", 5) == "abcde..."
        assert clipSting("abcdefghij", 3) == "abc..."
        assert clipSting("abcdefghij", 1) == "a..."

    def test_works_with_special_characters(self):
        """Test clipping with special characters."""
        result = clipSting("hello world! 🌍", 10)
        assert result == "hello worl..."

    def test_zero_max_returns_ellipsis_only(self):
        """Test that zero max length returns just ellipsis."""
        result = clipSting("text", 0)
        assert result == "..."
