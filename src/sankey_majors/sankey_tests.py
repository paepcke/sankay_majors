'''
Created on Apr 29, 2018

@author: paepcke
'''
import plotly


if __name__ == '__main__':
#     data = dict(
#         type='sankey',
#         node = dict(
#           pad = 15,
#           thickness = 20,
#           line = dict(
#             color = "black",
#             width = 0.5
#           ),
#           label = ["A1", "A2", "B1", "B2", "C1", "C2"],
#           color = ["blue", "blue", "blue", "blue", "blue", "blue"]
#         ),
#         link = dict(
#           source = [0,1,0,2,3,3],
#           target = [2,3,3,4,4,5],
#           value = [8,4,2,8,4,2]
#       ))

    data = {
          'type': 'sankey',
          'node':  {
                     'pad': 15,
                     'thickness': 20,
                     'line': {'color': 'black', 'width': 0.5},
                     'label': ['CS-BS', 'ECON-BA', 'ENGL-BA', 'HSTRY-BA', 'INTLR-BA', 'MATH-BS', 'POLSC-BA', 'PSYCH-BA', 'PUBPO-BA'],
                     #*********'color': ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
                     'color': ['rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)','rgb(0.5,0.5,0.5)']
                   },
          'link': {'source': [0, 1, 1, 1, 1, 1, 1, 3],
                   'target': [5, 2, 3, 4, 6, 7, 8, 6],
                   'value': [103, 123, 205, 215, 302, 160, 131, 105]
                  },
        }

    

    
    layout =  dict(
        title = "Basic Sankey Diagram",
        font = dict(
          size = 10
        )
    )
    
    fig = dict(data=[data], layout=layout)
    plotly.offline.plot(fig, validate=False)    
