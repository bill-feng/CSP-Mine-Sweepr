'''
Construct and return minesweeper CSP models.
'''

from cspbase import *
import itertools
import propagators


def minesweeper_csp_model_2d(initial_mine_board):
    '''
    Return a CSP object representing a minesweeper game.

    The input mine field would be represented by a list of lists of integers.
    An example mine field:
       -------------------
       |0|0|1|0|3|0|0|4|0|
       |1|2|2|3|0|4|0|0|2|
       |0|2|0|2|1|2|3|3|2|
       |2|3|2|2|1|0|1|0|1|
       |0|1|2|0|2|0|1|1|1|
       |1|1|2|0|2|0|0|0|0|
       -------------------

    And the solution should look something like this:
       -------------------
       | | |1|*|3|*|*|4|*|
       |1|2|2|3|*|4|*|*|2|
       |*|2|*|2|1|2|3|3|2|
       |2|3|2|2|1| |1|*|1|
       |*|1|2|*|2| |1|1|1|
       |1|1|2|*|2| | | | |
       -------------------
    '''

    variables = []
    variable_array = []
    for i in range(0, len(initial_mine_board)):
        row = []
        for j in range(0, len(initial_mine_board[0])):
            if initial_mine_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [" ", "*"])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_mine_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)

    reduce(variable_array, initial_mine_board)
    mine_csp = CSP("Minesweeper-2d", variables)

    # add constraints here
    for i in range(0, len(variable_array)):
        for j in range(0, len(variable_array[0])):
            if initial_mine_board[i][j] != 0:
                constraint = Constraint("C{},{}".format(i, j), get_variables_around(i, j, variable_array))

                domain = []
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if 0 <= (i + k) < len(variable_array) and 0 <= (j + l) < len(variable_array[0]):
                            domain.append(variable_array[i + k][j + l])
                holder = [0, 0, 0, 0, 0, 0, 0, 0]
                sat_tuples = []
                recursive_sat(domain, holder, sat_tuples)
                mine_csp.add_constraint(constraint)

    for row in variable_array:
        for item in row:
            item.restore_curdom()
    return mine_csp, variable_array


def minesweeper_csp_model_3d(initial_mine_board):
    variables = []
    variable_array = []
    for i in range(0, len(initial_mine_board)):
        layer = []
        for j in range(0, len(initial_mine_board[0])):
            row = []
            for k in range(0, len(initial_mine_board[0][0])):
                if initial_mine_board[i][j][k] == 0:
                    variable = Variable("V({},{},{})".format(i, j, k), [True, False])
                else:
                    variable = Variable("V({},{},{})".format(i, j, k), [initial_mine_board[i][j]])
                variables.append(variable)
                row.append(variable)
            layer.append(row)
        variable_array.append(layer)

    reduce_3d(variable_array, initial_mine_board)
    mine_csp = CSP("Minesweeper-3d", variables)

    # add constraints here
    for i in range(0, len(variable_array)):
        for j in range(0, len(variable_array[0])):
            for k in range(0, len(variable_array[0][0])):
                if initial_mine_board[i][j][k] != 0:
                    constraint = Constraint("C{},{}".format(i, j), get_variables_3d(i, j, k, variable_array))
                    add_mine_tuples(constraint, initial_mine_board[i][j])
                    mine_csp.add_constraint(constraint)

    for layer in variable_array:
        for row in layer:
            for item in row:
                item.restore_curdom()
    return mine_csp, variable_array


'''
def sudoku_csp_model_1(initial_sudoku_board):

#comment

       Return a CSP object representing a sudoku CSP problem along
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))
       
       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
      [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).

#comment
    
#IMPLEMENT
    variables = []
    variable_array = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            if initial_sudoku_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_sudoku_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)

    reduce(variable_array,initial_sudoku_board)
    sudoku_csp = CSP("Sudoku-M1", variables)

    for i in range(0, 9):
        for j in range(0, 9):
            for k in range(j + 1, 9):
                constraint = Constraint("C(({},{}),({},{}))".format(i+1,j+1,i+1,k+1),
                                        [variable_array[i][j], variable_array[i][k]])
                sat_tuples = []
                for sat_tuple in itertools.product(variable_array[i][j].cur_domain(),
                                                   variable_array[i][k].cur_domain()):
                    if sat_tuple[0] != sat_tuple[1]:
                        sat_tuples.append(sat_tuple)
                constraint.add_satisfying_tuples(sat_tuples)
                sudoku_csp.add_constraint(constraint)

    for i in range(0, 9):
        for j in range(0, 9):
            for k in range(i + 1, 9):
                constraint = Constraint("C(({},{}),({},{}))".format(i+1,j+1,k+1,j+1),
                                        [variable_array[i][j], variable_array[k][j]])
                sat_tuples = []
                for sat_tuple in itertools.product(variable_array[i][j].cur_domain(),
                                                   variable_array[k][j].cur_domain()):
                    if sat_tuple[0] != sat_tuple[1]:
                        sat_tuples.append(sat_tuple)
                constraint.add_satisfying_tuples(sat_tuples)
                sudoku_csp.add_constraint(constraint)

    for i in range(0, 3):
        for j in range(0, 3):
            for k in range(0, 3):
                for l in range(0, 3):
                    for m in range(k*3+l+1, 9):
                        if k!=m//3 and l!=m%3:
                            constraint = Constraint("C(({},{}),({},{}))".format(i*3+k+1,j*3+l+1,i*3+m//3+1,j*3+m%3+1),
                                                    [variable_array[i*3+k][j*3+l], variable_array[i*3+m//3][j*3+m%3]])
                            sat_tuples = []
                            for sat_tuple in itertools.product(variable_array[i*3+k][j*3+l].cur_domain(),
                                                               variable_array[i*3+m//3][j*3+m%3].cur_domain()):
                                if sat_tuple[0] != sat_tuple[1]:
                                    sat_tuples.append(sat_tuple)
                            constraint.add_satisfying_tuples(sat_tuples)
                            sudoku_csp.add_constraint(constraint)

    for row in variable_array:
        for item in row:
            item.restore_curdom()
    return sudoku_csp, variable_array

'''

