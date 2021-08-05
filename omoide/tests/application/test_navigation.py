# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from omoide.application import navigation


@pytest.fixture
def reference_graph():
    return {
        'A': {
            'label': 'Basic',
            'elements': {
                'A-1': {
                    'label': 'Mice and humans',
                    'elements': {
                        'A-1-1': {
                            'label': 'History',
                        },
                        'A-1-2': {
                            'label': 'As pets',
                        },
                        'A-1-3': {
                            'label': 'As model organism',
                        },
                        'A-1-4': {
                            'label': 'Folk culture',
                        },
                    }
                },
                'A-2': {
                    'label': 'Life expectancy',
                },
                'A-3': {
                    'label': 'Life cycle and reproduction',
                    'elements': {
                        'A-3-1': {
                            'label': 'Polygamy',
                        },
                        'A-3-2': {
                            'label': 'Polyandry',
                        },
                    }
                }
            },
        },
        'B': {
            'label': 'Animalia',
        },
        'C': {
            'label': 'Senses',
            'elements': {
                'C-1': {
                    'label': 'Vision'
                },
                'C-2': {
                    'label': 'Olfaction'
                },
                'C-3': {
                    'label': 'Tactile'
                },
            },
        },
        'D': {
            'label': 'Behavior',
            'elements': {
                'D-1': {
                    'label': 'Social behavior'
                }
            }
        }
    }


def test_calculate_graph_dimensions(reference_graph):
    height, width = navigation.calculate_graph_dimensions(reference_graph)
    assert height == 12
    assert width == 3


def test_calculate_table_dimensions(reference_graph):
    rows, cols = navigation.calculate_table_dimensions(reference_graph)
    assert rows == 23
    assert cols == 5


def test_generate_empty_table():
    dim = 2, 5
    table = navigation.generate_empty_table(*dim)
    text = navigation.stringify_table(table, width=5, verbose=True)

    assert text == """
[_____][_____][_____][_____][_____]
[_____][_____][_____][_____][_____]
    """.strip()


def test_populate_table(reference_graph):
    rows, cols = navigation.calculate_table_dimensions(reference_graph)
    table = navigation.generate_empty_table(rows, cols)
    initials = []
    coordinates = {}
    navigation.populate_table(table, reference_graph, initials, coordinates)
    navigation.continue_lines(table, initials)

    text = navigation.stringify_table(table, width=13, verbose=True)
    assert text == """
[Basic________][──────┬──────][Mice and huma][──────┬──────][History______]
[_____________][______│______][_____________][______│______][_____________]
[_____________][______│______][_____________][______├──────][As pets______]
[_____________][______│______][_____________][______│______][_____________]
[_____________][______│______][_____________][______├──────][As model orga]
[_____________][______│______][_____________][______│______][_____________]
[_____________][______│______][_____________][______└──────][Folk culture_]
[_____________][______│______][_____________][_____________][_____________]
[_____________][______├──────][Life expectan][_____________][_____________]
[_____________][______│______][_____________][_____________][_____________]
[_____________][______└──────][Life cycle an][──────┬──────][Polygamy_____]
[_____________][_____________][_____________][______│______][_____________]
[_____________][_____________][_____________][______└──────][Polyandry____]
[_____________][_____________][_____________][_____________][_____________]
[Animalia_____][_____________][_____________][_____________][_____________]
[_____________][_____________][_____________][_____________][_____________]
[Senses_______][──────┬──────][Vision_______][_____________][_____________]
[_____________][______│______][_____________][_____________][_____________]
[_____________][______├──────][Olfaction____][_____________][_____________]
[_____________][______│______][_____________][_____________][_____________]
[_____________][______└──────][Tactile______][_____________][_____________]
[_____________][_____________][_____________][_____________][_____________]
[Behavior_____][─────────────][Social behavi][_____________][_____________]
        """.strip()

    text = navigation.stringify_table(table, width=13, verbose=False)
    assert text == """
Basic        ──────┬──────Mice and huma──────┬──────History      
                   │                         │                   
                   │                         ├──────As pets      
                   │                         │                   
                   │                         ├──────As model orga
                   │                         │                   
                   │                         └──────Folk culture 
                   │                                             
                   ├──────Life expectan                          
                   │                                             
                   └──────Life cycle an──────┬──────Polygamy     
                                             │                   
                                             └──────Polyandry    
                                                                 
Animalia                                                         
                                                                 
Senses       ──────┬──────Vision                                 
                   │                                             
                   ├──────Olfaction                              
                   │                                             
                   └──────Tactile                                
                                                                 
Behavior     ─────────────Social behavi             
        """.strip() + '                          '
