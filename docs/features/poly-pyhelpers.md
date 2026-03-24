---
title: poly-pyhelpers Core Functions
status: done
owner: @DreadBreadcrumb
priority: high
complexity: 1
created: 2026-03-19
updated: 2026-03-24
tags: [documentation, poly-pyhelpers, utilities]
---

# poly-pyhelpers

A collection of Python helper utilities for common tasks.

## Installation

```bash
pip install poly-pyhelpers
```

## Core Functions

### `set_working_directory_to_exe_location()`

Changes the current working directory to the location of the executable. Useful for PyInstaller-generated executables to ensure relative paths work correctly.

**Behavior:**
- If running as a frozen executable (e.g., PyInstaller), changes to the executable's directory
- If running in a development environment, changes to the script's directory

```python
from poly_pyhelpers import set_working_directory_to_exe_location
set_working_directory_to_exe_location()
```

---

### `save_image_from_url(url, save_path)`

Downloads an image from a URL and saves it to disk.

**Parameters:**
- `url` (str): The URL of the image to download
- `save_path` (str): The local file path to save the image

**Returns:** `bool` - `True` on success, `False` on failure

**Behavior:**
- Returns `False` if URL is `None` or empty
- Uses `requests` to fetch the image
- Uses PIL/Pillow to save the image in the appropriate format

```python
from poly_pyhelpers import save_image_from_url
success = save_image_from_url("https://example.com/image.png", "local_image.png")
```

---

### `get_matching_or_first(items, predicate)`

Finds the first item in a list that matches a predicate, or returns the first item if no match is found.

**Parameters:**
- `items` (list): List of items to search
- `predicate` (callable): A function that takes an item and returns `True`/``False`

**Returns:** The first matching item, or the first item in the list if no match, or `None` if list is empty

```python
from poly_pyhelpers import get_matching_or_first

items = ["apple", "banana", "cherry"]
result = get_matching_or_first(items, lambda x: x.startswith("b"))
# Returns "banana"

# No match - returns first item
result = get_matching_or_first(items, lambda x: x.startswith("z"))
# Returns "apple"

# Empty list
result = get_matching_or_first([], lambda x: True)
# Returns None
```

---

### `clipString(value, max)`

Truncates a string to a maximum length, appending "..." if truncated.

**Parameters:**
- `value` (str): The string to clip
- `max` (int): Maximum length before truncation

**Returns:** `str` - The clipped string

**Behavior:**
- Returns empty string if value is `None`
- Appends "..." when truncating

```python
from poly_pyhelpers import clipString

result = clipString("Hello World", 5)
# Returns "Hello..."

result = clipString("Hi", 10)
# Returns "Hi"

result = clipString(None, 5)
# Returns ""
```

---

### `clipSting(value, max)`

Backward-compatible typo alias for `clipString`. Deprecated but maintained for compatibility.

```python
from poly_pyhelpers import clipSting
result = clipSting("Long text here", 10)  # Returns "Long tex..."
```

## Dependencies

- `requests`
- `Pillow` (PIL)