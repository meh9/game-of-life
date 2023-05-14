package com.zakalwe.gameoflife.collection;

import java.util.Map;
import java.util.TreeMap;

import com.zakalwe.gameoflife.GameOfLife;

/**
 * The actual Conway's Game of Life implementation.
 * 
 * The intent it that this implementation will use collections in order to not
 * have a finite universe and other associated limitations.
 */
public class GameOfLifeCollection implements GameOfLife {

    private final int generation = 0;
    private final Map<RowCol, Boolean> a = new TreeMap<>();

    /** Default constructor */
    public GameOfLifeCollection() {
    }

    /** Progresses the game one turn. */
    @Override
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
    @Override
    public void setCell(final int row, final int col, final boolean alive) {
        a.put(new RowCol(row, col), alive);
    }

    /**
     * Return the status of the given cell
     * 
     * @param row y coordinate of the cell
     * @param col x coordinate of the cell
     * @return the status of the cell
     */
    @Override
    public boolean getCell(final int row, final int col) {
        return a.get(new RowCol(row, col));
    }

    /**
     * Count the number of cells that are alive.
     * 
     * @return the number of cells that are alive
     */
    @Override
    public int countLiveCells() {
        final int count = -1;

        // TODO: implement
        return count;
    }

    /**
     * Get which iteration we are on.
     * 
     * @return which iteration we are on
     */
    @Override
    public int getGeneration() {
        return generation;
    }

    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder();
        sb.append("Generation: ").append(generation);
        sb.append(", Live cells: ").append(countLiveCells());
        sb.append(", All cells: ").append(countAllCells()); // .append("\n");
        // for (int row = 0; row < a.length; row++) {
        // for (int col = 0; col < a[row].length; col++) {
        // sb.append(a[row][col] ? "■ " : "□ ");
        // }
        // sb.append("\n");
        // }
        return sb.toString();
    }

    @Override
    public int countAllCells() {
        return a.size();
    }

    /* package-private */ record RowCol(int row, int col) implements Comparable<RowCol> {

        @Override
        public int compareTo(final RowCol o) {
            final int rowDiff = row - o.row;
            if (rowDiff == 0) {
                return col - o.col;
            }
            return rowDiff;
        }
    }
}
