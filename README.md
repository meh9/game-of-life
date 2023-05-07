# Game of Life implementations



## Approaches

### Parallel arrays:
1. 2x [x][y] arrays created at init, A and B
1. Set each individual live cell in A[x][y]
1. Algorithm loops through each element A[x][y]
1. Test the 8 adjacent elements of A[x][y], save the result in B[x][y]
    1. When testing, overflow on edges so if testing element at right edge (x.max), overflow and test from left edge (x.min)
1. Swap A and B
1. Print A

Downsides:
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