#!/usr/bin/env python3
import xml.etree.ElementTree as ET

def tree_to_brackets(tree:ET.Element):

    try:
        node = tree.getroot().findall('node')

    except AttributeError:
        node = tree


    def get_degree(node):
        degree = len(node)
        return degree

    def is_internal(node):
        if get_degree(node) >= 1:
            return True
        else:
            return False

    def is_leaf(node):
        if is_internal(node) == False:
            return True
        else:
            return False

    def is_subtree(node):
        if node.get('cat')is not None:
            return True
        else:
            return False

    def wrap(leaf):
        wrapped = str('{' + leaf + '}')
        return wrapped

    def open_wrap(node):
        bracket = '{'
        name = node.get('cat')
        if name.startswith('mwu'):
            name = 'mwu'
        return str(bracket + name)

    def close_wrap():
        bracket = '}'
        return bracket

    def get_span(node):
        if isinstance(node, ET.Element):
            begin = node.get('begin')
            end = node.get('end')

        else:
            begin = None
            end = None

        return begin, end


    to_close = []

    def _recursive_navigation(node, _descendants=None):

        if _descendants is None:
            _descendants = []

        else:
            if is_subtree(node):
                level = open_wrap(node)
                _descendants.append(level)
                to_close.append('')


            if is_leaf(node):

                leaf = wrap(node.get('rel')) # To change to rel when function is finished
                _descendants.append(leaf)


        for child in node:


            parent_begin, parent_end = get_span(node)
            child_begin, child_end = get_span(child)

            _recursive_navigation(child, _descendants)

            if parent_end == child_end:
                try:
                    to_close.pop()
                    _descendants.append(close_wrap())
                except IndexError:
                    print('Nothing to close')


        return(_descendants)



    return ''.join(_recursive_navigation(node))
