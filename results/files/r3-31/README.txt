31-vertex triangle-free 5-chromatic unit-distance graph in R^3: files to check it yourself
=========================================================================================

Claim: 31 points in R^3 whose unit-distance graph has 96 edges, is triangle-free, has chromatic
number 5, and is 5-critical. "Unit-distance graph" means: two points are joined exactly when they are
at distance 1 (the graph is faithful: no other pair of the 31 points is at distance 1).

Files
  coordinates_31.txt   the 31 points (70 significant digits; the coordinates written as 0 are exactly 0)
  edges_31.txt         the 96 edges
  check_31.py          the checker (Python 3.8+ and mpmath; everything else is the standard library)

Run
  pip install mpmath
  python check_31.py

It takes about 25 seconds. The last line should read:
  PASS: 31 points in R^3, 96 edges of length exactly 1, faithful, triangle-free, chromatic number 5, 5-critical  (..s)

What it checks (details at the top of check_31.py)
  - the edge list is the Mycielskian of the 15-vertex graph on points 0..14;
  - an exact identity in Q(sqrt5) shows that the "shadow" points -phi*x_i are exactly at distance 1 from
    the neighbors of point i and from the origin;
  - a Krawczyk interval test (320-bit interval arithmetic) proves that an exact solution of the 42
    sphere and edge equations lies within 1e-40 of the listed coordinates, so all 96 edges have length
    exactly 1;
  - every non-adjacent pair is at distance different from 1 (smallest |d - 1| about 0.0064), and no
    two points coincide;
  - the graph is triangle-free;
  - an exhaustive backtracking search finds no proper 4-coloring; a proper 5-coloring is found;
  - deleting any vertex or any edge makes it 4-colorable;
  - negative controls (a point moved by 1e-6, a deleted edge, a wrong radius) are rejected.

Exact algebraic coordinates exist but live in a number field of degree 704; they will be in the full
package with a DOI, together with the original certificate, a separately written verifier, SAT
proofs and the note. This folder is a small self-contained check.
