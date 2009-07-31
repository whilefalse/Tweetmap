from django import template
import tweetmap.treemap

register = template.Library()

class TreemapNode(template.Node):
    def __init__(self,data, urls):
        self.var_name = data
        self.url_var_name = urls
    
    def render(self,context):
        data = context[self.var_name]
        urls = context[self.url_var_name]
        html = tweetmap.treemap.render_treemap(data,1024,768, urls=urls)
        return html 
        #return "I rendered a treemap tag with the variable: %s = %s" % (self.var_name,data)
    
def do_treemap(parser, token):
    try:
        tag_name, data, urls = token.split_contents()
    except ValueError:
        msg = "%r tag requires a single dictionary argument" % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return TreemapNode(data, urls)

register.tag('treemap', do_treemap)