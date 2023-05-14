package com.zakalwe.gameoflife;

public interface GameOfLife {

    /** Progresses the game one turn. */
    public void progress();

    /**
     * Set a cell as dead or alive in the A array.
     * 
     * @param row   y coordinate of the cell
     * @param col   x coordinate of cell
     * @param alive status to set
     */
    public void setCell(int row, int col, boolean alive);

    /**
     * Return the status of the given cell
     * 
     * @param row y coordinate of the cell
     * @param col x coordinate of the cell
     * @return the status of the cell
     */
    public boolean getCell(int row, int col);

    /**
     * Count the number of cells that are alive.
     * 
     * @return the number of cells that are alive
     */
    public int countLiveCells();

    /**
     * Count the total number of cells that we are tracking - dead or alive.
     * 
     * @return the number of cells
     */
    public int countAllCells();

    /**
     * Get which iteration we are on.
     * 
     * @return which iteration we are on
     */
    public int getGeneration();

    @Override
    public String toString();

}