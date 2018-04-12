import sys
import os
import unittest
from unittest import TestCase

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

import docstring2pdf
from docstring2pdf import Object
from astlister import ModuleInfo, ClassInfo, FuncInfo


class TestPDFDoc(TestCase):
    def setUp(self):
        self.doc2pdf = docstring2pdf.PDF_Doc()

    def test__parse_object_name(self):
        correct_object = Object(file_path='/1/2/3/module.py',
                                module_name='module',
                                first_obj=None,
                                second_obj=None)
        self.assertEqual(correct_object, self.doc2pdf._parse_object_name('/1/2/3/module'))

        correct_object = Object(file_path='/1/2/3/module.py',
                                module_name='module',
                                first_obj='Class',
                                second_obj=None)

        self.assertEqual(correct_object, self.doc2pdf._parse_object_name('/1/2/3/module.Class'))

        correct_object = Object(file_path='/1/2/3/module.py',
                                module_name='module',
                                first_obj='Class',
                                second_obj='func')

        self.assertEqual(correct_object, self.doc2pdf._parse_object_name('/1/2/3/module.Class.func'))

    def test__extract_classes_info(self):
        module_info = ModuleInfo(name='test_module',
                                 docstrings='Module docstrings',
                                 classes=[ClassInfo(name='Namedtuple',
                                                    docstrings='Namedtuple(arg1, arg2, arg3)',
                                                    functions=None),
                                          ClassInfo(name='SomeClass',
                                                    docstrings='Class docstrings',
                                                    functions=[FuncInfo(name='some_func',
                                                                        signature=[],
                                                                        docstrings='Func docstrings'),
                                                               FuncInfo(name='another_func',
                                                                        signature=['arg1', 'arg2'],
                                                                        docstrings=None)]),
                                          ClassInfo(name='AnotherClass',
                                                    docstrings=None,
                                                    functions=[])],
                                 functions=[FuncInfo(name='module_func',
                                                     signature=[],
                                                     docstrings='Another docstrings'),
                                            FuncInfo(name='another_module_func',
                                                     signature=['a', 'b', 'c', 'd'],
                                                     docstrings=None)])
        correct_info = ClassInfo(name='SomeClass',
                                 docstrings='Class docstrings',
                                 functions=[FuncInfo(name='some_func',
                                                     signature=[],
                                                     docstrings='Func docstrings'),
                                            FuncInfo(name='another_func',
                                                     signature=['arg1', 'arg2'],
                                                     docstrings=None)])

        self.assertEqual(correct_info, self.doc2pdf._extract_classes_info(module_info, 'SomeClass'))

    def test__extract_functions_info(self):
        module_info = ModuleInfo(name='test_module',
                                 docstrings='Module docstrings',
                                 classes=[ClassInfo(name='SomeClass',
                                                    docstrings='Class docstrings',
                                                    functions=[FuncInfo(name='some_func',
                                                                        signature=[],
                                                                        docstrings='Func docstrings'),
                                                               FuncInfo(name='another_func',
                                                                        signature=['arg1', 'arg2'],
                                                                        docstrings=None)])],
                                 functions=[FuncInfo(name='module_func',
                                                     signature=[],
                                                     docstrings='Another docstrings')])
        correct_info = FuncInfo(name='module_func',
                                signature=[],
                                docstrings='Another docstrings')

        self.assertEqual(correct_info, self.doc2pdf._extract_functions_info(module_info, 'module_func'))

        class_info = ClassInfo(name='SomeClass',
                               docstrings='Class docstrings',
                               functions=[FuncInfo(name='some_func',
                                                   signature=[],
                                                   docstrings='Func docstrings')])
        correct_info = FuncInfo(name='some_func',
                                signature=[],
                                docstrings='Func docstrings')

        self.assertEqual(correct_info, self.doc2pdf._extract_functions_info(class_info, 'some_func'))


if __name__ == '__main__':
    unittest.main()
