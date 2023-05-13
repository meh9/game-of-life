package com.zakalwe.gameoflife.arrays;

/**
 * The actual Conway's Game of Life implementation.
 * 
 * This implementation uses a fixed sized (double array) universe where cells
 * wrap around the edges.
 */
public class GameOfLifeArrays {

    private boolean[][] a;
    private boolean[][] b;
    private int iteration = 0;

    /**
     * Initialise arrays
     * 
     * @param rows height of the board
     * @param cols width of the board
     */
    public GameOfLifeArrays(final int rows, final int cols) {
        a = new boolean[rows][cols];
    }

    /** Progresses the game one turn. */
    public void progress() {
        // would it be faster to loop through and reset all elements to false? probably
        // not for large arrays?
        b = new boolean[a.length][a[0].length];

        // loop through every single element in the board
        for (int row = 0; row < a.length; row++) {
            for (int col = 0; col < a[row].length; col++) {
                final int numNeighbours = countNeighbours(row, col);

                // 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the next
                // generation.
                if (numNeighbours == 3) {
                    b[row][col] = true;
                }
                // 2. A live cell with exactly 2 neighbours is alive in the next generation.
                else if (a[row][col] == true && numNeighbours == 2) {
                    b[row][col] = true;
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
     * 
     * @param row y coord for the cell
     * @param col x coord for the cell
     * @return the number of neighbour cells that are alive
     */
    private int countNeighbours(final int row, final int col) {
        int count = 0;

        // check if we need to wrap around
        // if y==0 we can't decrement further, so wrap around to other extreme of array
        final int top = row == 0 ? a.length - 1 : row - 1;
        // if y==a.length-1 we can't increment, so wrap around to 0
        final int bottom = row == a.length - 1 ? 0 : row + 1;

        // if x==0 then we can't decrement further, so wrap around to other extreme of
        // array
        final int left = col == 0 ? a[0].length - 1 : col - 1;
        // if x==a[0].length-1 we can't increment, so wrap around to 0
        final int right = col == a[0].length - 1 ? 0 : col + 1;

        // check all the neighbours
        count += a[top][left] ? 1 : 0;
        count += a[top][col] ? 1 : 0;
        count += a[top][right] ? 1 : 0;
        count += a[row][left] ? 1 : 0;
        // we don't do a[y][x] because it's the cell we're testing
        count += a[row][right] ? 1 : 0;
        count += a[bottom][left] ? 1 : 0;
        count += a[bottom][col] ? 1 : 0;
        count += a[bottom][right] ? 1 : 0;
        return count;
    }

    /**
     * Set a cell as dead or alive in the A array.
     * 
     * @param row   y coordinate of the cell
     * @param col   x coordinate of cell
     * @param alive status to set
     */
    public void setCell(final int row, final int col, final boolean alive) {
        a[row][col] = alive;
    }

    /**
     * Return the status of the given cell
     * 
     * @param row y coordinate of the cell
     * @param col x coordinate of the cell
     * @return the status of the cell
     */
    public boolean getCell(final int row, final int col) {
        return a[row][col];
    }

    /**
     * Count the number of cells that are alive.
     * 
     * @return the number of cells that are alive
     */
    public Object count() {
        int count = 0;

        // loop through every single element in the board
        for (int row = 0; row < a.length; row++) {
            for (int col = 0; col < a[row].length; col++) {
                if (a[row][col]) {
                    count++;
                }
            }
        }
        return count;
    }

    /**
     * Get which iteration we are on.
     * 
     * @return which iteration we are on
     */
    public int getIteration() {
        return iteration;
    }

    public String toString() {
        // initialise SB to x*y*2+y chars to prevent needing to increase the size
        final StringBuilder sb = new StringBuilder(a.length * a[0].length * 2 + a.length);
        for (int row = 0; row < a.length; row++) {
            for (int col = 0; col < a[row].length; col++) {
                sb.append(a[row][col] ? "■" : "□").append(" ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}
