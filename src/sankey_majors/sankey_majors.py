import argparse
import getpass
import os

from pymysql_utils.pymysql_utils import MySQLDB

from sankey_diagram import SankeyNode, SankeyLink, SankeyDiagram


#import urllib, json
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
     
    MIN_MAJOR_TRANSITIONS = 99
    
    #--------------------------
    # __init__
    #-------------------#--------------------------

    
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
        
        nodes = self.get_nodes()
        links = self.get_links()
        SankeyDiagram.plot_sankey(nodes, 
                                  links, 
                                  plot_title="Majors Transitions")
        
    #--------------------------
    # get_nodes 
    #-------------------
    
    def get_nodes(self):
        query = '''SELECT major_num, major
                     FROM major_nums;
                '''
        # Get:
        #     [ 
        #       (1,AA-BS)
        #       (2,AES-BAS)
        #       (3,AES-BS)
        #     ]
        MAJOR_NUM  = 0
        MAJOR_NAME = 1
        
        node_info = self.mydb.query(query).nextall()
        nodes = [ SankeyNode(one_node_info[MAJOR_NUM],
                             one_node_info[MAJOR_NAME],
                             self.get_color(one_node_info[MAJOR_NAME])
                             )
                             for one_node_info in node_info 
                             ]
        return(nodes)
        
    #--------------------------
    # get_links 
    #-------------------
    
    def get_links(self):
    
        query = '''SELECT major_left_num, major_right_num, count(*) AS num_transitions
                     FROM majors_transitions
                     GROUP BY major_left_num, major_right_num
                     HAVING num_transitions > %s
                ''' % SankeyMajors.MIN_MAJOR_TRANSITIONS 
                
        MAJOR_LEFT_NUM = 0
        MAJOR_RIGHT_NUM = 1
        NUM_TRANSITIONS = 2
        
        link_info = self.mydb.query(query).nextall()
        links = [ SankeyLink(one_link_info[MAJOR_LEFT_NUM],
                             one_link_info[MAJOR_RIGHT_NUM],
                             one_link_info[NUM_TRANSITIONS]
                             )
                             for one_link_info in link_info
                 ]
        return(links)
    
    #--------------------------
    # get_color 
    #-------------------
    
    def get_color(self, major_name):
        return 'blue'
    #--------------------------
    # get_sources
    #-------------------
    
    def get_sources(self):
      
        
        query = '''SELECT major_num_left, major AS major_name_left, count(*) AS num_students
                    FROM majors_links LEFT JOIN majors_nodes
                      ON majors_links.major_num_left = majors_nodes.node_num
                   WHERE is_ug = 1
                  GROUP BY major_num_left;
                '''
        node_num_pos = 0
        node_majors_pos = 1
        node_volume_pos = 2
        sources_node_nums_names_and_volumes = self.mydb.query(query).nextall()
        sources_nums = [sources_info[node_num_pos] for sources_info in sources_node_nums_names_and_volumes]
        sources_majors  = [sources_info[node_majors_pos] for sources_info in sources_node_nums_names_and_volumes]
        sources_volumes = [sources_info[node_volume_pos] for sources_info in sources_node_nums_names_and_volumes]
        return (sources_nums, sources_majors, sources_volumes)
        

    #--------------------------
    # get_targets
    #-------------------
    
    def get_targets(self):
      
        
        query = '''SELECT major_num_right, major AS major_right, count(*) AS num_students
                    FROM majors_links LEFT JOIN majors_nodes
                      ON majors_links.major_num_right = majors_nodes.node_num
                   WHERE is_ug = 1
                  GROUP BY major_num_right;
                '''
        node_num_pos = 0
        node_majors_pos = 1
        node_volume_pos = 2
        targets_node_nums_names_and_volumes = self.mydb.query(query).nextall()
        targets_nums = [targets_info[node_num_pos] for targets_info in targets_node_nums_names_and_volumes]
        targets_majors  = [targets_info[node_majors_pos] for targets_info in targets_node_nums_names_and_volumes]
        targets_volumes = [targets_info[node_volume_pos] for targets_info in targets_node_nums_names_and_volumes]
        return (targets_nums, targets_majors, targets_volumes)

    #--------------------------
    # 
    #-------------------
    
    def make_plot(self,
                  source_nums,
                  source_majors,
                  sources_volumes,
                  targets_nums,
                  targets_majors,
                  targets_volumes):

        majors_nums   = source_nums   + targets_nums
        majors_names  = source_majors + targets_majors
        majors_colors = ['blue']*len(majors_nums)
        
        nodes = [ SankeyNode(node_info[0],
                             node_info[1],
                             node_info[2]
                             ) 
                             for node_info in zip(majors_nums, majors_names, majors_colors) 
                             ]

        links = [ SankeyLink(link_info[0],
                             link_info[1],
                             link_info[2]
                             ) 
                             for link_info in zip(source_nums, targets_nums, targets_volumes) 
                             ]
        
        


            
    #--------------------------
    # get_major_names 
    #-------------------
    
    def get_major_names(self):
      
        
        query = '''SELECT major_num_left, count(*) AS num_students
                    FROM majors_links LEFT JOIN majors_nodes
                      ON majors_links.major_num_left = majors_nodes.node_num
                   WHERE is_ug = 1
                  GROUP BY major_num_left;
                '''
        source_nodes_and_volumes = self.mydb.query(query).nextall()
        sources = [sources_and_volumes[0] for sources_and_volumes in source_nodes_and_volumes]
        volumes = [sources_and_volumes[1] for sources_and_volumes in source_nodes_and_volumes]
        return (sources, volumes)

          
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
