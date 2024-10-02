import os
from io import BytesIO
from bs4 import BeautifulSoup
from .newparsec import _get_photsys_info
from .newparsec import get_file_archive_type
from .newparsec import update_config, generate_doc

def test_get_photsys_info():
    html_content = """
    <form>
        <select name="photsys_file">
            <option value="tab_mag_odfnew/tab_mag_ubvrijhk.dat">UBVRIJHK</option>
            <option value="tab_mag_odfnew/tab_mag_ugriz.dat">ugriz</option>
        </select>
    </form>
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')
    
    expected_output = {
        'ubvrijhk': ('UBVRIJHK', 'tab_mag_odfnew/tab_mag_ubvrijhk.dat'),
        'ugriz': ('ugriz', 'tab_mag_odfnew/tab_mag_ugriz.dat')
    }
    
    assert _get_photsys_info(forms) == expected_output

def test_get_file_archive_type():
    # Test with gzip file
    gzip_file = BytesIO(b'\x1f\x8b\x08')
    assert get_file_archive_type(gzip_file, stream=True) == 'gz'

    # Test with bzip2 file
    bzip2_file = BytesIO(b'\x42\x5a\x68')
    assert get_file_archive_type(bzip2_file, stream=True) == 'bz2'

    # Test with zip file
    zip_file = BytesIO(b'\x50\x4b\x03\x04')
    assert get_file_archive_type(zip_file, stream=True) == 'zip'

    # Test with uncompressed file
    uncompressed_file = BytesIO(b'plain text')
    assert get_file_archive_type(uncompressed_file, stream=True) is None

    # Test with file path (mocking open)
    with open('test.gz', 'wb') as f:
        f.write(b'\x1f\x8b\x08')
    assert get_file_archive_type('test.gz') == 'gz'
    os.remove('test.gz')

    with open('test.bz2', 'wb') as f:
        f.write(b'\x42\x5a\x68')
    assert get_file_archive_type('test.bz2') == 'bz2'
    os.remove('test.bz2')

    with open('test.zip', 'wb') as f:
        f.write(b'\x50\x4b\x03\x04')
    assert get_file_archive_type('test.zip') == 'zip'
    os.remove('test.zip')

    with open('test.txt', 'wb') as f:
        f.write(b'plain text')
    assert get_file_archive_type('test.txt') is None
    os.remove('test.txt')


def test_configuration():
    update_config()
    generate_doc()