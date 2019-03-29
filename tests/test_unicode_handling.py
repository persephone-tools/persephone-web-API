def test_normalize_ASCII():
    """Test that normalization of ASCII remains ASCII"""
    from persephone_api import unicode_handling
    assert unicode_handling.normalize("A") == "A"
