'''
Created on Apr 29, 2018

@author: paepcke
'''
import os

from sankay_diagram import SankeyDiagram


if __name__ == '__main__':
    
    curr_dir = os.path.dirname(__file__)
    with open(os.path.join(curr_dir, 'data/energy.json'), 'r') as energy_flow_fd:
        (node_list, link_list) = SankeyDiagram.import_sankey_json(energy_flow_fd)
    
    SankeyDiagram.plot_sankey(node_list, 
                              link_list, 
                              'Energy Flow'
                              )
    