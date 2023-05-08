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
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(10, 10);

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
