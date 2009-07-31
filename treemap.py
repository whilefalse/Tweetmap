"""
treemappy 0.9
jose nazario <jose@monkey.org>
1 december 2006

from the original PHP code, i'll keep the license the same:
This is provided AS-IS with no warranty express or implied.
Use this code, or any code that I write, at your own risk.
"""

from random import random

def ksort(d):
    if isinstance(d, dict): items = d.items()
    else: items = d
    items = [(v, k) for (k, v) in items]
    items.sort()
    items.reverse()        # so largest is first
    items = [(k, v) for (v, k) in items]
    return items

# "port" of PHPs array_chunk(), modified to sort the dict by values
def dict_chunk(D, size):
    D = ksort(D)
    keys = [ x[0] for x in D ]
    num_keys = len(keys)
    res = []
    X = []
    for i in xrange(0, num_keys):
        val = D[i]
        X.append(val)
        if len(X) == size: 
            res.append(X)
            X = []
    return res

# basically a straight port from the PHP of 
# http://www.neurofuzzy.net/2006/04/28/treemap-php-source-code/
def render_treemap(D, width, height, depth = 0, orientation = 0, urls=None):
    import math
    
    if depth == 0:
        html = '<div class="treemap" style="width: %dpx; height: %dpx;">' % (width, height)
    else: html = ''
    
    if len(D) > 1:
        split_D = dict_chunk(D, math.ceil(len(D)/ 2))
        
        a = split_D[0]
        b = split_D[1]
        
        if isinstance(D, dict):
            apercent = float(sum([ x[1] for x in a]))/sum(D.values()) 
        else: 
            apercent = float(sum([ x[1] for x in a]))/sum([ x[1] for x in D])
        bpercent = 1 - apercent
        
        if depth % 2 == orientation:
            awidth = math.ceil(width * apercent)
            bwidth = width - awidth
            
            aheight = height
            bheight = height
        else:
            aheight = math.ceil(height * apercent)
            bheight = height - aheight
            
            awidth = width
            bwidth = width
        
        rand_col_a = 'rgb('+str(int(random()*256))+','+str(int(random()*256))+','+str(int(random()*256))+')'
        rand_col_b = 'rgb('+str(int(random()*256))+','+str(int(random()*256))+','+str(int(random()*256))+')'        
        astyle = 'width: %dpx; height: %dpx; background-color:%s;' % (awidth, aheight,rand_col_a)
        bstyle = 'width: %dpx; height: %dpx; background-color:%s;' % (bwidth, bheight, rand_col_b)
    
        # recurse on a
        html += '\n<div class="node" style="%s">' % astyle
        html += render_treemap(a, awidth, aheight, depth + 1, urls=urls)
        html += '\n</div>'
        
        # recurse on b
        html += '\n<div class="node" style="%s">' % bstyle
        html += render_treemap(b, bwidth, bheight, depth + 1, urls=urls)
        html += '\n</div>'
    
    else:
        # make cell
        if isinstance(D, dict): tags = D.keys()
        else: tags = [ x[0] for x in D ]
        for tag in tags:
            urltag = tag.strip().lower()
            if urltag.startswith('-'): classtext = 'proper'
            else: classtext = ''
            styletext = ''
            textsize = max(10, math.floor((width - 16)/ max(8, len(tag))))
            textsize = max(10, min(textsize, height - 8))
            styletext = 'style=" font-size: %dpx; %s"' % (textsize, styletext)
            
            html += '\n<a class="textnode%s" %s href="%s" title="view data for %s"><img src="/media/img/treemap/spacer.gif" height="100%%" width="1" border="0" alt="" />%s</a>' % (classtext, styletext, urls[tag], tag, tag)

    if depth == 0:
        html += "\n</div>"
    
    return html

if __name__ == '__main__':
    # an example input dict
    D = {'RPC': 7618, 'FOO': 9181, 'BAR': 3293, 'BAZ': 981, 
         'a': 971, 'b': 873, 'c': 991, 'd': 300, 'e': 7}
    
    print """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <title>Treemap Example</title>
    <link href="css/styles.css" rel="stylesheet" type="text/css">
    </head>

    <body>
    <div align="center" style="width: 720px; margin: auto;">
    """
    print render_treemap(D, 720, 360)
    
    print """</div>
    </body>
    </html>"""
