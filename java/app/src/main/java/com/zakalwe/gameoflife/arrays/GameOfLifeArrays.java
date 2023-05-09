package com.zakalwe.gameoflife.arrays;

/**
 * The actual Conway's Game of Life implementation.
 * 
 * This implementation uses a fixed sized (double array) universe where cells wrap around the edges.
 */
public class GameOfLifeArrays {

    private boolean[][] a;
    private boolean[][] b;
    private int iteration = 0;
    
    /** Initialise arrays 
     * @param x width of the board
     * @param y height of the board
     */
    public GameOfLifeArrays(final int x, final int y) {
        a = new boolean[y][x];
        b = new boolean[y][x];
    }

    /** Progresses the game one turn. */
    public void progress() {
        // would it be faster to loop through and reset all elements to false? probably not for large arrays?
        b = new boolean[a.length][a[0].length];

        // loop through every single element in the board
        for (int y = 0; y < a.length; y++) {
            for (int x = 0; x < a[y].length; x++) {
                final int numNeighbours = countNeighbours(x, y);

                // 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the next generation.
                if (numNeighbours == 3) {
                    b[y][x] = true;
                }
                // 2. A live cell with exactly 2 neighbours is alive in the next generation.
                else if (a[y][x] == true && numNeighbours == 2) {
                    b[y][x] = true;
                }
                // 3. All other cells are dead in the next generation.
                else {
                    continue; // just being explicit
                }
            }
        }

        // swap the arrays
        a = b;
        b = null;
        iteration++;
    }

    /**
     * Check how many live neighbours we have for a given cell
     * @param x x coord for the cell
     * @param y y coord for the cell
     * @return the number of neighbour cells that are alive
     */
    private int countNeighbours(int x, int y) {
        int count = 0;

        // check if we need to wrap around
        // if y==0 we can't decrement further, so wrap around to other extreme of array
        final int top = y == 0 ? a.length-1 : y-1;
        // if y==a.length-1 we can't increment, so wrap around to 0
        final int bottom = y == a.length-1 ? 0 : y+1;

        // if x==0 then we can't decrement further, so wrap around to other extreme of array
        final int left = x == 0 ? a[0].length-1 : x-1;
        // if x==a[0].length-1 we can't increment, so wrap around to 0
        final int right = x == a[0].length-1 ? 0 : x+1;

        // check all the neighbours
        count += a[top   ][left ] ? 1 : 0;
        count += a[top   ][x    ] ? 1 : 0;
        count += a[top   ][right] ? 1 : 0;
        count += a[y     ][left ] ? 1 : 0;
        // we don't do a[y][x] because it's the cell we're testing
        count += a[y     ][right] ? 1 : 0;
        count += a[bottom][left ] ? 1 : 0;
        count += a[bottom][x    ] ? 1 : 0;
        count += a[bottom][right] ? 1 : 0;
        return count;
    }

    /**
     * Set a cell as dead or alive in the A array.
     * @param x x coordinate of cell
     * @param y y coordinate of the cell
     * @param alive status to set
     */
    public void setCell(final int x, final int y, final boolean alive) {
        a[y][x] = alive;
    }

    /**
     * Return the status of the given cell
     * @param x x coordinate of the cell
     * @param y y coordinate of the cell
     * @return the status of the cell
     */
    public boolean getCell(final int x, final int y) {
        return a[y][x];
    }

    /**
     * Count the number of cells that are alive.
     * @return the number of cells that are alive
     */
    public Object count() {
        int count = 0;

        // loop through every single element in the board
        for (int y = 0; y < a.length; y++) {
            for (int x = 0; x < a[y].length; x++) {
                if (a[y][x]) {
                    count++;
                }
            }
        }
        return count;
    }

    /**
     * Get which iteration we are on.
     * @return which iteration we are on
     */
    public int getIteration() {
        return iteration;
    }

    public String toString() {
        // initialise SB to x*y*2+y chars to prevent needing to increase the size
        final StringBuilder sb = new StringBuilder(a.length*a[0].length*2 + a.length);
        for (int y = 0; y < a.length; y++) {
            for (int x = 0; x < a[y].length; x++) {
                sb.append(a[y][x] ? "■" : "□").append(" ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}
