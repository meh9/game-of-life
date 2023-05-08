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

        // loop through every single element in the board
        for (int x = 0; x < a.length; x++) {
            for (int y = 0; y < a[x].length; y++) {
                final int numNeighbours = countNeighbours(x, y);

                // 1. Any live cell with two or three live neighbours survives.
                if (a[x][y] == true) {
                    if (numNeighbours == 2 || numNeighbours == 3) {
                        b[x][y] = true;
                    }
                }
                // 2. Any dead cell with three live neighbours becomes a live cell.
                else if (numNeighbours == 3) {
                    b[x][y] = true;
                }
                // 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
            }
        }

        // swap the arrays
        final boolean[][] tmp = a;
        a = b;
        b = tmp;
    }

    /**
     * Check how many live neighbours we have for a given cell
     * @param x x coord for the cell
     * @param y y coord for the cell
     * @return the number of neighbour cells that are alive
     */
    private int countNeighbours(int x, int y) {
        int count = 0;

        // check if we need to wrap around
        // if x==0 then we can't decrement further, so wrap around to other extreme of array
        final int left = x == 0 ? a.length-1 : x-1;
        // if x==a.length-1 we can't increment, so wrap around to 0
        final int right = x == a.length-1 ? 0 : x+1;
        // if y==0 we can't decrement further, so wrap around to other extreme of array
        final int top = y == 0 ? a[0].length-1 : y-1;
        // if y==a[0].length-1 we can't increment, so wrap around to 0
        final int bottom = y == a[0].length-1 ? 0 : y+1;

        // check all the neighbours
        count += a[left][top] ? 1 : 0;
        count += a[x  ][top] ? 1 : 0;
        count += a[right][top] ? 1 : 0;
        count += a[left][y  ] ? 1 : 0;
        // we don't do a[x][y] because it's the cell we're testing
        count += a[right][y  ] ? 1 : 0;
        count += a[left][bottom] ? 1 : 0;
        count += a[x  ][bottom] ? 1 : 0;
        count += a[right][bottom] ? 1 : 0;
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
