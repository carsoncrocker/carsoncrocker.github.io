"""Check the 31-vertex triangle-free 5-chromatic unit-distance graph in R^3.

usage:   python check_31.py          (needs Python 3.8+ and mpmath: pip install mpmath)

Reads coordinates_31.txt and edges_31.txt from this folder and checks:

 1. Structure. 31 points and 96 edges. Points 0..14 form a graph G; point 15+i is the "shadow" of
    point i; point 30 is the apex. The edge list is exactly the Mycielskian of G: the edges of G, the
    edges (15+i)-j and i-(15+j) for every edge i-j of G, and (15+i)-30 for every i.
 2. Exact identity (exact arithmetic in Q(sqrt5), standard library only). Put R = 1/phi = (sqrt5-1)/2
    and t = 1 - 1/R^2. If |x| = |y| = R, then
        |t x - y|^2 - 1 = t (|x - y|^2 - 1) + (R^2 (1 - t)^2 + t - 1)
    (expand |t x - y|^2 and use 2 x.y = 2 R^2 - |x - y|^2). The program checks exactly that
    R^2 (1 - t)^2 + t - 1 = 0, that t = -phi, and that t^2 R^2 = 1. So if base points i and j are at
    distance exactly 1, the shadow t x_i is at distance exactly 1 from x_j, and every shadow is at
    distance exactly 1 from the origin.
 3. Existence (rigorous interval arithmetic, mpmath.iv at 320 bits). The base points satisfy 42
    equations in 42 unknowns: |x_i|^2 = R^2 for i = 0..14 and |x_i - x_j|^2 = 1 for the 27 edges of G
    (x0 = y0 = 0 for point 0 and y = 0 for point 1 fix the rotation). The Krawczyk test on the box of
    radius 1e-40 around the listed coordinates proves that an exact solution lies in that box.
    With 2., every one of the 96 edges has length exactly 1.
 4. Faithful (interval arithmetic). With the base points enclosed in that box, the shadows enclosed as
    t x_i and the apex at 0, every one of the 369 non-adjacent pairs has a distance interval that does
    not contain 1, and no two points coincide. The listed coordinates are within 1e-40 of the
    enclosures.
 5. Triangle-free (direct check of every edge).
 6. Not 4-colorable: an exhaustive backtracking search (standard library, no SAT solver) finds no
    proper 4-coloring. A proper 5-coloring is found and checked, so the chromatic number is 5.
 7. 5-critical: deleting any one vertex or any one edge leaves a 4-colorable graph (each coloring
    is found and checked).
 8. Negative controls: a base point moved by 1e-6 must make step 3 fail; a deleted edge must make
    step 1 fail; R = 0.62 must make step 2 fail.

The last line says PASS or FAIL.
"""
import os, sys, time, itertools
from fractions import Fraction as Fr
from mpmath import mp, iv

HERE = os.path.dirname(os.path.abspath(__file__))
PREC = 320
mp.prec = PREC
iv.prec = PREC
EPS = mp.mpf("1e-40")
RESULTS = {}


def log(*a):
    print(*a, flush=True)


def check(name, ok, detail=""):
    RESULTS[name] = bool(ok)
    log(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))


def read_rows(name):
    with open(os.path.join(HERE, name)) as f:
        return [l.split() for l in f if l.strip() and not l.startswith("#")]


def lo(x): return mp.mpf(x.a)
def hi(x): return mp.mpf(x.b)
def finite(x): return mp.isfinite(lo(x)) and mp.isfinite(hi(x))


# ------------------------------------------------------------------ 1. structure
def mycielski_ok(E):
    G = {e for e in E if max(e) < 15}
    want = set(G)
    for i, j in G:
        want.add(tuple(sorted((15 + i, j))))
        want.add(tuple(sorted((i, 15 + j))))
    for i in range(15):
        want.add((15 + i, 30))
    return want == set(E), sorted(G)


# ------------------------------------------------------------------ 2. exact identity in Q(sqrt5)
class Q5:
    """a + b*sqrt5 with rational a, b."""
    def __init__(self, a, b=0): self.a, self.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    def __sub__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        return Q5(s.a / n, -s.b / n)
    def __eq__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s.a == o.a and s.b == o.b
    def __repr__(s): return f"{s.a} + {s.b}*sqrt5"


