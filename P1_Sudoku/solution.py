
from utils import *

vis_solver = False # True: turn on searching procedure, False: Turn off

left_diagonal_units = [["{}{}".format(r, c) for r, c in zip(rows, cols)]]
right_diagonal_units = [["{}{}".format(r, c) for r, c in zip(rows, cols[::-1])]]
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + left_diagonal_units + right_diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # # Collect boxes with only 2 elements
    # potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    # # Extract nake twin pairs 
    # naked_twins = [] 
    # for box1 in potential_twins:
    #     for box2 in peers[box1]:
    #         if set(values[box1])==set(values[box2]): 
    #             naked_twins.append([box1, box2])

    # # Remove the elements, which show in box1 and box2, from their union peers
    # for box1, box2 in naked_twins:
    #     # Extract all peers of the twin pairs
    #     common_peers = set(peers[box1]) & set(peers[box2])
    #     # Delete the two digits in naked twins from all union peers.
    #     for peer in common_peers:
    #         if len(values[peer])>2:
    #             for digit in values[box1]:
    #                 values = assign_value(values, peer, values[peer].replace(digit,''))
    # return values
    for unit in unitlist:  # for each unit (row/column/square/diagonal)
        # create a dictionary 'inv_twin_dict' that inverse maps value to box,
        # i.e., key is the value of that box, and value is the box label
        unit_values = [values[element] for element in unit]
        unit_dict = dict(zip(unit, unit_values))
        inverse_map = {}
        for key, value in unit_dict.items():
            inverse_map.setdefault(value, []).append(key)
        inv_twin_dict = {key: value for key, value in inverse_map.items() if len(value) == 2 and len(key) == 2}

        # create a list of unsolved boxes in that unit
        unsolved_boxes = [key for key in unit_dict.keys() if len(unit_dict[key]) > 1]

        # check the value of any unsolved box (exclude twin boxes)
        # if a digit is in any twin box, delete that digit from the unsolved box value
        for twin_value, twin_box in inv_twin_dict.items():
            for unsolved_box in unsolved_boxes:
                if unsolved_box not in twin_box:
                    for digit in twin_value:
                        # values[unsolved_box] = values[unsolved_box].replace(digit, '')
                        new_value = values[unsolved_box].replace(digit, '')
                        assign_value(values, unsolved_box, new_value)

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # applied strategies
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False # Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values # Solved
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Use recurrence to solve each one of the resulting sudokus (DFS)
    for value in values[s]:
        new_sudoku = values.copy() # Always use copied sudoku to search solution
        new_sudoku = assign_value(new_sudoku, s, value)
        # new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


before_naked_twins_2 = {"H8": "345678", "D9": "47", "D5": "36", "A7": "234568", "G8": "345678", "B8": "3456789", "E9": "3", "H9": "24578", "F6": "37", "C7": "2345678", "G4": "345678", "C1": "2345689", "A5": "1", "C5": "23456789", "D2": "9", "B2": "1234568", "A6": "23689", "A4": "34568", "G6": "1236789", "F3": "24", "I7": "1", "C8": "3456789", "I8": "345678", "B9": "124578", "H4": "345678", "G5": "23456789", "H3": "1234569", "E6": "4", "I2": "2345678", "B1": "2345689", "E8": "1", "H6": "1236789", "C2": "1234568", "E7": "9", "F8": "58", "I5": "2345678", "D1": "36", "G9": "24578", "A2": "234568", "A9": "2458", "B6": "236789", "I9": "9", "H2": "12345678", "D4": "1", "F5": "37", "B7": "2345678", "C6": "236789", "A1": "2345689", "E1": "567", "D7": "47", "D8": "2", "F4": "9", "A3": "7", "F2": "24", "G2": "12345678", "G1": "23456789", "I1": "2345678", "D3": "8", "D6": "5", "I3": "23456", "E5": "678", "B5": "23456789", "B4": "345678", "C3": "1234569", "C9": "124578", "I4": "345678", "G3": "1234569", "H7": "2345678", "G7": "2345678", "B3": "1234569", "H5": "23456789", "F7": "58", "H1": "23456789", "F1": "1", "F9": "6", "E2": "567", "E3": "56", "I6": "23678", "E4": "2", "C4": "345678", "A8": "345689"}
display(before_naked_twins_2)

possible_solutions_2 = {"A7": "234568", "G8": "345678", "B8": "3456789", "E9": "3", "G4": "345678", "A5": "1", "G6": "1236789", "I7": "1", "I8": "345678", "B9": "124578", "H4": "345678", "G5": "23456789", "H3": "1234569", "I3": "23456", "I5": "2345678", "B5": "23456789", "D1": "36", "G9": "24578", "D4": "1", "D9": "47", "H8": "345678", "D6": "5", "G2": "12345678", "G1": "23456789", "I1": "2345678", "E6": "4", "E5": "68", "A9": "2458", "B4": "345678", "D7": "47", "I4": "345678", "F7": "58", "H1": "23456789", "C7": "2345678", "I6": "23678", "I9": "9", "C4": "345678", "D8": "2", "F6": "37", "C1": "2345689", "C5": "23456789", "D2": "9", "F5": "37", "A6": "23689", "A4": "34568", "C9": "124578", "H6": "1236789", "F3": "24", "E8": "1", "C8": "3456789", "B7": "2345678", "I2": "2345678", "B1": "2345689", "C2": "1234568", "E7": "9", "F8": "58", "H9": "24578", "B6": "236789", "D5": "36", "B2": "1234568", "C6": "236789", "E1": "567", "A1": "2345689", "A3": "7", "F2": "24", "D3": "8", "H5": "23456789", "A2": "234568", "C3": "1234569", "F4": "9", "G3": "1234569", "H7": "2345678", "G7": "2345678", "B3": "1234569", "H2": "12345678", "F1": "1", "F9": "6", "E2": "567", "A8": "345689", "E4": "2", "E3": "56"}

print (naked_twins(before_naked_twins_2)==possible_solutions_2)
display(possible_solutions_2)

# if __name__ == "__main__":
#     diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#     # display(grid2values(diag_sudoku_grid))
#     result = solve(diag_sudoku_grid)
#     display(result)

#     try:
        
#         import PySudoku
        
#         if not vis_solver:
#             # show initial state
#             history = {}
#             PySudoku.play(grid2values(diag_sudoku_grid), result, history)
        
#         else:
#             # demo solver history
#             PySudoku.play(grid2values(diag_sudoku_grid), result, history)

#     except SystemExit:
#         pass
#     except:  # conda install -c cogsci pygame 
#         print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
