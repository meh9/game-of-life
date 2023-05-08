# Conway's Game of Life implementations

Just playing around getting back into programming, different languages, build tools, etc.


## Approaches

### Parallel arrays
1. 2x [x][y] arrays created at init, A and B
1. Set each individual live cell in A[x][y]
1. Algorithm loops through each element A[x][y]
1. Test the 8 adjacent elements of A[x][y], save the result in B[x][y]
    1. When testing, overflow on edges so if testing element at right edge (x.max), overflow and test from left edge (x.min)
1. Swap A and B
1. Print A

Negatives:
1. need a lot of memory, which limits max size
1. we test each element so O(x*y), also limits max size

Positives:
1. it's pretty fast for small sized boards
1. no hashtable lookups
1. simple to understand


## LinkedList and hashtable lookups
```
Cell
 - int x
 - int y
 - bool live
 - int[8][2] neighbourCoords
```

Use 2x hashtable<(x,y) -> Cell> to track Cells, A and B.

1. For each new live Cell:
    1. Add to A (do we need to check if there already is a live Cell at those coords in A?)
    1. Check neighbour coords in A, add Dead cell if no cell present

Main loop:

1. Clear B
1. Iterate over A.values
    1. Check all neighbour cells in A
    1. If no live neighbours do nothing (this will garbage collect all dead cells)
    1. Else determine next state dead or alive
    1. If next state is dead add dead to B (Any point in checking if it already exists or is that premature opt?)
    1. Else add new live cell to B and add all dead neighbours that do not already exist in B (ensuring we don't overwrite a live cell)
1. Swap A and B
1. Print A
1. Loop from top

Negatives:
1. needs a lot of hashtable lookups when checking neighbours
1. a little bit more complex to understand than parallel arrays

Positives:
1. sparse board means we are only limited by number of live cells (and their immediate neighbours), which is usually far fewer than empty cells


### Old stuff from here that's too complex!
```
Cell
 - int x
 - int y
 - bool live
 - Cell prevLL
 - Cell nextLL
 - Cell N
 - Cell NE
 - Cell E
 - Cell SE
 - Cell S
 - Cell SW
 - Cell W
 - Cell NW
```

1. Create LinkedList<Cell> and sorted hashtable<(x,y) -> Cell>
```
// new Cell
Cell c = hashtable.get(x,y)
if c == null
    c = new Cell(x,y, live, allNeighbours(x,y), LL.last())
    LL.add(c)
    hashtable.put(x,y, c)
```
1. For each live cell, add to hashtable as (x,y) -> LL_entry
1. For each live cell, also add each adjacent dead cell to LL and hashtable - do not replace live cells, need to do lookups first

Main loop:
1. Iterate through all cells
1. TODO: complicated! finish thinking this through some day