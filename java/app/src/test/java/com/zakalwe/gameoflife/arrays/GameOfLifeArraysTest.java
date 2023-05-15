package com.zakalwe.gameoflife.arrays;

import static org.testng.Assert.assertEquals;
import static org.testng.Assert.assertTrue;

import org.testng.annotations.Test;

import com.zakalwe.gameoflife.GameOfLife;

public class GameOfLifeArraysTest {
    /**
     * Test a simple glider that wraps around the universe.
     * 
     * This is only tested for the GameOfLifeArrays version since the Collections
     * based version has an unbounded universe.
     */
    @Test
    public void gliderWraparound() {
        System.out.println("gliderWraparound():");
        final int rows = 12;
        final int cols = 15;
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(rows, cols);
        gliderWraparoundTest(gameOfLifeArrays);
    }

    private void gliderWraparoundTest(final GameOfLife gameOfLife) {
        // create the glider
        gameOfLife.setCell(0, 1, true);
        gameOfLife.setCell(1, 2, true);
        gameOfLife.setCell(2, 0, true);
        gameOfLife.setCell(2, 1, true);
        gameOfLife.setCell(2, 2, true);
        System.out.println(gameOfLife + "\n");
        assertEquals(gameOfLife.countLiveCells(), 5);

        for (int i = 0; i < 10000; i++) {
            gameOfLife.progress();
            assertEquals(gameOfLife.countLiveCells(), 5);
        }
        System.out.println(gameOfLife + "\n");
        assertTrue(gameOfLife.getCell(4, 11), "should be alive");
        assertTrue(gameOfLife.getCell(5, 12), "should be alive");
        assertTrue(gameOfLife.getCell(6, 10), "should be alive");
        assertTrue(gameOfLife.getCell(6, 11), "should be alive");
        assertTrue(gameOfLife.getCell(6, 12), "should be alive");
    }
}
