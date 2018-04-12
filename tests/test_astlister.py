import sys
import os
import ast
import unittest
from unittest import TestCase

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

from astlister import ArgLister
from astlister import FuncLister, FuncInfo
from astlister import ClassLister, ClassInfo
from astlister import ModuleLister, ModuleInfo


class TestArgListerForFuncWithoutArgs(TestCase):
    """Test for function ast-node without args"""

    def setUp(self):
        """Define function without args ast-node and list it"""
        func_node_without_args = ast.FunctionDef(name='func',
                                                 args=ast.arguments(args=[],
                                                                    vararg=None,
                                                                    kwonlyargs=[],
                                                                    kw_defaults=[],
                                                                    kwarg=None,
                                                                    defaults=[]),
                                                 body=[ast.Pass()],
                                                 decorator_list=None,
                                                 returns=None)
        self.arg_lister = ArgLister()
        self.arg_lister.visit(func_node_without_args)

    def do_assertion(self):
        self.assertEqual([], self.arg_lister.args)

    def test_args(self):
        self.do_assertion()

    def test_visit_arg(self):
        self.do_assertion()


class TestArgListerForFuncWithArgs(TestCase):
    """Test for function ast-node with args"""

    def setUp(self):
        func_node_with_args = ast.FunctionDef(name='func',
                                              args=ast.arguments(args=[ast.arg(arg='a',
                                                                               annotation=ast.Str(s='annotation')),
                                                                       ast.arg(arg='b',
                                                                               annotation=None),
                                                                       ast.arg(arg='c',
                                                                               annotation=None)],
                                                                 vararg=ast.arg(arg='d',
                                                                                annotation=None),
                                                                 kwonlyargs=[ast.arg(arg='e',
                                                                                     annotation=None),
                                                                             ast.arg(arg='f',
                                                                                     annotation=None)],
                                                                 kw_defaults=[None,
                                                                              ast.Num(n=3)],
                                                                 kwarg=ast.arg(arg='g',
                                                                               annotation=None),
                                                                 defaults=[ast.Num(n=1),
                                                                           ast.Num(n=2)]),
                                              body=[ast.Pass()],
                                              decorator_list=None,
                                              returns=None)
        self.arg_lister = ArgLister()
        self.arg_lister.visit(func_node_with_args)

    def do_assertion(self):
        self.assertEqual(['a', 'b', 'c', 'd', 'e', 'f', 'g'], self.arg_lister.args)

    def test_args(self):
        self.do_assertion()

    def test_visit_arg(self):
        self.do_assertion()


class TestFuncListerWithoutDocstringsAndArgs(TestCase):
    def setUp(self):
        self.func_node = ast.FunctionDef(name='func',
                                         args=ast.arguments(args=[],
                                                            vararg=None,
                                                            kwonlyargs=[],
                                                            kw_defaults=[],
                                                            kwarg=None,
                                                            defaults=[]),
                                         body=[ast.Pass()],
                                         decorator_list=[],
                                         returns=None)
        self.func_lister = FuncLister()
        self.func_lister.visit(self.func_node)

    def do_assertion(self):
        correct_func_info = [FuncInfo(name='func',
                                      signature=[],
                                      docstrings=None)]

        self.assertEqual(correct_func_info, self.func_lister.functions_info)

    def test_functions_info(self):
        self.do_assertion()

    def test_visit_FunctionDef(self):
        self.do_assertion()

    def test_get_func_signature(self):
        self.assertEqual([], self.func_lister.get_func_signature(self.func_node))


class TestFuncListerWithDocstrings(TestCase):

    def setUp(self):
        self.func_node = ast.FunctionDef(name='module_to_pdf',
                                         args=ast.arguments(args=[ast.arg(arg='self',
                                                                          annotation=None),
                                                                  ast.arg(arg='module_info',
                                                                          annotation=None)],
                                                            vararg=None,
                                                            kwonlyargs=[],
                                                            kw_defaults=[],
                                                            kwarg=None,
                                                            defaults=[]),
                                         body=[ast.Expr(value=ast.Str(s="PDF-representation of module's docstrings")),
                                               ast.Pass()],
                                         decorator_list=[],
                                         returns=None)
        self.func_lister = FuncLister()
        self.func_lister.visit(self.func_node)

    def do_assertion(self):
        correct_func_info = [FuncInfo(name='module_to_pdf',
                                      signature=['self', 'module_info'],
                                      docstrings="PDF-representation of module's docstrings")]

        self.assertEqual(correct_func_info, self.func_lister.functions_info)

    def test_functions_info(self):
        self.do_assertion()

    def test_visit_FunctionDef(self):
        self.do_assertion()

    def test_get_func_signature(self):
        self.assertEqual(['self', 'module_info'],  self.func_lister.get_func_signature(self.func_node))


