'''
Created on Apr 29, 2018

@author: paepcke
'''
import json

import plotly

class SankeyDiagram(object):
    
    # ======================================= Public Methods =========================    
    
    #--------------------------
    # plot_sankey 
    #-------------------
    
    @classmethod
    def plot_sankey(cls,
                    node_list,
                    link_list,
                    plot_title="Sankey Diagram",
                    font=10):
        
        fig = SankeyDiagram.construct_plotly_struct(node_list, 
                                                    link_list, 
                                                    plot_title, 
                                                    font)
        plotly.offline.plot(fig, validate=False) 
    
    
    #--------------------------
    # import_sankey_json 
    #-------------------
        
    @classmethod
    def import_sankey_json(cls, fileObjOrJsonStr):
        
        # Is it a file-like object?
        try:
            json_str = fileObjOrJsonStr.read()
        except AttributeError:
            json_str = fileObjOrJsonStr
        
        try:
            sankey_info = json.loads(json_str)
        except ValueError:
            raise('Given JSON string cannot be parsed.')
        
        try:
            sankey_data = sankey_info['data'][0]
        except IndexError:
            raise("The 'data' key's value from the JSON is not an array as excpected.")
        
        
        # Construct node list:
        node_labels = sankey_data['node']['label']
        node_colors = sankey_data['node']['color']
        node_nums   = range(len(node_labels))
        nodes = [ SankeyNode(node_info[0],
                             node_info[1],
                             node_info[2]
                             ) 
                             for node_info in zip(node_nums, node_labels, node_colors) 
                             ]

        link_sources = sankey_data['link']['source']
        link_targets = sankey_data['link']['target']
        link_values  = sankey_data['link']['value']      
        
        links = [ SankeyLink(link_info[0],
                             link_info[1],
                             link_info[2]
                             ) 
                             for link_info in zip(link_sources, link_targets, link_values) 
                             ]
        
        return(nodes, links)    

    
    # ======================================= Private Methods =========================
        
    #--------------------------
    # construct_plotly_struct 
    #-------------------
    
    @classmethod
    def construct_plotly_struct(cls, 
                                node_list,
                                link_list,
                                plot_title="Sankey Diagram",
                                font=10,
                                orientation="h",
                                #****valueformat=".0f",
                                valueformat="d",
                                valuesuffix=""
                                ):
        
        node_colors  = [ node.color for node in node_list ]
        node_labels  = [ node.label for node in node_list ]
        
        link_sources = [ link.src_node_num for link in link_list ] 
        link_targets = [ link.target_node_num for link in link_list ]
        link_values  = [ link.weight for link in link_list ]
        
        layout =  dict(
            title = plot_title,
            font = dict(
              size = font
            )
        )
        
        plotly_data = dict(
            type = 'sankey',
            orientation = orientation,
            valueformat = valueformat,
            valuesuffix = valuesuffix,
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
        
        return dict(
            data=[plotly_data], 
            layout=layout
            )


# --------------------------- Node Class ----------------

class SankeyNode(object):
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
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.num == other.num and \
                   self.label == other.label and \
                   self.color == other.color
        else:
            return False
        
    def __ne__(self, other):
        return (not isinstance(other, self.__class__) or \
                self.num != other.num or \
                self.label != other.label or \
                self.color != other.color
                )

# --------------------------- Link Class ----------------
        
class SankeyLink(object):
    
    def __init__(self, src_node_num, target_node_num, weight):
        
        self.src_node_num = src_node_num
        self.target_node_num = target_node_num
        self.weight = weight

# --------------------------- Node Style Class ----------------
        
class NodeStyle(object):
    
        pad = 15
        thickness = 20
        popup_line_color = 'black'
        popup_line_thickness = 0.5
        