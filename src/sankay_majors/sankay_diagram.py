'''
Created on Apr 29, 2018

@author: paepcke
'''
import plotly


class SankayDiagram(object):
    
    @classmethod
    def plot_sankay(cls,
                    node_list,
                    link_list,
                    plot_title="Sankey Diagram",
                    font=10):
        
        fig = SankayDiagram.construct_plotly_struct(node_list, 
                                                    link_list, 
                                                    plot_title, 
                                                    font)
        plotly.offline.plot(fig, validate=False) 
    
    @classmethod
    def construct_plotly_struct(cls, 
                                node_list,
                                link_list,
                                plot_title="Sankey Diagram",
                                font=10):
        
        node_colors  = [ node.color for node in node_list ]
        node_labels  = [ node.label for node in node_list ]
        
        link_sources = [ link.src_node_num for link in link_list ] 
        link_targets = [ link.target_node_num for link in link_list ]
        link_values  = [ link.weight for link in link_list ]
        
        plotly_struct = dict(
            type = 'sankey',
            node = dict(
                pad = NodeStyle.pad,
                thickness = NodeStyle.thickness,
                line = dict(
                    color = NodeStyle.popup_line_color,
                    width = NodeStyle.popup_line_thickness
                ),
                label = node_labels,
                color = node_colors
            ),
            link = dict(
                source = link_sources,
                target = link_targets,
                value  = link_values
                )
        )
        
        layout =  dict(
            title = plot_title,
            font = dict(
              size = font
            )
        )
        
        return dict(
            data=[plotly_struct], 
            layout=layout
            )   

class SankayNode(object):
    '''
    classdocs
    '''

    def __init__(self, node_num, node_label, node_color):
        '''
        Constructor
        '''
        self.num = node_num
        self.label = node_label
        self.color = node_color
        
class SankayLink(object):
    
    def __init__(self, src_node_num, target_node_num, weight):
        
        self.src_node_num = src_node_num
        self.target_node_num = target_node_num
        self.weight = weight
        
class NodeStyle(object):
    
        pad = 15
        thickness = 20
        popup_line_color = 'black'
        popup_line_thickness = 0.5
        