package com.zakalwe.gameoflife;

import com.zakalwe.gameoflife.arrays.GameOfLifeArrays;

/**
 * Main class to run Conway's Game of Life.
 */
public final class App {

    /** Do nothing constructor */
    public App() {}


    //TODO: add command line argument processing
    /**
     * Main
     * @param args arguments
     */
    public static final void main(String[] args) {
        final int xmax = 10;
        final int ymax = 10;
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(xmax, ymax);

        gameOfLifeArrays.setCell(0, 0, true);
        gameOfLifeArrays.setCell(0, 5, true);
        gameOfLifeArrays.setCell(5, 0, true);
        gameOfLifeArrays.setCell(0, 1, true);
        gameOfLifeArrays.setCell(0, ymax-1, true);
        gameOfLifeArrays.setCell(xmax-1, 0, true);

        gameOfLifeArrays.setCell(5, 5, true);
        gameOfLifeArrays.setCell(5, 6, true);
        gameOfLifeArrays.setCell(6, 5, true);
        gameOfLifeArrays.setCell(6, 6, true);
        gameOfLifeArrays.setCell(7, 5, true);
        gameOfLifeArrays.printA();

        gameOfLifeArrays.progress();
        gameOfLifeArrays.printA();
    }
}
