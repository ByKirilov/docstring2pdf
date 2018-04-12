"""
Module for representing object's docstrings as pdf-code
"""

import astlister
import pdfformater

CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT


class PDF_Doc_Repr:
    """Representation of object's docstrings as pdf-code"""

    @staticmethod
    def make_pdf(pdf):
        """Wrap the base pdf-code in the tags for final use"""
        return pdfformater.to_page(pdf)

    @staticmethod
    def _members_to_pdf(members, pdf):
        global CURRENT_SHIFT
        for member in members:
            if _is_private_name(member.name):
                continue
            if isinstance(member, astlister.ClassInfo):
                pdf += pdfformater.to_subhead(member.name, CURRENT_SHIFT)
                CURRENT_SHIFT = 2 * pdfformater.HORIZONTAL_SHIFT
            if isinstance(member, astlister.FuncInfo):
                signature = '(' + ', '.join(member.signature) + ')'
                pdf += pdfformater.to_subhead(member.name + signature, CURRENT_SHIFT)
                CURRENT_SHIFT = 2 * pdfformater.HORIZONTAL_SHIFT
            docs = member.docstrings
            if docs:
                pdf += pdfformater.to_text(docs, CURRENT_SHIFT)
                CURRENT_SHIFT += pdfformater.HORIZONTAL_SHIFT
        return pdf

    def function_to_pdf(self, fnc_info, cls_name, mod_name):
        """PDF-representation of functions' docstrings"""
        global CURRENT_SHIFT

        fnc_name = fnc_info.name
        cls_name = cls_name
        mod_name = mod_name

        pdf = ''

        signature = '(' + ', '.join(fnc_info.signature) + ')'
        pdf += pdfformater.to_head(fnc_name + signature, CURRENT_SHIFT)
        CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT

        description = fnc_info.docstrings
        if description:
            pdf += pdfformater.to_text(description, CURRENT_SHIFT)
            CURRENT_SHIFT += pdfformater.HORIZONTAL_SHIFT

        pdf = pdfformater.to_page_description('Docstrings to {} method{}of {} module'
                                              .format(fnc_name, ' of {} class '
                                                      .format(cls_name) if cls_name is not None else ' ',
                                                      mod_name), pdfformater.get_page_height(pdf)) + pdf

        return self.make_pdf(pdf)

    def class_to_pdf(self, class_info, module_name):
        """PDF-representation of class' docstrings"""
        global CURRENT_SHIFT

        cls_name = class_info.name
        mod_name = module_name
        description = class_info.docstrings
        functions = class_info.functions

        if _is_all_private(functions):
            functions = None

        pdf = ''
        pdf += pdfformater.to_head('class {}'.format(cls_name), CURRENT_SHIFT)
        CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT

        if description:
            pdf += pdfformater.to_text(description, CURRENT_SHIFT)
            CURRENT_SHIFT += pdfformater.HORIZONTAL_SHIFT

        if functions:
            pdf += pdfformater.to_subhead('METHODS:', CURRENT_SHIFT)
            CURRENT_SHIFT = 2 * pdfformater.HORIZONTAL_SHIFT
            pdf = self._members_to_pdf(functions, pdf)

        pdf = pdfformater.to_page_description('Docstrings to {} class of {} module'
                                              .format(cls_name, mod_name), pdfformater.get_page_height(pdf)) + pdf

        return self.make_pdf(pdf)

    def module_to_pdf(self, module_info):
        """PDF-representation of module's docstrings"""
        global CURRENT_SHIFT

        mod_name = module_info.name
        description = module_info.docstrings
        classes = module_info.classes
        functions = module_info.functions

        if _is_all_private(functions):
            functions = None

        pdf = ''
        pdf += pdfformater.to_head('NAME', CURRENT_SHIFT)
        CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT
        pdf += pdfformater.to_subhead(mod_name, CURRENT_SHIFT)
        CURRENT_SHIFT = 2 * pdfformater.HORIZONTAL_SHIFT

        if description:
            pdf += pdfformater.to_head('DESCRIPTION', CURRENT_SHIFT)
            CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT
            pdf += pdfformater.to_text(description, CURRENT_SHIFT)
            CURRENT_SHIFT += pdfformater.HORIZONTAL_SHIFT

        if classes:
            pdf += pdfformater.to_head('CLASSES', CURRENT_SHIFT)
            CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT
            pdf = self._members_to_pdf(classes, pdf)

        if functions:
            pdf += pdfformater.to_head('FUNCTIONS', CURRENT_SHIFT)
            CURRENT_SHIFT = pdfformater.HORIZONTAL_SHIFT
            pdf = self._members_to_pdf(functions, pdf)

        pdf = pdfformater.to_page_description('Docstrings to {} module'.format(mod_name),
                                              pdfformater.get_page_height(pdf)) + pdf

        return self.make_pdf(pdf)


def _is_private_name(name):
    if name in ['__author__', '__builtins__', '__cached__', '__credits__',
                '__date__', '__doc__', '__file__', '__spec__',
                '__loader__', '__module__', '__name__', '__package__',
                '__path__', '__qualname__', '__slots__', '__version__']:
        return True
    if name.startswith('__') and name.endswith('__'):
        return False
    return name.startswith('_')


def _is_all_private(functions):
    if functions is None:
        return True
    private_count = sum(list(map(_is_private_name, [func.name for func in functions])))
    return private_count == len(functions)
