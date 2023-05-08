package com.zakalwe.gameoflife.arrays;

// TODO: add test class

/**
 * The actual Conway's Game of Life implementation.
 */
public class GameOfLifeArrays {

    private boolean[][] a;
    private boolean[][] b;

    
    /** Initialise arrays 
     * @param x width of the board
     * @param y height of the board
     */
    public GameOfLifeArrays(final int x, final int y) {
        a = new boolean[x][y];
        b = new boolean[x][y];
    }

    /** Progresses the game one turn. */
    public void progress() {
        // TODO: would it be faster to loop through and reset all elements to false? probably not for large arrays?
        b = new boolean[a.length][a[0].length];

        // TODO: fix wrap around!
        for (int x = 1; x < a.length-1; x++) {
            for (int y = 1; y < a[x].length-1; y++) {
                final int numNeighbours = countNeighbours(x, y);

                // if a cell has less than 2 neighbours then it starves to death
                if (numNeighbours < 2) {
                    b[x][y] = false;
                } 
                // if a cell has more than 5 neighbours it starves to death
                else if (numNeighbours > 3) {
                    b[x][y] = false;
                }
                // otherwise it is alive
                else {
                    b[x][y] = true;
                }
            }
        }

        // swap the arrays
        final boolean[][] tmp = a;
        a = b;
        b = tmp;
    }


    private int countNeighbours(int x, int y) {
        int count = 0;
        count += a[x-1][y-1] ? 1 : 0;
        count += a[x  ][y-1] ? 1 : 0;
        count += a[x+1][y-1] ? 1 : 0;
        count += a[x-1][y  ] ? 1 : 0;
        // we don't do a[x][y] because it's the cell we're testing
        count += a[x+1][y  ] ? 1 : 0;
        count += a[x-1][y+1] ? 1 : 0;
        count += a[x  ][y+1] ? 1 : 0;
        count += a[x+1][y+1] ? 1 : 0;
        return count;
    }

    /**
     * Set a cell as dead or alive in the A array.
     * @param x x coordinate of cell
     * @param y y coordinate of the cell
     * @param alive status to set
     */
    public void setCell(final int x, final int y, final boolean alive) {
        a[x][y] = alive;
    }

    /** Print the A array to the console */
    public void printA() {
        System.out.println("========================================");
        for (int x = 0; x < a.length; x++) {
            for (int y = 0; y < a[x].length; y++) {
                System.out.print(a[x][y] ? "X" : " ");
            }
            System.out.println();
        }
        System.out.println("========================================");
    }
}
