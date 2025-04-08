import os
from io import BytesIO

from .config import generate_doc, update_config
from .parsec import build_query, get_file_archive_type, get_isochrones


def test_get_file_archive_type():
    # Test with gzip file
    gzip_file = BytesIO(b"\x1f\x8b\x08")
    assert get_file_archive_type(gzip_file, stream=True) == "gz"

    # Test with bzip2 file
    bzip2_file = BytesIO(b"\x42\x5a\x68")
    assert get_file_archive_type(bzip2_file, stream=True) == "bz2"

    # Test with zip file
    zip_file = BytesIO(b"\x50\x4b\x03\x04")
    assert get_file_archive_type(zip_file, stream=True) == "zip"

    # Test with uncompressed file
    uncompressed_file = BytesIO(b"plain text")
    assert get_file_archive_type(uncompressed_file, stream=True) is None

    # Test with file path (mocking open)
    with open("test.gz", "wb") as f:
        f.write(b"\x1f\x8b\x08")
    assert get_file_archive_type("test.gz") == "gz"
    os.remove("test.gz")

    with open("test.bz2", "wb") as f:
        f.write(b"\x42\x5a\x68")
    assert get_file_archive_type("test.bz2") == "bz2"
    os.remove("test.bz2")

    with open("test.zip", "wb") as f:
        f.write(b"\x50\x4b\x03\x04")
    assert get_file_archive_type("test.zip") == "zip"
    os.remove("test.zip")

    with open("test.txt", "wb") as f:
        f.write(b"plain text")
    assert get_file_archive_type("test.txt") is None
    os.remove("test.txt")


def test_configuration_update_and_doc():
    update_config()
    generate_doc()


def test_build_query():
    # Test with default configuration
    result = build_query()
    assert result["photsys_file"] == "YBC_tab_mag_odfnew/tab_mag_ubvrijhk.dat"
    assert result["imf_file"] == "tab_imf/imf_kroupa_orig.dat"

    # Test with custom photsys_file
    result = build_query(photsys_file="ugriz")
    assert result["photsys_file"] == "YBC_tab_mag_odfnew/tab_mag_ugriz.dat"
    assert result["imf_file"] == "tab_imf/imf_kroupa_orig.dat"

    # Test with custom imf_file
    result = build_query(imf_file="salpeter")
    assert result["photsys_file"] == "YBC_tab_mag_odfnew/tab_mag_ubvrijhk.dat"
    assert result["imf_file"] == "tab_imf/imf_salpeter.dat"

    # Test with both custom photsys_file and imf_file
    result = build_query(photsys_file="ugriz", imf_file="salpeter")
    assert result["photsys_file"] == "YBC_tab_mag_odfnew/tab_mag_ugriz.dat"
    assert result["imf_file"] == "tab_imf/imf_salpeter.dat"


def test_end_to_end():
    get_isochrones(default_ranges=True)


def test_readme_example():
    get_isochrones(photsys_file='gaiaEDR3', logage=(6, 10, 0.2), MH=(-2, 1, 0.4))