class TestClassLister(TestCase):
    def setUp(self):
        class_node = ast.ClassDef(name='Class',
                                  bases=[],
                                  keywords=[],
                                  body=[ast.Expr(value=ast.Str(s='Class docstrings')),
                                        ast.FunctionDef(name='__init__',
                                                        args=ast.arguments(args=[ast.arg(arg='self',
                                                                                         annotation=None)],
                                                                           vararg=None,
                                                                           kwonlyargs=[],
                                                                           kw_defaults=[],
                                                                           kwarg=None,
                                                                           defaults=[]),
                                                        body=[ast.Expr(value=ast.Str(s="Constructor's docstrings")),
                                                              ast.Pass()],
                                                        decorator_list=[],
                                                        returns=None),
                                        ast.FunctionDef(name='_private_func',
                                                        args=ast.arguments(args=[ast.arg(arg='self',
                                                                                         annotation=None),
                                                                                 ast.arg(arg='arg',
                                                                                         annotation=None)],
                                                                           vararg=None,
                                                                           kwonlyargs=[],
                                                                           kw_defaults=[],
                                                                           kwarg=None,
                                                                           defaults=[]),
                                                        body=[ast.Pass()],
                                                        decorator_list=[],
                                                        returns=None),
                                        ast.FunctionDef(name='func_without_args',
                                                        args=ast.arguments(args=[],
                                                                           vararg=None,
                                                                           kwonlyargs=[],
                                                                           kw_defaults=[],
                                                                           kwarg=None,
                                                                           defaults=[]),
                                                        body=[ast.Expr(value=ast.Str(s='Func docstrings')),
                                                              ast.Pass()],
                                                        decorator_list=[ast.Name(id='staticmethod',
                                                                                 ctx=ast.Load())],
                                                        returns=None),
                                        ast.FunctionDef(name='func_with_args',
                                                        args=ast.arguments(args=[ast.arg(arg='self',
                                                                                         annotation=None),
                                                                                 ast.arg(arg='a', annotation=None),
                                                                                 ast.arg(arg='b', annotation=None),
                                                                                 ast.arg(arg='c', annotation=None)],
                                                                           kwonlyargs=[],
                                                                           kw_defaults=[],
                                                                           kwarg=None,
                                                                           defaults=[]),
                                                        body=[ast.Pass()],
                                                        decorator_list=[],
                                                        returns=None)],
                                  decorator_list=[])
        self.class_lister = ClassLister()
        self.class_lister.visit(class_node)

    def do_assertion(self):
        correct_classes_info = [ClassInfo(name='Class',
                                          docstrings='Class docstrings',
                                          functions=[FuncInfo(name='__init__',
                                                              signature=['self'],
                                                              docstrings="Constructor's docstrings"),
                                                     FuncInfo(name='_private_func',
                                                              signature=['self', 'arg'],
                                                              docstrings=None),
                                                     FuncInfo(name='func_without_args',
                                                              signature=[],
                                                              docstrings='Func docstrings'),
                                                     FuncInfo(name='func_with_args',
                                                              signature=['self', 'a', 'b', 'c'],
                                                              docstrings=None)])]

        self.assertEqual(correct_classes_info, self.class_lister.classes_info)

    def test_classes_info(self):
        self.do_assertion()

    def test_visit_ClassDef(self):
        self.do_assertion()


class TestClassListerWithNamedTuples(TestCase):
    def setUp(self):
        namedtuple_node = ast.Assign(targets=[ast.Name(id='Namedtuple',
                                                       ctx=ast.Store())],
                                     value=ast.Call(func=ast.Name(id='namedtuple',
                                                                  ctx=ast.Load()),
                                                    args=[ast.Str(s='Namedtuple'),
                                                          ast.Str(s='arg1 arg2 arg3')],
                                                    keywords=[]))
        self.class_lister = ClassLister()
        self.class_lister.visit(namedtuple_node)

    def do_assertion(self):
        correct_classes_info = [ClassInfo(name='Namedtuple',
                                          docstrings='Namedtuple(arg1, arg2, arg3)',
                                          functions=None)]

        self.assertEqual(correct_classes_info, self.class_lister.classes_info)

    def test_classes_info(self):
        self.do_assertion()

    def test_visit_Assign(self):
        self.do_assertion()


class TestModuleLister(TestCase):
    def setUp(self):
        self.module = '''

"""
Module docstrings
"""

from collections import namedtuple


Namedtuple = namedtuple("Namedtuple", "arg1 arg2 arg3")

class SomeClass:
    """Class docstrings"""

    def some_func():
        """Func docstrings"""
        pass

    def another_func(arg1, arg2=3):
        pass

class AnotherClass:
    pass

def module_func():
    """Another docstrings"""
    pass

def another_module_func(a, b, c, d):
    pass

        '''
        self.module_node = ast.parse(self.module)
        self.module_lister = ModuleLister('test_module', self.module_node)

    def test_module_info(self):
        correct_module_info = ModuleInfo(name='test_module',
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

        self.assertEqual(correct_module_info, self.module_lister.module_info)


if __name__ == '__main__':
    unittest.main()
