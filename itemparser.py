from bs4 import BeautifulSoup, NavigableString

# styles = {
#     "-mod": "#%s",
#     "-value": "**%s**",
#     "-flavour": "*%s*",
#     "-corrupted": "%s"
# }

hide_string = "#####&#009;\n\n######&#009;\n\n####&#009;\n\n%s\n\n***\n\n"


# <span class="item-box -unique">
#   <span class="header -double">Sire of Shards<br>Serpentine Staff</span>
#   <span class="item-stats">
#     <span class="group">
#       <em class="tc -default">Staves</em><br>
#       <em class="tc -default">Physical Damage: </em><em class="tc -value"><em class="tc -value">46</em>&ndash;<em class="tc -value">95</em></em><br>
#       <em class="tc -default">Critical Strike Chance: </em><em class="tc -value"><em class="tc -value">6.40%</em></em><br>
#       <em class="tc -default">Attacks per Second: </em><em class="tc -value"><em class="tc -value">1.20</em></em>
#     </span>
#     <span class="group">
#       <em class="tc -default">Requires </em><em class="tc -default">Level </em><em class="tc -value">49</em><em class="tc -default">, </em><em class="tc -value"><em class="tc -value">85</em></em><em class="tc -default"> Str</em><em class="tc -default">, </em><em class="tc -value"><em class="tc -value">85</em></em><em class="tc -default"> Int</em>
#     </span>
#     <span class="group tc -mod">18% Chance to [[Block]]</span>
#     <span class="group tc -mod">+(15-20) to all Attributes<br>
#       +(5-7)% to all [[Elemental Resistance|Elemental Resistances]]<br>
#       (60-100)% increased Projectile Damage<br>
#       20% increased Light Radius<br>
#       [[Item socket|Socketed]] Gems fire 4 additional Projectiles<br>
#       [[Item socket|Socketed]] Gems fire Projectiles in a Nova</span>
#     <span class="group -textwrap tc -flavour">That which was broken may yet break.</span>
#   </span>
# </span>

def parse_item2(panel):
    soup = BeautifulSoup(panel, "html.parser")
    # Find div with class item-box. Only unique items so far..
    itembox = soup.find("span", { "class": "item-box" })
    if not itembox or "-unique" not in itembox["class"]: return ""
    header = itembox.find("span", { "class": "header" })
    unique_name = str(header.children.next())
    base_item = header.children.next().next.text
    
    unparsed_groups = itembox.find("span", { "class": "item-stats" }).find_all("span", { "class": "group" })
    
    groups = []
    for group in unparsed_groups:
        lines = []
        line = ""
        for child in group.children:
            if not unicode(child).strip():
                continue #Ignore whitespace lines.
            elif unicode(child) == '<br/>':
                lines.append(line)
                line = ""
            else: 
                line += format_text(child) or ""
        if line is not "":
            lines.append(line)
        groups.append(lines)
    item_string = make_string(unique_name, base_item, groups)
    #return (hide_string % unique_name) + item_string + "\n\n" #Add hiding.. Shows "GGG forum post. Hover to view.".
    return item_string + "\n\n"


def parse_item(page):
    soup = BeautifulSoup(page, "html.parser")
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
            if not unicode(child).strip():
                continue #Ignore whitespace lines.
            elif unicode(child) == '<br/>':
                lines.append(line)
                line = ""
            else: 
                line += format_text(child) or ""
        if line is not "":
            lines.append(line)
        groups.append(lines)
    item_string = make_string(unique_name, base_item, groups)
    #return (hide_string % unique_name) + item_string + "\n\n" #Add hiding.. Shows "GGG forum post. Hover to view.".
    return item_string + "\n\n"

def format_text(child):
    if type(child) == NavigableString:
        classes = child.parent["class"]
    else:
        classes = child["class"]

    if "-value" in classes:
        return "**%s**" % child.string
    elif "-corrupted" in classes:
        return child.string
    elif "-fire" in classes:
        return child.string #Should be red, but not possible.
    elif "-cold" in classes:
        return child.string #Should be blue, but not possible.
    elif "-lightning" in classes:
        return child.string #Should be yellow, but not possible.
    elif "-mod" in classes: 
        return "#%s" % child.string
    elif "-flavour" in classes: 
        return "*%s*\n>>" % child.string.strip()
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