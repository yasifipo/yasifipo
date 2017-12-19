

def node_dump(start, node, txt):
    for it in node.keys():
        if type(node[it]).__name__ == "str":
            if ' ' in node[it]:
                txt += start + it + ": \"" + node[it] + "\"\n"
            else:
                txt += start + it + ": " + node[it] + "\n"
        elif type(node[it]).__name__ == "int" or type(node[it]).__name__ ==  "float":
            txt += start + it + ": " + str(node[it]) + "\n"
        elif type(node[it]).__name__ == "bool":
            txt += start + it + ": " + str(node[it]) + "\n"
        elif type(node[it]).__name__ == "dict":
            txt += start + it + ":\n"
            txt = node_dump(start + '  ', node[it], txt)
        elif type(node[it]).__name__ == "list":
            txt += start + it + ":\n"
            for it_ in node[it]:
                for it__ in [it__ for it__ in it_ if it_[it__] is None]:
                    txt += start + "- " + it__ + ":\n"
                txt = node_dump(start + '  ', it_, txt)

    return txt


def yaml_dump(yaml):
    txt = node_dump('',yaml, "---\n")
    txt += "---\n"
    txt += "\n" + yaml.content + "\n"
    return txt
