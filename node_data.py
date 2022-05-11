"""
The data for every node. The format is as follows:

'name' -> The name of the node. This will be shown on the node itself
'desc'-> The description of the node. This will be shown in the node's tooltip
'color' -> The color of the node's body.
'cost' -> The monetary cost to purchase the node.
'parent' -> The name of the parent of this node. *name, not a reference to
'children' -> The names of the children of this node. *names, not references to
'generation' -> The generation of this node.
'index' -> A number that helps with the spacing of the nodes
'dist' -> The distance between this node and it's parent
"""


main_data = [{'name': 'EARTH',
            'desc': 'center',
            'color': 'white',
            'cost': 0,
            'is_zoomable': True,
            'parent': None,
            'children': ['ACQUISITIONS', 'OPS', 'PERSONNEL', 'GSSAP'],
            'generation': 0,
            'index': 0,
            'dist': 0},

            {'name': 'ACQUISITIONS',
            'desc': 'this is an upgrade',
            'color': 'orange',
            'cost': 10,
            'is_zoomable': True,
            'parent': 'EARTH',
            'children': [],
            'generation': 1,
            'index': 1,
            'dist': 150},
            {'name': 'OPS',
            'desc': 'this is an upgrade',
            'color': 'orange',
            'cost': 10,
            'is_zoomable': True,
            'parent': 'EARTH',
            'children': [],
            'generation': 1,
            'index': 2,
            'dist': 120},
            {'name': 'PERSONNEL',
            'desc': 'this is an upgrade',
            'color': 'orange',
            'cost': 10,
            'is_zoomable': True,
            'parent': 'EARTH',
            'children': [],
            'generation': 1,
            'index': 3,
            'dist': 110},
            {'name': 'GSSAP',
            'desc': 'A satellite',
            'color': 'red',
            'cost': 10,
            'is_zoomable': True,
            'parent': 'EARTH',
            'children': [],
            'generation': 5,
            'index': 1,
            'dist': 400}]

gssap_data = [{'name': 'GSSAP',
                'desc': 'A satellite used for observation and spy things',
                'color': 'red',
                'cost': 0,
                'is_zoomable': False,
                'parent': None,
                'children': ['PRICE-', 'BETTER ELECTRONICS', 'BETTER MATERIALS'],
                'generation': 0,
                'index': 0,
                'dist': 110},

                {'name': 'BETTER ELECTRONICS',
                'desc': 'General improvements to the onboard electronics',
                'color': 'orange',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'GSSAP',
                'children': ['ACCURACY+', 'AI ENHANCED TRACKING'],
                'generation': 1,
                'index': 2,
                'dist': 200},

                {'name': 'BETTER MATERIALS',
                'desc': 'Everything gets better',
                'color': 'orange',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'GSSAP',
                'children': ['SPEED', 'RESIALANCY'],
                'generation': 2,
                'index': 2,
                'dist': 140},

                {'name': 'PRICE-',
                'desc': 'Make each satellite a little cheaper',
                'color': 'orange',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'GSSAP',
                'children': ['PRICE--'],
                'generation': 1,
                'index': 1,
                'dist': 150},
                {'name': 'PRICE--',
                'desc': 'Only a couple million dollars now',
                'color': 'mint',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'PRICE-',
                'children': ['PRICE---'],
                'generation': 2,
                'index': 1,
                'dist': 110},
                {'name': 'PRICE---',
                'desc': "It's cheaper to buy penny stocks",
                'color': 'skyblue',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'PRICE--',
                'children': [],
                'generation': 3,
                'index': 1,
                'dist': 110},

                {'name': 'SPEED',
                'desc': 'Faster movement means better evasion',
                'color': 'mint',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'BETTER MATERIALS',
                'children': ['SPEEEED'],
                'generation': 2,
                'index': 1,
                'dist': 110},
                {'name': 'SPEEEED',
                'desc': 'WEEEEEEEEEEEEEEE',
                'color': 'skyblue',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'SPEED',
                'children': [],
                'generation': 3,
                'index': 1,
                'dist': 110},
                {'name': 'RESIALANCY',
                'desc': 'Basically HP',
                'color': 'mint',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'BETTER MATERIALS',
                'children': [],
                'generation': 2,
                'index': 2,
                'dist': 110},

                {'name': 'AI ENHANCED TRACKING',
                'desc': 'Adds an AI system (Buzz) to aid in tracking',
                'color': 'mint',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'BETTER ELECTRONICS',
                'children': [],
                'generation': 2,
                'index': 2,
                'dist': 120},

                {'name': 'ACCURACY+',
                'desc': 'Make each satellite a little more accurate',
                'color': 'mint',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'BETTER ELECTRONICS',
                'children': ['ACCURACY++'],
                'generation': 2,
                'index': 1,
                'dist': 140},
                {'name': 'ACCURACY++',
                'desc': 'You can watch a mosquito fly around NYC with ease',
                'color': 'skyblue',
                'cost': 10,
                'is_zoomable': False,
                'parent': 'ACCURACY+',
                'children': [],
                'generation': 3,
                'index': 1,
                'dist': 110}]
