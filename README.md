# Conway's Game of Life implementations

Just playing around getting back into programming, different languages, build tools, etc.

Original Rules:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

Condensed Rules:
1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

Further simplified Rules that are easier to program:
1. Any cell, dead or alive, with exactly 3 neighbours is alive in the next generation.
2. A live cell with exactly 2 neighbours is alive in the next generation.
3. All other cells are dead in the next generation.


## Approaches

### Parallel arrays
1. `A[rows][columns]` array created at init
1. Set each individual live cell in `A`
1. Create parallel `B` array set to same size but all cells are dead
1. Algorithm loops through each element `A[row][col]`
    1. Test the 8 adjacent elements of `A[row][col]`, save the result in `B[row][col]`
    1. When testing, overflow on edges so if testing element at edges `cols.max` or `rows.max`, overflow and test from opposite edge. Same for `columns.min` and `rows.min`
1. Assign `B` to `A`
1. Print `A`

Negatives:
1. need `rows*columns*2` of memory, which limits max size
1. we test each element so `O(rows*columns)`, also limits max size

Positives:
1. it's fast for small sized boards
1. no hashtable lookups
1. simple to understand


### TreeMap simple implementation that might work???
1. Create new TreeMap<int[], Cell>, A. 
    1. The key is the int[row,col] of the Cell. 
    1. We rely on the ordering of the keys when later iterating to create an "array view" for display.
    1. TODO: Need to check what natural ordering is of int[row,col] - might have to provide our own Comparator. When we iterate over the keys they need to come out in row order left to right.
1. Create new live Cells and put/replace in TreeMap at their row,col coordinate. No need to check if it exists already.
    1. Check in TreeMap if each neighbour exists. For each that does not exist, add a new dead Cell.
1. Now we have all live and dead Cells that need to be considered when progressing a generation.
1. Create new TreeMap B for next generation.
1. Iterate through all Cells in A
    1. Check each cell - both live and dead - if it will be alive in next gen by doing lookups for all 8 of its neighbours in A. Use predefined `int[row,col]` for N, NE, E, SE, S, SW, W, NW neighbours to avoid garbage collection? Maybe test this for speed.
    1. Because we have also checked all dead neighbours of all live cells, we have checked all cells in the universe that could possibly become live.
    1. If it will be alive, create a new Cell in B, with all it's dead neighbours as above.
    1. If it will be dead, do not add to B.
1. At this point, next generation is ready in B, and has only the live Cells and their immediate dead neighbours.
1. Assign B to A.

Negatives:
1. does a lot of TreeMap lookups

Positives:
1. able to create much larger universes compared to arrays - as long as the universe is sparsely populated
1. no edge to the universe except for Integer.MAX for keys which gliders etc will eventually hit - could try to deal with this by using BigInteger?
1. not too hard to understand


## Old and irrelevant: LinkedList and hashtable lookups
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