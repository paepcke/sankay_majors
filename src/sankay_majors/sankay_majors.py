import argparse
import getpass
import os
import warnings

import MySQLdb
import plotly
from pymysql_utils.pymysql_utils import MySQLDB


#import urllib, json
class SankayMajors(object):
    
    #--------------------------
    # __init__
    #-------------------#--------------------------

    
    def __init__(self,
                 majors_table='sankay'
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
        
        (sources_nums, sources_majors, sources_volumes) = self.get_sources()
        (targets_nums, targets_majors, targets_volumes) = self.get_targets()
        
        self.make_plot(sources_nums,
                       sources_majors,
                       sources_volumes,
                       targets_nums,
                       targets_majors,
                       targets_volumes)       

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
                  sources_nums,
                  sources_majors,
                  sources_volumes,
                  targets_nums,
                  targets_majors,
                  targets_volumes):

        majors_names = sources_majors + targets_majors 
        data = dict(
            type = 'sankey',
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(
                color = "black",
                width = 0.5
              ),
              label = majors_names,
              color = ["blue"]*len(majors_names)
            ),
            link = dict(
              source = sources_nums,
              target = targets_nums,
              value  = sources_volumes
          ))        

        layout =  dict(
            title = "Basic Sankey Diagram",
            font = dict(
              size = 10
            )
        )
        
        fig = dict(data=[data], layout=layout)
        plotly.offline.plot(fig, validate=False)

            
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
    # get
    #-------------------
    
    def getSources(self):
      
        
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
    
    sankay_maker = SankayMajors()

