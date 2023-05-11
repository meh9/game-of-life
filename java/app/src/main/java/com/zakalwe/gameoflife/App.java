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
        final int rows = 10;
        final int cols = 10;
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(rows, cols);

        gameOfLifeArrays.setCell(0, 0, true);
        gameOfLifeArrays.setCell(5, 0, true);
        gameOfLifeArrays.setCell(0, 5, true);
        gameOfLifeArrays.setCell(1, 0, true);
        gameOfLifeArrays.setCell(rows-1, 0, true);
        gameOfLifeArrays.setCell(0, cols-1, true);

        gameOfLifeArrays.setCell(5, 5, true);
        gameOfLifeArrays.setCell(6, 5, true);
        gameOfLifeArrays.setCell(5, 6, true);
        gameOfLifeArrays.setCell(6, 6, true);
        gameOfLifeArrays.setCell(5, 7, true);
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");

        gameOfLifeArrays.progress();
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");

        gameOfLifeArrays.progress();
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
    }
}
