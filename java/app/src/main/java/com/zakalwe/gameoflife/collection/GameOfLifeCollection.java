package com.zakalwe.gameoflife.collection;

/**
 * The actual Conway's Game of Life implementation.
 * 
 * The intent it that this implementation will use collections in order to not
 * have a finite universe and other associated limitations.
 */
public class GameOfLifeCollection {

    private int iteration = 0;

    /**
     * Default constructor
     */
    public GameOfLifeCollection() {
    }

    /** Progresses the game one turn. */
    public void progress() {
        // TODO: implement
        /*
         * final int numNeighbours = countNeighbours(row, col);
         * // 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the next
         * // generation.
         * if (numNeighbours == 3) {
         * b[row][col] = true;
         * }
         * // 2. A live cell with exactly 2 neighbours is alive in the next generation.
         * else if (a[row][col] == true && numNeighbours == 2) {
         * b[row][col] = true;
         * }
         * // 3. All other cells are dead in the next generation.
         * else {
         * continue; // just being explicit
         * }
         */
    }

    /**
     * Set a cell as dead or alive in the A array.
     * 
     * @param row   y coordinate of the cell
     * @param col   x coordinate of cell
     * @param alive status to set
     */
    public void setCell(final int row, final int col, final boolean alive) {
        // TODO: implement
    }

    /**
     * Return the status of the given cell
     * 
     * @param row y coordinate of the cell
     * @param col x coordinate of the cell
     * @return the status of the cell
     */
    public boolean getCell(final int row, final int col) {
        // TODO: implement
        return false;
    }

    /**
     * Count the number of cells that are alive.
     * 
     * @return the number of cells that are alive
     */
    public Object count() {
        int count = 0;

        // TODO: implement
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
        // TODO: implement
        return null;
    }
}
