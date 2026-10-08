228-vertex 5-chromatic unit-distance graph on a sphere: files to check it yourself
=================================================================================

Claim: 228 points on the sphere of radius r, r^2 = (5+sqrt5)/8 (r = cos(pi/10), about 0.95106, the
circumradius of the icosahedron with edges of length 1). Two points are joined when their straight-line
(chord) distance in R^3 is exactly 1. The graph has 910 edges, is faithful (no other pair is at chord
distance 1), has chromatic number 5, and is vertex-critical (deleting any vertex makes it 4-colorable).

Files
  sphere_228.json              exact coordinates in a number field of degree 8, 30-digit decimals, the field,
                               and the edge list
  sphere_228_edges.txt         the edge list alone: first line "n m", then 0-based pairs "a b"
  sphere_228_minpolys.json     the minimal polynomial over Q of every coordinate
  sphere_228.cnf               the "is it 4-colorable?" question as a SAT formula
  sphere_228.drat              a DRAT proof that the formula has no solution (binary format)
  sphere_228_colourings.json   for every vertex v, a proper 4-coloring of the graph with v deleted
  verify_standalone.py         the checker

Run
  pip install python-flint python-sat      (python-sat is optional)
  python verify_standalone.py

It takes about 1 minute. The last line should read:
  ALL CHECKS PASS: sphere_228: n = 228, edges = 910, chromatic number 5 (..s)

If drat-trim (https://github.com/marijnheule/drat-trim) is on your PATH, or given with
--drat-trim /path/to/drat-trim, the checker uses it for the proof. Otherwise it uses its built-in
pure-Python DRAT checker (py_drat_check, standard library only), which takes under a minute.
The checker also writes its output to log_verify_228.txt.

What it checks: every point is exactly on the sphere; for all 25,878 pairs, the pairs at chord
exactly 1 are exactly the listed edges (exact arithmetic in the number field, which is shown to be a
field with a real embedding); the stored decimals and minimal polynomials match; the SAT formula is
rebuilt from the edge list and the DRAT proof refutes it, so there is no proper 4-coloring; every
vertex-deleted graph has a stored proper 4-coloring; negative controls are rejected.

The full package, with a DOI, will also contain a second 231-vertex example, the provenance of the
construction and the logs of a separately written verifier.