def identities(R):
    R2 = R * R
    t = Q5(1) - R2.inv()
    phi = Q5(Fr(1, 2), Fr(1, 2))
    bracket = R2 * (Q5(1) - t) * (Q5(1) - t) + t - Q5(1)
    return bracket == Q5(0), t == Q5(0) - phi, t * t * R2 == Q5(1), t


# ------------------------------------------------------------------ 3. Krawczyk
def krawczyk(P, Gedges, R_iv):
    """P: list of 15 base points (lists of 3 mp.mpf). Returns (ok, info, enclosures)."""
    fixed = {(0, 0), (0, 1), (1, 1)}
    var = [(i, k) for i in range(15) for k in range(3) if (i, k) not in fixed]
    vidx = {vk: n for n, vk in enumerate(var)}
    nv = len(var)
    neq = 15 + len(Gedges)
    if nv != neq:
        return False, f"system not square ({neq} equations, {nv} unknowns)", None
    if any(P[i][k] != 0 for i, k in fixed):
        return False, "gauge coordinates are not exactly 0", None
    R2 = R_iv * R_iv

    def pts(vec):
        return [[vec[vidx[(i, k)]] if (i, k) in vidx else iv.mpf(0) for k in range(3)] for i in range(15)]

    def F(vec):
        Q = pts(vec)
        out = [Q[i][0] * Q[i][0] + Q[i][1] * Q[i][1] + Q[i][2] * Q[i][2] - R2 for i in range(15)]
        for i, j in Gedges:
            d = [Q[i][k] - Q[j][k] for k in range(3)]
            out.append(d[0] * d[0] + d[1] * d[1] + d[2] * d[2] - 1)
        return out

    def J(Q, zero):
        rows = []
        for i in range(15):
            rows.append([(vidx[(i, k)], 2 * Q[i][k]) for k in range(3) if (i, k) in vidx])
        for i, j in Gedges:
            r = []
            for k in range(3):
                d = Q[i][k] - Q[j][k]
                if (i, k) in vidx: r.append((vidx[(i, k)], 2 * d))
                if (j, k) in vidx: r.append((vidx[(j, k)], -2 * d))
            rows.append(r)
        return rows

    m = [P[i][k] for i, k in var]
    # approximate inverse Y of the Jacobian at the centre (ordinary multiprecision, not rigorous; it need not be)
    Qm = [[m[vidx[(i, k)]] if (i, k) in vidx else mp.mpf(0) for k in range(3)] for i in range(15)]
    Jm = mp.matrix(nv, nv)
    for r, row in enumerate(J(Qm, mp.mpf(0))):
        for c, val in row:
            Jm[r, c] += val
    Y = mp.inverse(Jm)
    Yi = [[iv.mpf(Y[a, b]) for b in range(nv)] for a in range(nv)]
    mi = [iv.mpf(x) for x in m]
    Fm = F(mi)
    X = [iv.mpf([x - EPS, x + EPS]) for x in m]
    YJ = [[iv.mpf(0)] * nv for _ in range(nv)]
    for j, row in enumerate(J(pts(X), iv.mpf(0))):
        for l, val in row:
            for a in range(nv):
                YJ[a][l] = YJ[a][l] + Yi[a][j] * val
    K = []
    for a in range(nv):
        s = mi[a] - sum((Yi[a][j] * Fm[j] for j in range(nv)), iv.mpf(0))
        acc = iv.mpf(0)
        for l in range(nv):
            acc = acc + ((iv.mpf(1) if a == l else iv.mpf(0)) - YJ[a][l]) * (X[l] - mi[l])
        K.append(s + acc)
    if not all(finite(k) for k in K):
        return False, "non-finite interval", None
    inside = all(lo(K[t]) > lo(X[t]) and hi(K[t]) < hi(X[t]) for t in range(nv))
    off = max(max(abs(lo(K[t]) - m[t]), abs(hi(K[t]) - m[t])) for t in range(nv))
    info = f"{neq} equations, {nv} unknowns; K(X) inside X: {inside}; max |K(X) - centre| <= {mp.nstr(off, 3)}"
    if not inside:
        return False, info, None
    enc = [iv.mpf([max(lo(K[t]), lo(X[t])), min(hi(K[t]), hi(X[t]))]) for t in range(nv)]
    return True, info, pts(enc)