##############################

'''
def sudoku_csp_model_2(initial_sudoku_board):

#comment

       Return a CSP object representing a sudoku CSP problem along
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.

#comment

#IMPLEMENT
    variables = []
    variable_array = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            if initial_sudoku_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_sudoku_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)

    reduce(variable_array, initial_sudoku_board)
    sudoku_csp = CSP("Sudoku-M2", variables)

    for i in range(0, 9):
        constraint = Constraint("C(ROW{})".format(i+1), variable_array[i])

        dm = [variable_array[i][0].cur_domain(),
              variable_array[i][1].cur_domain(),
              variable_array[i][2].cur_domain(),
              variable_array[i][3].cur_domain(),
              variable_array[i][4].cur_domain(),
              variable_array[i][5].cur_domain(),
              variable_array[i][6].cur_domain(),
              variable_array[i][7].cur_domain(),
              variable_array[i][8].cur_domain()]

        holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sat_tuples = []
        recursive_sat(dm, holder, sat_tuples)
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    for i in range(0, 9):
        var_arr = []
        for j in range(0, 9):
            var_arr.append(variable_array[j][i])
        constraint = Constraint("C(COL{})".format(i+1), var_arr)

        dm = [variable_array[0][i].cur_domain(),
              variable_array[1][i].cur_domain(),
              variable_array[2][i].cur_domain(),
              variable_array[3][i].cur_domain(),
              variable_array[4][i].cur_domain(),
              variable_array[5][i].cur_domain(),
              variable_array[6][i].cur_domain(),
              variable_array[7][i].cur_domain(),
              variable_array[8][i].cur_domain()]

        holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sat_tuples = []
        recursive_sat(dm, holder, sat_tuples)
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    for i in range(0, 3):
        for j in range(0, 3):
            var_arr = []
            for k in range(0, 3):
                for l in range(0, 3):
                    var_arr.append(variable_array[i*3+k][j*3+l])
            constraint = Constraint("C(BOX{})".format(i*3+j+1), var_arr)

            dm = [variable_array[i*3][j*3].cur_domain(),
                  variable_array[i*3][j*3+1].cur_domain(),
                  variable_array[i*3][j*3+2].cur_domain(),
                  variable_array[i*3+1][j*3].cur_domain(),
                  variable_array[i*3+1][j*3+1].cur_domain(),
                  variable_array[i*3+1][j*3+2].cur_domain(),
                  variable_array[i*3+2][j*3].cur_domain(),
                  variable_array[i*3+2][j*3+1].cur_domain(),
                  variable_array[i*3+2][j*3+2].cur_domain()]

            holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            sat_tuples = []
            recursive_sat(dm, holder, sat_tuples)
            constraint.add_satisfying_tuples(sat_tuples)
            sudoku_csp.add_constraint(constraint)

    for row in variable_array:
        for item in row:
            item.restore_curdom()
    return sudoku_csp, variable_array

'''


def reduce(table, initial):
    for i in range(0, len(initial)):
        for j in range(0, len(initial[0])):
            if initial[i][j] == 0 and no_indicator(initial, i, j):
                table[i][j].prune_value(True)


def no_indicator(initial, i, j):
    for k in range(-1, 2):
        for l in range(-1, 2):
            if 0 <= (i + k) < len(initial) and 0 <= (j + l) < len(initial[0]):
                if initial[i + k][j + l] !=0:
                    return False
    return True


def reduce_3d(table, initial):
    for i in range(0, len(initial)):
        for j in range(0, len(initial[0])):
            for k in range(0, len(initial[0][0])):
                if initial[i][j][k] == 0 and no_indicator_3d(initial, i, j, k):
                    table[i][j].prune_value(True)


def no_indicator_3d(initial, i, j, k):
    for l in range(-1, 2):
        for m in range(-1, 2):
            for n in range(-1, 2):
                if 0 <= (i + l) < len(initial) and 0 <= (j + m) < len(initial[0]) and 0 <= (k + n) < len(initial[0]):
                    if initial[i + l][j + m][k + n] !=0:
                        return False
    return True


def get_variables_around(i, j, table):
    array = []
    for k in range(-1, 2):
        for l in range(-1, 2):
            if not(k == 0 and l == 0) and 0 <= (i + k) < len(table) and 0 <= (j + l) < len(table[0]):
                array.append(table[i + k][j + l])
    return array


def get_variables_3d(i, j, k, table):
    array = []
    for l in range(-1, 2):
        for m in range(-1, 2):
            for n in range(-1, 2):
                if not(l == 0 and m == 0 and n == 0) and 0 <= (i + l) < len(table) and 0 <= (j + m) < len(table[0]) and 0 <= (k + n) < len(table[0][0]):
                    array.append(table[i + l][j + m][k + n])
    return array


def recursive_sat(domain, holder, sat_tuples):
    if len(domain) == 1:
        for item in domain[0]:
            if item not in holder:
                holder[8] = item
                sat_tuples.append(list(holder))
    else:
        temp = domain.pop(0)
        for item in temp:
            if item not in holder:
                holder[8-len(domain)] = item
                recursive_sat(list(domain), list(holder), sat_tuples)
