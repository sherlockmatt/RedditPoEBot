from bs4 import BeautifulSoup, NavigableString

# styles = {
#     "-mod": "#%s",
#     "-value": "**%s**",
#     "-flavour": "*%s*"
# }

hide_string = "#####&#009;\n\n######&#009;\n\n####&#009;\n\n%s\n\n***\n\n"

def parse_item(page):
    soup = BeautifulSoup(page)
    # Find div with class item-box. Only unique items so far..
    itembox = soup.find("div", { "class": "item-box" })
    if not itembox or "-unique" not in itembox["class"]: return ""
    header = itembox.find("span", { "class": "header" })
    unique_name = header.children.next().text
    base_item = header.find("a").text
    
    unparsed_groups = itembox.find("span", { "class": "item-stats" }).find_all("span", { "class": "group" })
    
    groups = []
    for group in unparsed_groups:
        lines = []
        line = ""
        for child in group.children:
            if unicode(child) == '<br/>':
                lines.append(line)
                line = ""
            else: 
                line += format_text(child)
        if line is not "":
            lines.append(line)
        groups.append(lines)
    item_string = make_string(unique_name, base_item, groups)
    #return (hide_string % unique_name) + item_string + "\n\n" #Add hiding.. Shows "GGG forum post. Hover to view.".
    return item_string

def format_text(child):
    if not type(child) == NavigableString and "-value" in child["class"]:
        #if type(child.next) == NavigableString:
            return "**%s**" % child.string
        #elif "-mod" in child.next["class"]:
            #return "#%s" % child.string
    elif "-mod" in child.parent["class"]: 
        return "#%s" % child.string
    elif "-flavour" in child.parent["class"]: 
        return "*%s*" % child.string
    else:
        return child.string

def make_string(name, base, groups):
    s = ">######%s[](#break)%s\n" % (name, base)
    #s = ">######[%s](%s)[](#break)%s\n" % (name, link, base) #also include link in the header..
    for group in groups:
        for line in group:
            s += ">>%s%s\n" % ("" if line.startswith("*") else "####", line)
        s += ">>[](#line)\n"
    if len(groups) > 0:
        s = s[:-13]
    return s

# parse_item(open("C:\urltext.txt", "r").read())