# ------------------------------------------------------------------ 6./7. colorings by backtracking
def color(n, E, k, skip_vertex=None):
    """Return a proper k-coloring of the graph (minus skip_vertex) as a list, or None if none exists.
    Exhaustive: vertices in a fixed order, colors tried in order, and a vertex may only open the next
    unused color (this only removes renamings of the colors, so the search stays complete)."""
    adj = [set() for _ in range(n)]
    for a, b in E:
        if skip_vertex not in (a, b):
            adj[a].add(b); adj[b].add(a)
    verts = [v for v in range(n) if v != skip_vertex]
    order = [max(verts, key=lambda v: len(adj[v]))]
    rest = set(verts) - set(order)
    while rest:  # next: the vertex with most already-ordered neighbours, then highest degree
        v = max(sorted(rest), key=lambda v: (len(adj[v] & set(order)), len(adj[v])))
        order.append(v); rest.discard(v)
    col = [-1] * n

    def go(p, used):
        if p == len(order):
            return True
        v = order[p]
        bad = {col[u] for u in adj[v]}
        for c in range(min(k, used + 1)):
            if c not in bad:
                col[v] = c
                if go(p + 1, max(used, c + 1)):
                    return True
        col[v] = -1
        return False

    sys.setrecursionlimit(10000)
    return col if go(0, 0) else None


def proper(col, E, skip=None):
    return all(col[a] >= 0 and col[b] >= 0 and col[a] != col[b] for a, b in E if skip not in (a, b))


# ------------------------------------------------------------------ main
def geometry(coords, E, R, R_iv, label="data"):
    """Steps 1-4 on given data. Returns dict of booleans (used for the real run and the controls)."""
    out = {}
    out["structure"], G = mycielski_ok(E)
    a, b, c, t = identities(R)
    out["identity"] = a and b and c
    P = [[mp.mpf(s) for s in p] for p in coords]
    ok, info, enc = krawczyk(P[:15], G, R_iv)
    out["krawczyk"] = ok
    out["krawczyk_info"] = info
    out["G"] = G
    out["t"] = t
    out["enc"] = enc
    return out


