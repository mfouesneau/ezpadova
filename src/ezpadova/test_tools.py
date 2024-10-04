import warnings
from .tools import deprecated_replacedby

def test_deprecated_replacedby():
    @deprecated_replacedby("new_function")
    def old_function():
        """This is the old function."""
        return "old"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = old_function()
        
        # Check that a warning was raised
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "old_function is deprecated and will be removed in a future version. Use new_function instead." in str(w[-1].message)
        
        # Check the result of the function
        assert result == "old"
        
        # Check the docstring
        assert old_function.__doc__.startswith("old_function is deprecated and will be removed in a future version. Use new_function instead.")
        assert "This is the old function." in old_function.__doc__