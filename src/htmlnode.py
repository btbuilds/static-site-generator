from typing import Optional

class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[list] = None, props: Optional[dict] = None):
        """Initialize an HTMLNode.

        Args:
            tag: (Optional) The HTML tag for this node (e.g., 'p', 'div', 'a'). Defaults to None.
            value: (Optional) The raw text content of this node if it's a text node (e.g., "Hello world"). Defaults to None.
            children: (Optional) A list of child HTMLNode instances. Defaults to None.
            props: (Optional) A dictionary of HTML attributes (e.g., {'href': 'https://example.com'}). Defaults to None.

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