import argparse
import getpass
import os

from pymysql_utils.pymysql_utils import MySQLDB
from sankey_diagram import SankeyNode, SankeyLink, SankeyDiagram
from color_generator import ColorSource

class SankeyMajors(object):
    
    # Minimum number of students to have made the transitions 
    # between two particular majors to be included in the 
    # diagram. For undergrad majors only:
    #    
    #    > 5: 505 pairs
    #    >10: 249 pairs
    #    >20: 101 pairs
    #    >50:  41 pairs
    #    >99:   8 pairs
     
    MIN_MAJOR_TRANSITIONS = 10
    
    #--------------------------
    # __init__
    #-------------------

    
    def __init__(self,
                 majors_table='sankey'
                 ):
        '''
        '''

        self.majors_table = majors_table
        self.mysql_passwd = self.getMySQLPasswd()
        self.mysql_dbhost ='localhost'
        self.mysql_user = getpass.getuser() # mySQLUser that started this process
        self.mydb = MySQLDB(user=self.mysql_user, 
                            passwd=self.mysql_passwd, 
                            db=self.majors_table)
        
        (nodes, links) = self.get_nodes_and_links()
        SankeyDiagram.plot_sankey(nodes, 
                                  links, 
                                  plot_title="Majors Transitions")
        
    #--------------------------
    # get_nodes_and_links 
    #-------------------
    
    def get_nodes_and_links(self):
    
        query = '''SELECT major_left_num, major_right_num, count(*) AS num_transitions
                     FROM majors_transitions
                     GROUP BY major_left_num, major_right_num
                     HAVING num_transitions > %s
                ''' % SankeyMajors.MIN_MAJOR_TRANSITIONS 
                
        MAJOR_LEFT_NUM = 0
        MAJOR_RIGHT_NUM = 1
        NUM_TRANSITIONS = 2
        
        link_info = self.mydb.query(query).nextall()
        
        # The int coercions below prevent nums to be treated
        # like LONG, and have subsequent displays of the numbers
        # have an 'L' suffix:
        
        links = [ SankeyLink(int(one_link_info[MAJOR_LEFT_NUM]),
                             int(one_link_info[MAJOR_RIGHT_NUM]),
                             int(one_link_info[NUM_TRANSITIONS])
                             )
                             for one_link_info in link_info
                 ]
        
        nodes = self.get_nodes(links)
        
        # Now we need to change the source and target node numbers
        # in the SankeyLink objects to be indexes into the just
        # obtained list of SankeyNodes instances. Right now those
        # source/target numbers are the absolute majors numbers
        # in the db:
        
        for sankey_link_obj in links:
            src_node_abs_num = sankey_link_obj.src_node_num
            # Find node obj with the link object's left-major absolute
            # number. The filter() method returns an array, therefore
            # the [0] 
            src_node_obj = filter(lambda sankey_node_obj: sankey_node_obj.num == src_node_abs_num,
                                  nodes)[0]
            node_index   = nodes.index(src_node_obj)
            sankey_link_obj.src_node_num = node_index
            
            # Same for target:
            target_node_abs_num = sankey_link_obj.target_node_num
            target_node_obj = filter(lambda sankey_node_obj: sankey_node_obj.num == target_node_abs_num,
                                     nodes)[0]
            node_index   = nodes.index(target_node_obj)
            sankey_link_obj.target_node_num = node_index
            
        return(nodes, links) 
    
    #--------------------------
    # get_nodes 
    #-------------------
    
    def get_nodes(self, sankey_link_obj_list):
        
        # The 'int' coercion is to avoid the suffix
        # 'L'
        nodes_to_get = [ link_obj.src_node_num for link_obj in sankey_link_obj_list ]
        nodes_to_get.extend([ link_obj.target_node_num for link_obj in sankey_link_obj_list ])

        # Turn into a tuple so that conversion to string
        # in query below will yield a nice list of node numbers
        # in parens:
        
        node_num_tuple = tuple(nodes_to_get)
        
        query = '''SELECT major_num, major
                     FROM major_nums
                    WHERE major_num IN %s;
                ''' % str(node_num_tuple)
        # Get:
        #     [ 
        #       (1,AA-BS)
        #       (2,AES-BAS)
        #       (3,AES-BS)
        #     ]
        MAJOR_NUM  = 0
        MAJOR_NAME = 1
        
        node_info = self.mydb.query(query).nextall()
        
        color_source = ColorSource(len(node_info))
        
        # The 'str()' is to get rid of the unicode 'u' prefix:
        nodes = [ SankeyNode(int(one_node_info[MAJOR_NUM]),
                             str(one_node_info[MAJOR_NAME]),
                             color_source.next()
                             )
                             for one_node_info in node_info 
                             ]
        
        return(nodes)
        
          
    #--------------------------
    # get MySQLPasswd
    #-------------------
    
    def getMySQLPasswd(self):
        homeDir=os.path.expanduser('~'+getpass.getuser())
        f_name = homeDir + '/.ssh/mysql'
        try:
            with open(f_name, 'r') as f:
                password = f.readline().strip()
        except IOError:
            return ''
        return password


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Look up countries from many IP addresses in bulk.')
#     parser.add_argument('--passthrough_lines', 
#                         type=int,
#                         default=0,
#                     help="Number of header lines to copy to output without looking for an IP address. " +
#                           "String 'country,region,city' will be added to each line. Default is 0.")
#     parser.add_argument('infile', type=str,
#                     help='CSV file path with rows that include an IP addresss column')
#     parser.add_argument('ipPos', type=int,
#                     help='Index of column with IP address (0-origin)')
    
#     args = parser.parse_args()
    
    sankay_maker = SankeyMajors()
