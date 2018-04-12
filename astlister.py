"""
Module get info from modules,
classes, functions and other data
"""

import ast
from collections import namedtuple


ModuleInfo = namedtuple('ModuleInfo', 'name docstrings classes functions')
ClassInfo = namedtuple('ClassInfo', 'name docstrings functions')
FuncInfo = namedtuple('FuncInfo', 'name signature docstrings')


class ModuleLister:
    """Read module to get info"""

    def __init__(self, module_name, module_node):
        """Constructor gets module name as a string and a module AST-node"""
        self.module_name = module_name
        self.module_node = module_node
        self._module_info = None
        self._set_module_info()

    @property
    def module_info(self):
        """Return module_info list which save ModuleInfo instance"""
        return self._module_info

    def _set_module_info(self):
        name = self.module_name

        docstrings = ast.get_docstring(self.module_node)

        class_lister = ClassLister()
        for child in ast.iter_child_nodes(self.module_node):
            if type(child) == ast.ClassDef or type(child) == ast.Assign:
                class_lister.visit(child)
        classes = class_lister.classes_info

        function_lister = FuncLister()
        for child in ast.iter_child_nodes(self.module_node):
            if type(child) == ast.FunctionDef:
                function_lister.visit(child)
        functions = function_lister.functions_info

        info = ModuleInfo(name, docstrings, classes, functions)

        self._module_info = info


class ClassLister(ast.NodeVisitor):
    """Going through classes with NodeVisitor to get info"""

    def __init__(self):
        self._classes_info = []

    @property
    def classes_info(self):
        """Return classes_info list which save ClassInfo instances"""
        return self._classes_info

    def visit_ClassDef(self, node):
        """Visit class and append it to self.classes_info"""
        name = node.name
        docstrings = ast.get_docstring(node)

        func_lister = FuncLister()
        func_lister.visit(node)
        functions = func_lister.functions_info

        class_info = ClassInfo(name, docstrings, functions)

        self._classes_info.append(class_info)

    def visit_Assign(self, node):
        """
        Visit assignes that define
        namedtuples and add it to class_info.
        """
        if type(node.value) == ast.Call:
            if hasattr(node.value.func, 'id'):
                if node.value.func.id == 'namedtuple':
                    name = node.targets[0].id
                    args = node.value.args
                    call_name = args[0].s
                    call_args = args[1]
                    try:
                        if type(call_args) == ast.List:
                            call_args = ' '.join(ast.literal_eval(call_args))
                        else:
                            try:
                                call_args = args[1].s
                            except ValueError:
                                call_args = None
                        docstrings = '{}({})'.format(call_name,
                                                     ', '.join([a.replace(',', '') for a in call_args.split()]))
                    except AttributeError:
                        docstrings = None

                    namedtuple_info = ClassInfo(name, docstrings=docstrings, functions=None)

                    self._classes_info.append(namedtuple_info)


class FuncLister(ast.NodeVisitor):
    """Going through functions with NodeVisitor to get info"""

    def __init__(self):
        self._functions_info = []

    @property
    def functions_info(self):
        """Return functions_info list which save FuncInfo instances"""
        return self._functions_info

    @staticmethod
    def get_func_signature(func_node):
        if hasattr(func_node, 'args'):
            arg_lister = ArgLister()
            arg_lister.visit(func_node.args)
            signature = arg_lister.args
            return signature
        return []

    def visit_FunctionDef(self, node):
        """Visit function and append it to self.functions_info"""
        name = node.name
        docstrings = ast.get_docstring(node)
        signature = self.get_func_signature(node)
        func_info = FuncInfo(name, signature, docstrings)

        self._functions_info.append(func_info)


class ArgLister(ast.NodeVisitor):
    """Going through ast.arg class with NodeVisitor"""

    def __init__(self):
        self._args = []

    @property
    def args(self):
        """Args"""
        return self._args

    def visit_arg(self, node):
        """Visit the arg node"""
        self._args.append(node.arg)
