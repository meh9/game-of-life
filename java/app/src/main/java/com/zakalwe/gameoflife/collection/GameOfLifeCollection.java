package com.zakalwe.gameoflife.collection;

import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

import com.zakalwe.gameoflife.GameOfLife;

/**
 * The actual Conway's Game of Life implementation.
 * 
 * The intent it that this implementation will use collections in order to not
 * have a finite universe and other associated limitations.
 */
public class GameOfLifeCollection implements GameOfLife {

    private enum Neighbours {
        TWO,
        THREE,
        NOT_TWO_OR_THREE
    }

    private int generation = 0;
    private Map<RowCol, Boolean> a = new TreeMap<>();
    private int minRow = Integer.MAX_VALUE;
    private int maxRow = Integer.MIN_VALUE;
    private int minCol = Integer.MAX_VALUE;
    private int maxCol = Integer.MIN_VALUE;

    /** Default constructor */
    public GameOfLifeCollection() {
    }

    /** Progresses the game one turn. */
    @Override
    public void progress() {
        minRow = Integer.MAX_VALUE;
        maxRow = Integer.MIN_VALUE;
        minCol = Integer.MAX_VALUE;
        maxCol = Integer.MIN_VALUE;
        final Map<RowCol, Boolean> b = new TreeMap<>();

        for (final Entry<RowCol, Boolean> entry : a.entrySet()) {
            final RowCol rowCol = entry.getKey();
            final Boolean alive = entry.getValue();
            final Neighbours neighbours = countNeighbours(rowCol);

            switch (neighbours) {
                // 2. A live cell with exactly 2 neighbours is alive in the next generation.
                case TWO:
                    if (alive) {
                        setCell(rowCol, true, b);
                    }
                    break;

                // 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the next
                // generation.
                case THREE:
                    setCell(rowCol, true, b);
                    break;

                // 3. All other cells are dead in the next generation.
                default:
                    // do nothing
            }
        }

        // finalise the generation
        a = b;
        generation++;
    }

    private Neighbours countNeighbours(final RowCol rowCol) {
        int count = 0;
        final RowCol[] keys = rowCol.computeNeighbours();
        for (int i = 0; i < keys.length; i++) {
            if (getCell(keys[i])) {
                count++;
                // short circuit when over 4
                if (count >= 4) {
                    return Neighbours.NOT_TWO_OR_THREE;
                }
            }
        }

        return switch (count) {
            case 2 -> Neighbours.TWO;
            case 3 -> Neighbours.THREE;
            default -> Neighbours.NOT_TWO_OR_THREE;
        };
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
        setCell(new RowCol(row, col), alive, a);
    }

    private void setCell(final RowCol rowCol, final boolean alive, final Map<RowCol, Boolean> m) {
        if (alive) {
            // add the actual live cell
            m.put(rowCol, alive);
            // add all the neighbouring dead cells if the do not exist already
            for (final RowCol rc : rowCol.computeNeighbours()) {
                setCell(rc, false, m);
            }
        } else {
            // only add dead cells if there is no cell at that coord already, dead or alive
            m.putIfAbsent(rowCol, false);
        }
        // make sure we track min/max bounds
        minRow = rowCol.row < minRow ? rowCol.row : minRow;
        maxRow = rowCol.row > maxRow ? rowCol.row : maxRow;
        minCol = rowCol.col < minCol ? rowCol.col : minCol;
        maxCol = rowCol.col > maxCol ? rowCol.col : maxCol;
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
        return getCell(new RowCol(row, col));
    }

    private boolean getCell(final RowCol rowCol) {
        final Boolean b = a.get(rowCol);
        // if there is no cell then the cell is dead - this is a common occurrence
        if (b == null) {
            return false;
        } else {
            return b;
        }
    }

    /**
     * Count the number of cells that are alive.
     * 
     * @return the number of cells that are alive
     */
    @Override
    public int countLiveCells() {
        int count = 0;
        for (final boolean live : a.values()) {
            if (live) {
                count++;
            }
        }
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
        sb.append(", All cells: ").append(countAllCells());
        sb.append(", 2D array equiv. elements: ").append((maxRow - minRow + 1) * (maxCol - minCol + 1)).append("\n");

        for (int row = minRow; row <= maxRow; row++) {
            for (int col = minCol; col <= maxCol; col++) {
                final Boolean b = a.get(new RowCol(row, col));
                if (b == null) {
                    sb.append("  ");
                } else {
                    sb.append(b ? "■ " : "□ ");
                }
            }
            sb.append("\n");
        }
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

        private RowCol[] computeNeighbours() {
            final RowCol[] r = new RowCol[8];
            final int top = row - 1;
            final int bottom = row + 1;
            final int left = col - 1;
            final int right = col + 1;
            r[0] = new RowCol(top, left);
            r[1] = new RowCol(top, col);
            r[2] = new RowCol(top, right);
            r[3] = new RowCol(row, right);
            r[4] = new RowCol(bottom, right);
            r[5] = new RowCol(bottom, col);
            r[6] = new RowCol(bottom, left);
            r[7] = new RowCol(row, left);
            return r;
        }
    }
}
