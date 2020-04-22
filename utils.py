##### UNIVERSAL UTILITY #####
# Simple function to print sudoku puzzles
def show(values, outfile):
    max_width = 1+max(len(values[index]) for index in super_matrix)
    divider = '+'.join(['-'*max_width*3]*3)
    for c in chars:
        print((''.join(values[c+n].center(max_width)+('|' if n in '36' else '') for n in numbers)), file=outfile)
        if c in 'CF':
            print(divider, file = outfile)

#####   DATA STRUCTURES FOR   #####
##### CONSTRAINED BACKTRACING #####
# Function to take cross product of two vectors
def combine(X, Y):
    return [x+y for x in X for y in Y]

### SET UP ###
numbers         = '123456789'                               # Columns Values          A1 A2 A3 A4 A5..  
chars           = 'ABCDEFGHI'                               # Rows Values             B1 B2 B3 B4 B5..
super_matrix    = combine(chars, numbers)                   # A1 - I9 Matrix          C1 C2 C3 C4 C5..        
master_rows     = [combine(chars, n) for n in numbers]      # Array of all rows       [[A1-9], ..., [I1-9]]
master_cols     = [combine(c, numbers) for c in chars]      # Array of all cols       [[A-I1], ..., [A-I9]]
master_squares  = [combine(cs, ns) for cs in ('ABC', 'DEF','GHI') for ns in ('123', '456', '789')]

### REAL STUFF ###
# master_list   - holds combination of all rows, cols and squares
master_list     = (master_rows + master_cols + master_squares)

# index_dict    - dictionary correlating every square to their impacted squares
index_dict      = dict((index, [s for s in master_list if index in s]) for index in super_matrix)

# c_index_dict  - cleaned up dictionary removing self and duplicates
c_index_dict    = dict((index, set(sum(index_dict[index],[])) - set([index])) for index in super_matrix)