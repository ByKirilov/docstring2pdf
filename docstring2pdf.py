"""
Get python-docstrings in PDF-format
"""

import os
import sys
import ast
import astlister
import argparser
from collections import namedtuple
from os.path import basename
from pdfdocrepr import PDF_Doc_Repr

Object = namedtuple('Object', 'file_path module_name first_obj second_obj')


def main():
    args = argparser.parse_args()
    pdf_doc = PDF_Doc()
    pdf = pdf_doc.get_pdf_doc(args.fromobject)
    if args.to == 'results/':
        _save_pdf('results/', pdf_doc.full_name, pdf)
    else:
        _save_pdf(args.to, pdf_doc.full_name, pdf)


def _save_pdf(directory, name, pdf):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + '/' + name + '.pdf', 'w', encoding='utf-8') as f:
        f.write(pdf)


class PDF_Doc:
    """
    Get info and docstrings from python-file
    """

    def __init__(self):
        self.full_name = ''

    def _parse_object_name(self, object_path):
        path_list = object_path.split('/')
        self.full_name = path_list[-1]
        split_name = path_list[-1].split('.')
        length = len(split_name)

        if len(path_list) > 1:
            file_path = '/'.join(path_list[:-1]) + '/' + split_name[0] + '.py'
        else:
            file_path = split_name[0] + '.py'
        module_name = basename(file_path).split('.')[0]

        first_obj = None
        if length >= 2:
            first_obj = split_name[1]

        second_obj = None
        if length == 3:
            second_obj = split_name[2]

        return Object(file_path, module_name, first_obj, second_obj)

    @staticmethod
    def _extract_classes_info(obj_info, class_name):
        for cls in obj_info.classes:
            if cls.name == class_name:
                return cls
        return None

    @staticmethod
    def _extract_functions_info(obj_info, fnc_name):
        for fnc in obj_info.functions:
            if fnc.name == fnc_name:
                return fnc
        return None

    def get_pdf_doc(self, filename):
        """Get pdf-docstrings to Object"""
        obj = self._parse_object_name(filename)
        try:
            with open(obj.file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except (FileNotFoundError, AttributeError):
            sys.stderr.write("No such module, class or function. Read help.\n")
            sys.exit()

        tree = ast.parse(code)
        lister = astlister.ModuleLister(obj.module_name, tree)
        pdf_doc = PDF_Doc_Repr()

        mod_info = lister.module_info

        if obj.first_obj is not None and obj.second_obj is None:
            cls_info = self._extract_classes_info(mod_info, obj.first_obj)
            if cls_info is None:
                fnc_info = self._extract_functions_info(mod_info, obj.first_obj)
                return pdf_doc.function_to_pdf(fnc_info, None, obj.module_name)
            else:
                return pdf_doc.class_to_pdf(cls_info, obj.module_name)
        elif obj.second_obj is not None:
            cls_info = self._extract_classes_info(mod_info, obj.first_obj)
            fnc_info = self._extract_functions_info(cls_info, obj.second_obj)
            return pdf_doc.function_to_pdf(fnc_info, obj.first_obj, obj.module_name)
        else:
            return pdf_doc.module_to_pdf(mod_info)


if __name__ == "__main__":
    main()
