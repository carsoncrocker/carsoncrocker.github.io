276-vertex 5-chromatic unit-distance graph in the hyperbolic plane: files to check it yourself
=============================================================================================

Claim: 276 points in the hyperbolic plane. Two points are joined when their hyperbolic distance is
exactly d, the distance of Exoo and Ismailescu (arXiv:2303.06801): cosh d = c/(1-c), where c is the
largest real root of 16c^4 + 8c^3 - 12c^2 - 2c + 1, so d = 1.3750335088... The graph has 1025 edges, is
faithful (no other pair is at distance d), has chromatic number 5, and is vertex-critical.

Files
  hyp_EI_276.json                 exact coordinates in the number field Q(c) (hyperboloid model), 30-digit
                                  hyperboloid and Poincare-disk decimals, the distance, and the edge list
  hyp_EI_276_edges.txt            the edge list alone: first line "n m", then 0-based pairs "a b"
  cert2_hyp_276.cnf               the "is it 4-colorable?" question as a SAT formula
  cert2_hyp_276.drat              a DRAT proof that the formula has no solution (binary format)
  cert2_hyp_276_colourings.json   for every vertex v, a proper 4-coloring of the graph with v deleted
  verify_standalone.py            the checker

Run
  pip install python-flint python-sat      (python-sat is optional)
  python verify_standalone.py hyp_EI_276.json

It takes under a minute. The last line should read:
  ALL CHECKS PASS (20 checks, ..s)

If drat-trim (https://github.com/marijnheule/drat-trim) is on your PATH the checker uses it for the
proof; otherwise it uses its built-in pure-Python DRAT checker (py_drat_check, standard library only).

What it checks: the field and the distance (c isolated exactly, cosh d = c/(1-c) is a root of the
stated polynomial); every point is on the hyperboloid; every listed edge is at distance exactly d and
every other pair is not (all 37,950 pairs, exact arithmetic); the points are distinct; the SAT formula
is rebuilt from the edge list and the DRAT proof refutes it, so there is no proper 4-coloring; every
vertex-deleted graph has a stored proper 4-coloring; negative controls are rejected.

The full package, with a DOI, will also contain a picture of the graph in the Poincare disk and the
logs of a separately written verifier.
