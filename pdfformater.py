"""Module represents data in pdf-format"""

import math


FILE = '''%PDF-1.2
%вгПУ
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources
<<
/Font
<<
/FClassic
<<
/Type /Font
/Subtype /Type1
/BaseFont /Times-Roman
>>
/FBold
<<
/Type /Font
/Subtype /Type1
/BaseFont /Times-Bold
>>
/FItalic
<<
/Type /Font
/Subtype /Type1
/BaseFont /Times-Italic
>>
>>
>>
/MediaBox [0 0 600 {}]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length {}
>>
stream
  BT
  {}
  ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000015 00000 n
0000000064 00000 n
0000000121 00000 n
{} 00000 n
trailer
<<
/Root 1 0 R
/Size 5
>>
startxref
{}
%%EOF'''

HORIZONTAL_SHIFT = 40
VERTICAL_SHIFT = 25
PAGE_WIDTH = 600
PAGE_HEIGHT = None

FONT_SIZE_BIG = 20
FONT_SIZE_SMALL = 12


def replace_spec_symbols(string):
    """Screening of pdf-symbols in a string"""
    return string.replace('(', '\\(').replace(')', '\\)')


def to_page(text):
    """Wrap the main code in the required tags for use"""
    page_height = str(get_page_height(text))
    text_len = str(len(text) + 9)
    shift_to_text_obj = str(431 + len(page_height))
    shift_to_text_obj = '0'*(10 - len(shift_to_text_obj)) + shift_to_text_obj
    shift_to_xref = str(491 + len(page_height) + len(text_len) + len(text))
    return FILE.format(page_height, text_len, text, shift_to_text_obj, shift_to_xref)


def get_page_height(text):
    string_count = math.ceil(len(text.split('\n')) / 3)
    PAGE_HEIGHT = string_count * VERTICAL_SHIFT + 20
    return PAGE_HEIGHT


def to_head(string, current_shift):
    """Present in the form of a paragraph heading"""
    string = replace_spec_symbols(string)
    return '/FBold 15 Tf\n{} -25 Td\n({}) Tj\n'.format(HORIZONTAL_SHIFT - current_shift, string)


def to_subhead(string, current_shift):
    """Present in the form of a subheading of a paragraph"""
    string = replace_spec_symbols(string)
    return '/FBold 12 Tf\n{} -25 Td\n({}) Tj\n'.format(2*HORIZONTAL_SHIFT - current_shift, string)


def to_page_description(string, page_height):
    """Provide the first line describing the page"""
    string = replace_spec_symbols(string)
    return '/FItalic 12 Tf\n40 {} Td\n({}) Tj\n'.format(page_height - 20, string)


def to_text(text, current_shift):
    """Wrap text in the required for presentation tags"""
    text = replace_spec_symbols(text)
    splited_text = text.split('\n')
    strings_count = len(splited_text)
    if strings_count == 1:
        return '/FClassic 12 Tf\n{} -25 Td\n({}) Tj\n'.format(HORIZONTAL_SHIFT, text)
    else:
        result = '/FClassic 12 Tf\n{} -25 Td\n({}) Tj\n'.format(HORIZONTAL_SHIFT, splited_text[0])
        for i in range(1, strings_count):
            result += '/FClassic 12 Tf\n0 -25 Td\n({}) Tj\n'.format(splited_text[i])
        return result
