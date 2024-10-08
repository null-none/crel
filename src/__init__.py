from html import escape
from types import GeneratorType
from typing import (
    Tuple,
    Union,
    Dict,
    List,
    FrozenSet,
    Generator,
    Iterable,
    Any,
    Callable,
)


class SafeString:
    __slots__ = ("safe_str",)

    def __init__(self, safe_str: str) -> None:
        self.safe_str = safe_str

    def __hash__(self) -> int:
        return hash(f"SafeString__{self.safe_str}")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SafeString) and other.safe_str == self.safe_str

    def __repr__(self) -> str:
        return f"SafeString(safe_str='{self.safe_str}')"


Node = Union[
    str,
    SafeString,
    "Tag",
    "TagTuple",
    List["Node"],
    Generator["Node", None, None],
]

TagTuple = Tuple[str, Tuple[Node, ...], str]

_common_safe_attribute_names: FrozenSet[str] = frozenset(
    {
        "alt",
        "autoplay",
        "autoplay",
        "charset",
        "checked",
        "class",
        "colspan",
        "content",
        "contenteditable",
        "d",
        "data-index",
        "data-format",
        "dir",
        "disabled",
        "draggable",
        "enctype",
        "for",
        "fill",
        "height",
        "hidden",
        "href",
        "hreflang",
        "http-equiv",
        "id",
        "itemprop",
        "itemscope",
        "itemtype",
        "label",
        "lang",
        "loadable",
        "method",
        "name",
        "onblur",
        "onclick",
        "onfocus",
        "onkeydown",
        "onkeyup",
        "onload",
        "onselect",
        "onsubmit",
        "placeholder",
        "poster",
        "property",
        "rel",
        "required",
        "rowspan",
        "selected",
        "sizes",
        "spellcheck",
        "src",
        "style",
        "target",
        "title",
        "type",
        "value",
        "viewBox",
        "width",
        "xmlns"
    }
)


class Tag:
    __slots__ = (
        "tag_start",
        "closing_tag",
        "tag_start_no_attrs",
        "rendered",
        "no_children_close",
    )

    def escape_attribute_key(self, k: str) -> str:
        return (
            escape(k, True)
            .replace("=", "&#x3D;")
            .replace("\\", "&#x5C;")
            .replace("`", "&#x60;")
            .replace(" ", "&nbsp;")
        )

    def __init__(self, name: str, self_closing: bool = False) -> None:
        self.tag_start = f"<{name}"
        self.tag_start_no_attrs = f"{self.tag_start}>"
        self.closing_tag = f"</{name}>"
        if self_closing:
            self.no_children_close = "/>"
        else:
            self.no_children_close = f">{self.closing_tag}"
        self.rendered = f"{self.tag_start}{self.no_children_close}"

    def __call__(
        self,
        attributes: Dict[Union[SafeString, str], Union[str, SafeString, None]],
        *children: Node,
    ) -> Union[TagTuple, SafeString]:
        if attributes:
            # in this case this is faster than attrs = "".join([...])
            attrs = ""
            for key, val in attributes.items():
                # optimization: a large portion of attribute keys should be
                # covered by this check. It allows us to skip escaping
                # where it is not needed. Note this is for attribute names only;
                # attributes values are always escaped (when they are `str`s)
                if key not in _common_safe_attribute_names:
                    key = (
                        self.scape_attribute_key(key)
                        if isinstance(key, str)
                        else key.safe_str
                    )

                if isinstance(val, str):
                    attrs += f' {key}="{escape(val, True)}"'
                elif isinstance(val, SafeString):
                    attrs += f' {key}="{val.safe_str}"'
                elif val is None:
                    attrs += f" {key}"

            if children:
                return f"{self.tag_start}{attrs}>", children, self.closing_tag
            else:
                return SafeString(f"{self.tag_start}{attrs}{self.no_children_close}")
        elif children:
            return self.tag_start_no_attrs, children, self.closing_tag
        else:
            return SafeString(self.rendered)


