# this is solution to a problem from leetcode, 63. Unique Paths II
# ... given a grid of obstacles, find the number of unique paths
# ... to get from the top-left corner to the bottom-right corner
# ... moving only down or right one unit at a time

# this solution follows concepts of dynamic programming, as only a single line array is being utilised
# key to the problem itself is realising the number of ways to reach a square
# ... is the sum of the number of ways to reach the square above and the number of ways to reach the square to the left

def unique_paths(grid):
    line = [0] * len(grid[0])
    line[0] = 1
    for obstacles in grid:
        for i in range(len(obstacles)):
            if obstacles[i] == 1: line[i] = 0
            elif i != 0: line[i] += line[i - 1]
        print(line)
    return line[-1]
     
unique_paths([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
    [0, 0, 0]
])