package com.zakalwe.gameoflife;

import com.zakalwe.gameoflife.collection.GameOfLifeCollection;

/**
 * Main class to run Conway's Game of Life.
 */
public final class App {

    /** Do nothing constructor */
    public App() {
    }

    /**
     * Main
     * 
     * @param args arguments
     */
    public static final void main(final String[] args) {
        final int rows = 10;
        final int cols = 10;
        final GameOfLife gameOfLife = new GameOfLifeCollection();

        gameOfLife.setCell(0, 0, true);
        gameOfLife.setCell(5, 0, true);
        gameOfLife.setCell(0, 5, true);
        gameOfLife.setCell(1, 0, true);
        gameOfLife.setCell(rows - 1, 0, true);
        gameOfLife.setCell(0, cols - 1, true);

        gameOfLife.setCell(5, 5, true);
        gameOfLife.setCell(6, 5, true);
        gameOfLife.setCell(5, 6, true);
        gameOfLife.setCell(6, 6, true);
        gameOfLife.setCell(5, 7, true);
        System.out.println(gameOfLife + "\n");

        gameOfLife.progress();
        System.out.println(gameOfLife + "\n");

        gameOfLife.progress();
        System.out.println(gameOfLife + "\n");
    }
}
