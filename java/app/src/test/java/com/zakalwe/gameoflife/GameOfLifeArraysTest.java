/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package com.zakalwe.gameoflife;

import org.testng.annotations.*;
import com.zakalwe.gameoflife.arrays.GameOfLifeArrays;
import static org.testng.Assert.*;

public class GameOfLifeArraysTest {

    // Rules:
    // 1. Any live cell with two or three live neighbours survives.
    // 2. Any dead cell with three live neighbours becomes a live cell.
    // 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

    /** Test a simple glider that wraps around the universe. */
    @Test public void gliderWraparound() {
        System.out.println("gliderWraparound():");
        final int rows = 12;
        final int cols = 15;
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(rows, cols);

        // create the glider
        gameOfLifeArrays.setCell(0, 1, true);
        gameOfLifeArrays.setCell(1, 2, true);
        gameOfLifeArrays.setCell(2, 0, true);
        gameOfLifeArrays.setCell(2, 1, true);
        gameOfLifeArrays.setCell(2, 2, true);
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 5);

        for (int i = 0; i < 10000; i++) {
            gameOfLifeArrays.progress();
            assertEquals(gameOfLifeArrays.count(), 5);
        }
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertTrue(gameOfLifeArrays.getCell(4, 11), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(5, 12), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(6, 10), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(6, 11), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(6, 12), "should be alive");
    }

    /** Test that dead cells with 3 neighbours becomes live. */
    @Test public void deadWithThreeNeighboursComeAlive() {
        System.out.println("deadWithThreeNeighboursComeAlive():");
        final int rows = 7;
        final int cols = 6;
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(rows, cols);

        // set a line of 3 live cells
        gameOfLifeArrays.setCell(1, 1, true);
        gameOfLifeArrays.setCell(1, 2, true);
        gameOfLifeArrays.setCell(1, 3, true);

        // set a line of 2 live cells
        gameOfLifeArrays.setCell(4, 1, true);
        gameOfLifeArrays.setCell(4, 2, true);

        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 5);

        // line of 3 spawns 1 above and 1 below, middle stays alive because it has 2 neighbours, left and right dies because only a 1 neighbour
        // line of 2 only has 1 neighbour each and both die
        gameOfLifeArrays.progress();
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 3);

        // check new vertical line of 3 is alive
        assertTrue(gameOfLifeArrays.getCell(0, 2), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(1, 2), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(2, 2), "should be alive");

        // check "corners" did not come alive
        assertFalse(gameOfLifeArrays.getCell(0, 1), "should be dead");
        assertFalse(gameOfLifeArrays.getCell(0, 3), "should be dead");
        assertFalse(gameOfLifeArrays.getCell(2, 1), "should be dead");
        assertFalse(gameOfLifeArrays.getCell(2, 3), "should be dead");

        // check the line of 2 died
        assertFalse(gameOfLifeArrays.getCell(4, 1), "should be dead");
        assertFalse(gameOfLifeArrays.getCell(4, 2), "should be dead");

        // next iteration the line should flip horizontal again
        gameOfLifeArrays.progress();
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 3, "should be a a line of 3");
        assertTrue(gameOfLifeArrays.getCell(1, 1), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(1, 2), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(1, 3), "should be alive");

        // the line should keep flipping infinitely, flip an odd number of times and it should change orientation
        for (int i = 0; i < 101; i++) {
            gameOfLifeArrays.progress();
        }
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        // check line is vertical
        assertTrue(gameOfLifeArrays.getCell(0, 2), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(1, 2), "should be alive");
        assertTrue(gameOfLifeArrays.getCell(2, 2), "should be alive");
        assertEquals(gameOfLifeArrays.count(), 3, "should be a a line of 3");
    }


    /** Test that a 2x2 square of cells is stable - each cell has 3 neighbours. */
    @Test public void aliveWithThreeNeighboursSurvive() {
        System.out.println("aliveWithThreeNeighboursSurvive():");
        final int rows = 4;
        final int cols = 6;
        final GameOfLifeArrays gameOfLifeArrays = new GameOfLifeArrays(rows, cols);

        // set a 2x2 square of live cells
        gameOfLifeArrays.setCell(1, 1, true);
        gameOfLifeArrays.setCell(1, 2, true);
        gameOfLifeArrays.setCell(2, 1, true);
        gameOfLifeArrays.setCell(2, 2, true);
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 4);

        gameOfLifeArrays.progress();
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 4);

        // check row above square
        assertFalse(gameOfLifeArrays.getCell(0, 0));
        assertFalse(gameOfLifeArrays.getCell(0, 1));
        assertFalse(gameOfLifeArrays.getCell(0, 2));
        assertFalse(gameOfLifeArrays.getCell(0, 3));

        // check row below square
        assertFalse(gameOfLifeArrays.getCell(3, 0));
        assertFalse(gameOfLifeArrays.getCell(3, 1));
        assertFalse(gameOfLifeArrays.getCell(3, 2));
        assertFalse(gameOfLifeArrays.getCell(3, 3));

        // check left and right of square
        assertFalse(gameOfLifeArrays.getCell(1, 0));
        assertFalse(gameOfLifeArrays.getCell(2, 0));
        assertFalse(gameOfLifeArrays.getCell(1, 3));
        assertFalse(gameOfLifeArrays.getCell(2, 3));

        // 2x2 square of live cells is stable and should never change
        for (int i = 0; i < 101; i++){ 
            gameOfLifeArrays.progress();
            assertEquals(gameOfLifeArrays.count(), 4);
        }
        System.out.println("Iteration: " + gameOfLifeArrays.getIteration() + ":\n" + gameOfLifeArrays + "\n");
        assertEquals(gameOfLifeArrays.count(), 4);
    }
}
