""" This module contains utility functions used by the ezpadova package. """
import re
import warnings
from functools import wraps
from io import BytesIO
from typing import Union


def dedent(text: str) -> str:
    """Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalized to a newline character.
    """
    # Look for the longest leading string of spaces and tabs common to
    # all lines.
    _whitespace_only_re = re.compile("^[ \t]+$", re.MULTILINE)
    _leading_whitespace_re = re.compile("(^[ \t]*)(?:[^ \t\n])", re.MULTILINE)

    margin = None
    text = _whitespace_only_re.sub("", text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent

        # Current line more deeply indented than previous winner:
        # no change (previous winner is still on top).
        elif indent.startswith(margin):
            pass

        # Current line consistent with and no deeper than previous winner:
        # it's the new winner.
        elif margin.startswith(indent):
            margin = indent

        # Find the largest common whitespace between current line and previous
        # winner.
        else:
            for i, (x, y) in enumerate(zip(margin, indent)):
                if x != y:
                    margin = margin[:i]
                    break

    # sanity check (testing/debugging only)
    if 0 and margin:
        for line in text.split("\n"):
            assert not line or line.startswith(margin), "line = %r, margin = %r" % (
                line,
                margin,
            )

    if margin:
        text = re.sub(r"(?m)^" + margin, "", text)
    return text


def deprecated_replacedby(replace_by):
    """
    This is a decorator which can be used to mark functions as deprecated.

    Parameters:
        replace_by (str): The name of the function that should be used instead of the deprecated one.

    Returns:
        function: A decorator that can be applied to functions to mark them as deprecated.

    Example:
        .. code-block:: python

            @deprecated_replacedby('new_function')
            def old_function():
                '''This is the old function.'''
                pass

            # When old_function is called, a DeprecationWarning will be issued, and the docstring will be updated to indicate the deprecation.

    """
    def decorator(func):
        msg = f".. deprecated:: 2.0\n  {func.__name__} is deprecated and will be removed in a future version. Use :func:`{replace_by}` instead."
        doc = dedent(func.__doc__)

        @wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(msg, DeprecationWarning)
            return func(*args, **kwargs)

        # add to docstring
        new_func.__doc__ = f"{doc}\n\n{msg}"

        return new_func

    return decorator


def get_file_archive_type(
    filename: Union[str, BytesIO], stream: bool = False
) -> Union[str, None]:
    """Detect the type of a potentially compressed file.

    This function checks the beginning of a file to determine if it is compressed
    using gzip, bzip2, or zip formats. It returns the corresponding file type if
    a compression is detected, otherwise it returns None.

    Args:
        filename (str | BytesIO): The path to the file or a BytesIO stream to check.
        stream (bool): If True, `filename` is treated as a BytesIO stream. If False,
                       `filename` is treated as a file path.

    Returns:
        str | None: The type of compression detected ('gz', 'bz2', 'zip'), or None if
                    no compression is detected.
    """
    magic_dict = {
        b"\x1f\x8b\x08": "gz",
        b"\x42\x5a\x68": "bz2",
        b"\x50\x4b\x03\x04": "zip",
    }

    max_len = max(len(x) for x in magic_dict)
    if not stream:
        with open(filename, "rb") as f:
            file_start = f.read(max_len)
    else:
        try:
            file_pos = filename.tell()
            file_start = filename.read(max_len)
            filename.seek(file_pos)
        except AttributeError:
            file_start = filename[:max_len]

    for magic, filetype in magic_dict.items():
        if file_start.startswith(magic):
            return filetype

    return None
