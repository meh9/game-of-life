package com.zakalwe.gameoflife.collection;

import static org.testng.Assert.assertEquals;

import java.util.Iterator;
import java.util.Set;
import java.util.TreeSet;

import org.testng.annotations.Test;

import com.zakalwe.gameoflife.collection.GameOfLifeCollection.RowCol;

public class GameOfLifeCollectionTest {

    private final RowCol minusOneZero = new RowCol(-1, 0);
    private final RowCol zeroZero = new RowCol(0, 0);
    private final RowCol zeroZero2nd = new RowCol(0, 0);
    private final RowCol zeroOne = new RowCol(0, 1);
    private final RowCol oneZero = new RowCol(1, 0);
    private final RowCol oneOne = new RowCol(1, 1);

    /** Test the natural ordering of RowCol. */
    @Test
    public void rowColOrdering() {
        assertEquals(minusOneZero.compareTo(zeroZero), -1);
        assertEquals(zeroZero.compareTo(minusOneZero), 1);
        assertEquals(zeroZero.compareTo(zeroZero2nd), 0);
        assertEquals(zeroZero.compareTo(zeroOne), -1);
        assertEquals(zeroOne.compareTo(oneZero), -1);
        assertEquals(oneOne.compareTo(oneZero), 1);
    }

    /** Test natural ordering in a TreeSet. */
    @Test
    public void treeSetOrdering() {
        final Set<RowCol> set = new TreeSet<>();
        set.add(zeroOne);
        set.add(oneOne);
        set.add(zeroZero);
        set.add(oneZero);
        set.add(minusOneZero);
        final Iterator<RowCol> it = set.iterator();

        assertEquals(it.next(), minusOneZero);
        assertEquals(it.next(), zeroZero);
        assertEquals(it.next(), zeroOne);
        assertEquals(it.next(), oneZero);
        assertEquals(it.next(), oneOne);
    }

}
