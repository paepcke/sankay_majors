'''
Created on May 1, 2018

@author: paepcke
'''
import random


    # ---------------------------------Color Picking -------------------------    
    #                      from https://gist.github.com/adewes/5884820  
# ==================================================== Class ColorSource ========================
class ColorSource(object):

    #--------------------------
    # constructor 
    #-------------------

    def __init__(self, num_colors):
        self.reserved_colors = self.get_contrasting_colors(num_colors)
        self.i = -1
        
    #--------------------------
    # next 
    #-------------------
        
    def next(self):

        self.i += 1        
        if self.i >= len(self.reserved_colors):
            raise StopIteration()
        
        return 'rgb%s' % str(tuple(self.reserved_colors[self.i]))
        
    
    def __iter__(self):
        return self
    
    
    #--------------------------
    # get_contrasting_colors 
    #-------------------
    
    def get_contrasting_colors(self, num_color):
        
        random.seed(10)
        colors = []

        for _ in range(0,num_color):
            colors.append(self.generate_new_color(colors,pastel_factor = 0.9))
            
        return colors
    
    #--------------------------
    # get_random_color 
    #-------------------
    
    def get_random_color(self, pastel_factor=0.5):
        return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for _ in [1,2,3]]] 

    #--------------------------
    # color_distance 
    #-------------------
    
    def color_distance(self, c1,c2):
        return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

    #--------------------------
    # generate_new_color 
    #-------------------
    
    def generate_new_color(self, existing_colors, pastel_factor = 0.5):
        max_distance = None
        best_color = None
        for _ in range(0,100):
            color = self.get_random_color(pastel_factor = pastel_factor)
            if not existing_colors:
                return color
            best_distance = min([self.color_distance(color,c) for c in existing_colors])
            if not max_distance or best_distance > max_distance:
                max_distance = best_distance
                best_color = color
        return best_color
