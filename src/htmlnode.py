from typing import Optional

class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[list] = None, props: Optional[dict] = None):
        """Initialize an HTMLNode.

        Args:
            tag: (Optional[str]) The HTML tag for this node (e.g., 'p', 'div', 'a'). Defaults to None.
            value: (Optional[str]) The raw text content of this node if it's a text node (e.g., "Hello world"). Defaults to None.
            children: (Optional[list]) A list of child HTMLNode instances. Defaults to None.
            props: (Optional[dict]) A dictionary of HTML attributes (e.g., {'href': 'https://example.com'}). Defaults to None.

        Example:
            node = HTMLNode("a", "Click here", props={"href": "https://example.com"})
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    
    def to_html(self):
        raise NotImplementedError("Not implemented yet")
    
    def props_to_html(self):
        if not self.props:
            return ""
        all_props = ""
        for key, value in self.props.items():
            all_props += f' {key}="{value}"'
        return all_props


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value, props: Optional[dict] = None):
        """
        Represents an HTML node that cannot have child nodes (a "leaf" node in the DOM tree).

        This class inherits from HTMLNode and is used for elements that contain only text
        and attributes but no children.

        Args:
            tag (Optional[str]): The HTML tag for this node (e.g., 'p', 'div', 'a'). Use None for plain text nodes.
            value (str): The raw text content of this node if it's a text node (e.g., "Hello world").
            props (Optional[dict]): Optional dictionary of HTML attributes (e.g., {'href': 'https://example.com'}).

        Example:
            ```python
            node = LeafNode("a", "Click me", {"href": "https://example.com"})
            node.to_html()  # returns: '<a href="https://example.com">Click me</a>'
            ```
        """
        super().__init__(tag, value, props=props)
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if not self.value:
            raise ValueError("No value given - leaf nodes must have a value")
        if not self.tag:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: Optional[dict] = None):
        """
        Represents an HTML node that can have child nodes.

        Args:
            tag (str): The HTML tag for this node (e.g., 'p', 'div', 'a').
            children (list): A list of HTMLNode objects to nest inside.
            props (Optional[dict]): Optional dictionary of HTML attributes (e.g., {'href': 'https://example.com'}).

        Example:
            ```python
            child1 = LeafNode("li", "Item 1")
            child2 = LeafNode("li", "Item 2")
            parent = ParentNode("ul", [child1, child2])
            parent.to_html()  # returns: '<ul><li>Item 1</li><li>Item 2</li></ul>'
            ```
        """

        super().__init__(tag, children=children, props=props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
    def to_html(self):
        if not self.tag:
            raise ValueError("No tag given - parent nodes must have a tag")
        if not self.children:
            raise ValueError("No children given - parent nodes must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"