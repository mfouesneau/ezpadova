from io import BytesIO
from functools import wraps
import warnings


def deprecated_replacedby(replace_by):
    """ This is a decorator which can be used to mark functions as deprecated. """

    def decorator(func):
        msg = f"{func.__name__} is deprecated and will be removed in a future version. Use {replace_by} instead."

        @wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(msg, DeprecationWarning)
            return func(*args, **kwargs)
        
        # add to docstring
        new_func.__doc__ = f"{msg}\n\n{func.__doc__}"
        
        return new_func
    return decorator


def get_file_archive_type(filename: str | BytesIO, stream: bool = False) -> str | None:
    """ Detect the type of a potentially compressed file.

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
    magic_dict = { b"\x1f\x8b\x08": "gz", b"\x42\x5a\x68": "bz2", b"\x50\x4b\x03\x04": "zip" }

    max_len = max(len(x) for x in magic_dict)
    if not stream:
        with open(filename, 'rb') as f:
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