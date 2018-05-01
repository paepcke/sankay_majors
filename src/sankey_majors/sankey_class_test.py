'''
Created on Apr 29, 2018

@author: paepcke
'''
from sankay_diagram import SankeyDiagram, SankeyLink, SankeyNode

if __name__ == '__main__':
    node_list = [
        SankeyNode(0, 'A1', 'blue'),
        SankeyNode(1, 'A2', 'blue'),
        SankeyNode(2, 'B1', 'blue'),
        SankeyNode(3, 'B2', 'blue'),
        SankeyNode(4, 'C1', 'blue'),
        SankeyNode(5, 'C2', 'blue')
        ]
    link_list = [
        SankeyLink(0,2,8),
        SankeyLink(1,3,4),
        SankeyLink(0,3,2),
        SankeyLink(2,4,8),
        SankeyLink(3,4,4),
        SankeyLink(3,5,2),
        ]
    
    SankeyDiagram.plot_sankey(node_list, 
                              link_list, 
                              'Basic Sankay Diagram'
                              )
    