def main():
    T0 = time.time()
    rows = read_rows("coordinates_31.txt")
    coords = [r[1:4] for r in rows]
    E = sorted(tuple(sorted((int(a), int(b)))) for a, b in read_rows("edges_31.txt"))
    n = len(coords)
    log(f"check_31.py: {n} points, {len(E)} edges; mpmath {mp.prec} bits")
    check("0 counts and edge list well-formed",
          n == 31 and len(E) == 96 and len(set(E)) == 96 and all(0 <= a < b < n for a, b in E)
          and [int(r[0]) for r in rows] == list(range(31)))

    R = Q5(Fr(-1, 2), Fr(1, 2))                       # 1/phi = (sqrt5 - 1)/2
    R_iv = (iv.sqrt(iv.mpf(5)) - 1) / 2
    g = geometry(coords, E, R, R_iv)
    check("1 edge list = Mycielskian of the 15-vertex graph G on points 0..14", g["structure"],
          f"G has {len(g['G'])} edges")
    check("2 exact identity in Q(sqrt5): shadows -phi*x_i are exactly unit from the neighbours of i and from 0",
          g["identity"], f"t = 1 - 1/R^2 = {g['t']}")
    check("3 Krawczyk: an exact solution of the 42 sphere and edge equations lies within 1e-40 of the data",
          g["krawczyk"], g["krawczyk_info"])
    if not g["krawczyk"]:
        log("FAIL"); sys.exit(1)

    # ---- 4. enclose all 31 points, check every pair
    tI = 1 - 1 / (R_iv * R_iv)
    X = {i: g["enc"][i] for i in range(15)}
    for i in range(15):
        X[15 + i] = [tI * x for x in X[i]]
    X[30] = [iv.mpf(0)] * 3
    dev = max(max(abs(lo(iv.mpf(coords[p][k]) - X[p][k])), abs(hi(iv.mpf(coords[p][k]) - X[p][k])))
              for p in range(31) for k in range(3))
    Es = set(E)
    minmarg, worst, minsep, bad_non, bad_edge = None, None, None, [], []
    for i, j in itertools.combinations(range(31), 2):
        d = [X[i][k] - X[j][k] for k in range(3)]
        dist = iv.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
        if minsep is None or lo(dist) < minsep: minsep = lo(dist)
        if (i, j) in Es:
            if not (lo(dist) <= 1 <= hi(dist)): bad_edge.append((i, j))
        else:
            if lo(dist) > 1: mg = lo(dist) - 1
            elif hi(dist) < 1: mg = 1 - hi(dist)
            else: bad_non.append((i, j)); continue
            if minmarg is None or mg < minmarg: minmarg, worst = mg, (i, j)
    check("4a the listed coordinates are within 1e-40 of the certified enclosures", dev < EPS, f"max deviation {mp.nstr(dev, 3)}")
    check("4b every edge interval contains 1 (consistency; exactness is steps 2-3)", not bad_edge, f"failing {bad_edge[:5]}")
    check("4c faithful: no non-adjacent pair is at distance 1", not bad_non,
          f"{465 - 96} non-edges, smallest |d - 1| >= {mp.nstr(minmarg, 8)} at pair {worst}")
    check("4d all 31 points distinct", minsep > 0, f"smallest distance >= {mp.nstr(minsep, 8)}")

    # ---- 5. triangle-free
    adj = {v: set() for v in range(31)}
    for a, b in E: adj[a].add(b); adj[b].add(a)
    tri = [(a, b) for a, b in E if adj[a] & adj[b]]
    check("5 triangle-free", not tri, f"{len(tri)} edges with a common neighbour")

    # ---- 6. chromatic number 5
    t1 = time.time()
    c4 = color(31, E, 4)
    check("6a no proper 4-coloring exists (exhaustive backtracking)", c4 is None, f"{time.time() - t1:.1f}s")
    c5 = color(31, E, 5)
    check("6b a proper 5-coloring exists and is checked", c5 is not None and proper(c5, E), f"coloring {c5}")

    # ---- 7. 5-critical
    t1 = time.time()
    vok = sum(1 for v in range(31) if (lambda c: c is not None and proper(c, E, v))(color(31, E, 4, skip_vertex=v)))
    eok = 0
    for e in E:
        E2 = [f for f in E if f != e]
        c = color(31, E2, 4)
        eok += c is not None and proper(c, E2)
    check("7 5-critical: every vertex-deleted and every edge-deleted subgraph is 4-colorable", vok == 31 and eok == 96,
          f"{vok}/31 vertex deletions, {eok}/96 edge deletions ({time.time() - t1:.1f}s)")

    # ---- 8. negative controls
    bad = [list(p) for p in coords]
    bad[5][0] = mp.nstr(mp.mpf(bad[5][0]) + mp.mpf("1e-6"), 70)
    c1 = not geometry(bad, E, R, R_iv)["krawczyk"]
    c2 = not mycielski_ok([e for e in E if e != (0, 5)])[0]
    c3 = not identities(Q5(Fr(62, 100)))[0] or not identities(Q5(Fr(62, 100)))[1]
    check("8 negative controls rejected (point moved 1e-6; edge 0-5 deleted; R = 0.62)", c1 and c2 and c3,
          f"moved point rejected {c1}, deleted edge rejected {c2}, R = 0.62 rejected {c3}")

    allok = all(RESULTS.values())
    log(f"\n{'PASS' if allok else 'FAIL'}: 31 points in R^3, 96 edges of length exactly 1, faithful, triangle-free, "
        f"chromatic number 5, 5-critical  ({time.time() - T0:.0f}s)" if allok else
        f"\nFAIL: {[k for k, v in RESULTS.items() if not v]}  ({time.time() - T0:.0f}s)")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
