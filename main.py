#if we don't want to use the UI, then put the filename here.

from ocr import perform_ocr

perform_ocr("test.jpg")

import os
os.startfile("output.txt")