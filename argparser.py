import argparse

def parse_args():
    """Command-line arguments parser"""
    parser = argparse.ArgumentParser(description="DOCSTRING2PDF: "
                                                 "Get python-docstrings as PDF-file")
    parser.add_argument('fromobject', type=str, help="path to python module or module's objects. "
                                                     "Examples: /d1/module or /d1/module.Class, or "
                                                     "/d1/module.Class.func, "
                                                     "etc.")
    parser.add_argument('--to', type=str, default='results/', help="path to save PDF file. Default: "
                                                                   "results/")
    return parser.parse_args()
