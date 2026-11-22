class HTMLNode:
    def __init__(self, tag = None, value= None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not Implemented")

    def props_to_html(self):
        props = ''
        if self.props:
            for key,value in self.props.items():
                props += f' {key}="{value}"'
            return props
        return ""

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None ,props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf nodes must have values")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("unvalid tag")
        if not self.children:
            raise ValueError("does not have children")
        acc_children = ''
        for child in self.children:
            acc_children += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{acc_children}</{self.tag}>"