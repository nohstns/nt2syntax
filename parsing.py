import xml.etree.ElementTree as ET

def tree_to_brackets(tree:ET.Element):
    '''
    Converts a syntactic tree stored in a xml structure into bracket notation.
    Requires the argument tree to have been read as an etree Element Tree.

    Returns a single string with the tree transformed into bracket
    notation with curly brackets.

    Each node is labelled with the phrasal category as defined by Alpino unless
    it's a terminal node or leaf, in which case it is labelled with its dependency
    tag in relationship to its parent node.
    '''

    try:
        node = tree.getroot().findall('node')

    except AttributeError:
        node = tree

    n_nodes = len([node for node in tree.iter('node')])


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



    def _recursive_navigation(node, _descendants=None):

        if _descendants is None:
            _descendants = []

        else:
            if is_subtree(node):
                level = open_wrap(node)
                _descendants.append(level)


            if is_leaf(node):
                leaf = wrap(node.get('rel'))
                _descendants.append(leaf)

            
        for child in node:


            parent_begin, parent_end = get_span(node)
            child_begin, child_end = get_span(child)

            _recursive_navigation(child, _descendants)

            if parent_end == child_end:
                _descendants.append(close_wrap())


        return(_descendants)



    return ' '.join(_recursive_navigation(node))