DOCTYPE_HTML5 = SafeString("<!doctype html>")

a = Tag("a")
abbr = Tag("abbr")
address = Tag("address")
area = Tag("area", True)
article = Tag("article")
aside = Tag("aside")
audio = Tag("audio")
b = Tag("b")
base = Tag("base", True)
bdi = Tag("bdi")
bdo = Tag("bdo")
blockquote = Tag("blockquote")
body = Tag("body")
br = Tag("br", True)
button = Tag("button")
canvas = Tag("canvas")
center = Tag("center")
caption = Tag("caption")
cite = Tag("cite")
code = Tag("code")
col = Tag("col")
colgroup = Tag("colgroup")
datalist = Tag("datalist")
dd = Tag("dd")
details = Tag("details")
del_ = Tag("del")
dfn = Tag("dfn")
div = Tag("div")
dl = Tag("dl")
dt = Tag("dt")
em = Tag("em")
embed = Tag("embed", True)
fieldset = Tag("fieldset")
figure = Tag("figure")
figcaption = Tag("figcaption")
footer = Tag("footer")
font = Tag("font")
form = Tag("form")
head = Tag("head")
header = Tag("header")
h1 = Tag("h1")
h2 = Tag("h2")
h3 = Tag("h3")
h4 = Tag("h4")
h5 = Tag("h5")
h6 = Tag("h6")
hr = Tag("hr", True)
html = Tag("html")
i = Tag("i")
iframe = Tag("iframe", True)
img = Tag("img", True)
inp = Tag("input", True)
ins = Tag("ins")
kbd = Tag("kbd")
label = Tag("label")
legend = Tag("legend")
li = Tag("li")
link = Tag("link", True)
main = Tag("main")
mark = Tag("mark")
marquee = Tag("marquee")
math = Tag("math")
menu = Tag("menu")
menuitem = Tag("menuitem")
meta = Tag("meta", True)
meter = Tag("meter")
nav = Tag("nav")
object_ = Tag("object")
noscript = Tag("noscript")
ol = Tag("ol")
optgroup = Tag("optgroup")
option = Tag("option")
p = Tag("p")
path = Tag("path")
param = Tag("param", True)
picture = Tag("picture")
pre = Tag("pre")
progress = Tag("progress")
q = Tag("q")
rp = Tag("rp")
rt = Tag("rt")
ruby = Tag("ruby")
s = Tag("s")
samp = Tag("samp")
script = Tag("script")
section = Tag("section")
select = Tag("select")
small = Tag("small")
source = Tag("source", True)
span = Tag("span")
strike = Tag("strike")
strong = Tag("strong")
style = Tag("style")
sub = Tag("sub")
summary = Tag("summary")
sup = Tag("sup")
svg = Tag("svg")
table = Tag("table")
tbody = Tag("tbody")
template = Tag("template")
textarea = Tag("textarea")
td = Tag("td")
th = Tag("th")
thead = Tag("thead")
time = Tag("time")
title = Tag("title")
tr = Tag("tr")
track = Tag("track", True)
u = Tag("u")
ul = Tag("ul")
var = Tag("var")
video = Tag("video")
wbr = Tag("wbr")


def _render(nodes: Iterable[Node], append_to_list: Callable[[str], None]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    for node in nodes:
        if type(node) is tuple:
            append_to_list(node[0])
            _render(node[1], append_to_list)
            append_to_list(node[2])
        elif isinstance(node, SafeString):
            append_to_list(node.safe_str)
        elif isinstance(node, str):
            append_to_list(escape(node))
        elif isinstance(node, Tag):
            append_to_list(node.rendered)
        elif isinstance(node, list):
            _render(node, append_to_list)
        elif isinstance(node, GeneratorType):
            _render(node, append_to_list)
        else:
            raise TypeError(f"Got unknown type: {type(node)}")


def render(*nodes: Node) -> str:
    results: List[str] = []
    _render(nodes, results.append)

    return "".join(results)
