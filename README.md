# Conway's Game of Life implementations

<img width="500" alt="gameplay" src="https://raw.githubusercontent.com/meh9/game-of-life/main/gameplay.gif">

## Just playing around, this is in no way complete and likely never will be. :)

Plans:
1. Java implementation: This was the first implementation. The game logic is complete, but no work on user interface.
1. Python implementation: This is currently the most progressed, and has a simple terminal user interface.
1. TypeScript in NodeJS implementation: Planned, currently unstarted.
1. Haskell implementation: Yeah maybe, would be interesting.
1. C# implementation: Maybe.

TODO:
1. Some form of different UI allowing different zoom levels? (Preferably not a web interface...)
1. Add ability to use different rules.
1. Ability to get RLE and other formats directly from (popular?) GoL sites on the internet.
1. Ability to reset back to last edit. Probably implemented that we save the state when we exit Edit mode.
1. Ability to write out the current board to a file, "Save Game" function.
1. (Done for Python) Add other formats such as Plaintext.
1. (Done for Python) Add RLE (Run Length Encoded) file format reading.
1. (Done for Python) GitHub Actions CI?
1. (Done for Python) Codecov?
1. (Done in Python) Implement simple terminal based interface.
1. (Done in Java, Python) Add GitHub Dependabot.
1. (Done in Java, Python) Add tests.
1. (Done in Java, Python) Implement game logic.
1. (Done in Java, Python) Use languange appropriate build management tools.


## Conway's Game of Life rules

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

### Set based simple implementation
1. Create new Set<int, int>, `A`. This set simply records the coordinates as (row,col) of live cells. By being in the set it's a live cell. We don't record dead cells, so it is a very sparse data structure.
1. Create new set `B` for next generation.
1. Create a new ephemeral set for recording dead cells that have been checked this generation, `tmp`.
1. Iterate through all live cells in `A`
    1. For each cell, check how many of the 8 neighbours are alive in `A`. If 2 or 3, this cell stays alive so add the coordinates to the next-gen `B` set.
    1. Get the collection of the 8 neighbours that are dead.
    1. Check each of the dead cells if it has already been checked by looking if it is in `tmp`.
    1. Check if the dead neighbour has exactly 3 live neighbours in `A`, in which case it will come alive in the next generation, so add it to `B` meaning it will be live.
    1. Record the dead cell in `tmp` as having been checked.
    1. We have now checked all live cells, and all their neighbours - this means we have checked all cells in the universe that could possibly become live.
1. At this point the next generation of live cells is ready in `B`.
1. Assign `B` to `A`, clear `tmp`.

Negatives:
1. only 2 states per cell - alive (coordinates present) or dead (coordinates not present)
1. does a lot of set lookups:
    1. 8 lookups to find the neighbours of each live cell
    1. 1 lookup for each dead neighbour to see if it has already been checked
    1. for each of the dead neighbours that has not already been checked, another 8 lookups to see if it has enough live neighbours to come alive

Positives:
1. memory efficient as we only store coordinates, no other state
1. able to create much larger universes compared to e.g. arrays or the map implementation - as long as the universe is sparsely populated
1. no edge to the universe except for the languages maximum key value (e.g. in Java Integer.MAX) which gliders etc will eventually hit - could try to deal with this by using some implementation of e.g. BigInteger?
1. not too hard to understand


### 2D arrays
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


### TreeMap simple implementation - actually scratch that, the Python version now uses a normal map/dict for better performance.
1. Create new TreeMap<int[], Cell>, A. 
    1. The key is the int[row,col] of the Cell. 
    1. We rely on the ordering of the keys when later iterating to create an "array view" for display.
        1. Funnily enough the way the python version was implemented this is not actually true and we _do not_ rely on the ordering. Changing to a normal dict resulted in an immediate 30% performance increase.
        1. Revisit this in the Java version some time.
    1. Need to check what natural ordering is of int[row,col] - might have to provide our own Comparator. When we iterate over the keys they need to come out in row order left to right.
1. Create new live Cells and put/replace in map at their row,col coordinate. No need to check if it exists already.
    1. Check in map if each neighbour exists. For each that does not exist, add a new dead Cell.
1. Now we have all live and dead Cells that need to be considered when progressing a generation.
1. Create new map B for next generation.
1. Iterate through all Cells in A
    1. Check each cell - both live and dead - if it will be alive in next gen by doing lookups for all 8 of its neighbours in A. Use predefined `int[row,col]` for N, NE, E, SE, S, SW, W, NW neighbours to avoid garbage collection? Maybe test this for speed.
    1. Because we have also checked all dead neighbours of all live cells, we have checked all cells in the universe that could possibly become live.
    1. If it will be alive, create a new Cell in B, with all it's dead neighbours as above.
    1. If it will be dead, do not add to B.
1. At this point, next generation is ready in B, and has only the live Cells and their immediate dead neighbours.
1. Assign B to A.

Negatives:
1. does a lot of map lookups

Positives:
1. able to create much larger universes compared to arrays - as long as the universe is sparsely populated
1. no edge to the universe except for Integer.MAX for keys which gliders etc will eventually hit - could try to deal with this by using BigInteger?
1. not too hard to understand
