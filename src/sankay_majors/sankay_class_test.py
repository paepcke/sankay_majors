'''
Created on Apr 29, 2018

@author: paepcke
'''
from sankay_diagram import SankayDiagram, SankayLink, SankayNode

if __name__ == '__main__':
    node_list = [
        SankayNode(0, 'A1', 'blue'),
        SankayNode(1, 'A2', 'blue'),
        SankayNode(2, 'B1', 'blue'),
        SankayNode(3, 'B2', 'blue'),
        SankayNode(4, 'C1', 'blue'),
        SankayNode(5, 'C2', 'blue')
        ]
    link_list = [
        SankayLink(0,2,8),
        SankayLink(1,3,4),
        SankayLink(0,3,2),
        SankayLink(2,4,8),
        SankayLink(3,4,4),
        SankayLink(3,5,2),
        ]
    
    SankayDiagram.plot_sankay(node_list, 
                              link_list, 
                              'Basic Sankay Diagram'
                              )
    