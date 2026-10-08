r"""Standalone verifier for the faithful 5-chromatic unit-distance graphs on the sphere S^2(r), r^2 = (5+sqrt5)/8.

Requires: Python 3.9+, python-flint (exact rationals/matrices/polynomials, ball arithmetic), python-sat (optional
sanity re-solve). The DRAT proof is checked with drat-trim if it is on PATH (or given with --drat-trim PATH);
otherwise with the pure-Python forward checker py_drat_check below (standard library, about a minute).
It reads only the files in this folder:
    sphere_228.json, sphere_228.cnf / .drat / _colourings.json, sphere_228_minpolys.json

usage:  python verify_standalone.py
        python verify_standalone.py --no-drat
        python verify_standalone.py --drat-trim /path/to/drat-trim

Arithmetic: the coordinates lie in F = Q(w1, w2, w3), w1^2 = 5, w2^2 = d2 in Q(w1), w3^2 = d3 in Q(w1, w2).
This program does NOT use the nested tower arithmetic of the prover: it writes every element as a vector of 8
rationals on the monomial basis w1^i w2^j w3^k (i, j, k in {0,1}), builds the multiplication table by reducing
monomial products with the three relations, and does all exact work with flint fmpq matrices.

Checks:
 (a) EXACT GEOMETRY
   a1 F is a field of degree 8: the characteristic polynomial of a primitive element is irreducible of degree 8
      (so the 8-dim commutative algebra equals Q(theta), a field); d2 > 0 and d3 > 0 in the real embedding
      w1, w2, w3 > 0 (rigorous ball arithmetic), so that embedding F -> R exists and is injective.
   a2 |X|^2 = r^2 exactly for every vertex.
   a3 for ALL pairs X != Y: X.Y computed exactly; |X-Y|^2 = 2 r^2 - 2 X.Y, so |X-Y|^2 = 1 iff X.Y = r^2 - 1/2 and
      X = Y iff X.Y = r^2.  The set of exact unit pairs must equal the edge list (faithful), and no pair coincides.
      Since F -> R is injective, "!= in F" means "!= in R".
   a4 every stored 30-decimal coordinate is within 1e-29 of the exact coordinate's real value (ball arithmetic).
 (b) CNF: the 4-colouring CNF is regenerated from the edge list (+ triangle colour fixing) and compared with the
      certificate CNF byte by byte (after CRLF -> LF) and as a clause multiset.
 (c) drat-trim (or, if it is not installed, the built-in py_drat_check) checks the DRAT refutation of that CNF
      (=> G is not 4-colourable).
 (d) every stored colouring of G - v is a proper 4-colouring of G - v, for every v (=> vertex-critical, chi(G) = 5).
 (e) minimal polynomials: each stored P is primitive, irreducible over Q, P(alpha) = 0 EXACTLY in F, |P(alpha)| <
      1e-25 in ball arithmetic, the stored real root matches the coordinate, and it isolates exactly one root of P.
 (f) sanity: python-sat Glucose 4 re-solves the regenerated CNF (expected UNSAT; not a proof, (c) is the proof).
 (g) negative controls: a coordinate perturbed by 1e-6, and an edge deleted from the list, must FAIL (a2)/(a3).
"""
import sys, os, json, time, hashlib, subprocess, platform
import flint

Q = flint.fmpq
HERE = os.path.dirname(os.path.abspath(__file__))
flint.ctx.prec = 400
ARB = flint.arb


class Log:
    def __init__(self, path): self.f = open(path, "w", newline="\n")
    def __call__(self, *a):
        s = " ".join(str(x) for x in a); print(s, flush=True); self.f.write(s + "\n"); self.f.flush()


def py_drat_check(cnf_path, drat_path):
    """Pure-Python forward DRAT checker (standard library only; slower than drat-trim, same verdict).
    Every added lemma must be RUP (or RAT on its first literal) with respect to the clauses present at that
    point; deletions of non-unit clauses are applied, deletions of unit clauses are ignored (as drat-trim does;
    keeping a clause never makes a check weaker). Returns (verified, message)."""
    cls = []
    for line in open(cnf_path):
        t = line.split()
        if not t or t[0] in ("c", "p"): continue
        cls.append([int(x) for x in t[:-1]])
    raw = open(drat_path, "rb").read()
    steps = []
    if raw[:1] in (b"a", b"d") and any(b > 127 or b < 32 and b not in (9, 10, 13) for b in raw[:200]):
        i = 0
        while i < len(raw):
            kind = raw[i]; i += 1; lits = []
            while True:
                u = 0; sh = 0
                while True:
                    b = raw[i]; i += 1; u |= (b & 127) << sh; sh += 7
                    if b < 128: break
                if u == 0: break
                lits.append(-(u >> 1) if u & 1 else u >> 1)
            steps.append((kind == 100, lits))  # 100 = 'd'
    else:
        for line in raw.decode().splitlines():
            t = line.split()
            if not t or t[0] == "c": continue
            dele = t[0] == "d"
            steps.append((dele, [int(x) for x in (t[1:] if dele else t)[:-1]]))
    nv = max([abs(l) for c in cls for l in c] + [abs(l) for _, c in steps for l in c] + [1])
    val = [0] * (2 * nv + 2)                       # val[l] for literal index l
    def ix(l): return 2 * l if l > 0 else -2 * l + 1
    watch = [[] for _ in range(2 * nv + 2)]
    store = []; alive = []; units = {}; where = {}
    def add(c):
        k = len(store); store.append(list(c)); alive.append(True)
        where.setdefault(tuple(sorted(c)), []).append(k)
        if len(c) == 1: units[c[0]] = units.get(c[0], 0) + 1
        elif len(c) >= 2: watch[ix(c[0])].append(k); watch[ix(c[1])].append(k)
        return k
    def rup(neg):
        trail = []
        def setlit(l):
            if val[ix(l)] == 1: return True
            if val[ix(-l)] == 1: return False
            val[ix(l)] = 1; trail.append(l); return True
        ok = True
        for l in list(units) + neg:
            if not setlit(l): ok = False; break
        p = 0
        while ok and p < len(trail):
            f = -trail[p]; p += 1                    # literal f just became false
            wl = watch[ix(f)]; j = 0
            while j < len(wl):
                k = wl[j]
                if not alive[k]: wl[j] = wl[-1]; wl.pop(); continue
                c = store[k]
                if c[0] == f: c[0], c[1] = c[1], c[0]
                if val[ix(c[0])] == 1: j += 1; continue
                for q in range(2, len(c)):
                    if val[ix(-c[q])] != 1:
                        c[1], c[q] = c[q], c[1]; watch[ix(c[1])].append(k); wl[j] = wl[-1]; wl.pop(); break
                else:
                    if not setlit(c[0]): ok = False; break
                    j += 1
        for l in trail: val[ix(l)] = 0
        return not ok                                # True = conflict = RUP
    for c in cls:
        if not c: return True, "empty clause in CNF"
        add(c)
    added = rat = 0
    for dele, c in steps:
        if dele:
            if len(c) == 1: continue
            ks = [k for k in where.get(tuple(sorted(c)), []) if alive[k]]
            if ks: alive[ks[-1]] = False; where[tuple(sorted(c))].remove(ks[-1])
            continue
        added += 1
        if not rup([-l for l in c]):
            if not c: return False, f"empty clause at lemma {added} is not RUP"
            p = c[0]; ok = True
            for k in range(len(store)):
                d = store[k]
                if alive[k] and -p in d:
                    r = set(c) | (set(d) - {-p})
                    if any(-x in r for x in r): continue
                    if not rup([-x for x in r]): ok = False; break
            if not ok: return False, f"lemma {added} {c[:8]} is neither RUP nor RAT"
            rat += 1
        if not c: return True, f"VERIFIED: {added} lemmas checked ({rat} by RAT), empty clause derived"
        add(c)
    if rup([]): return True, f"VERIFIED: {added} lemmas checked ({rat} by RAT), conflict by unit propagation"
    return False, f"proof ends without a conflict ({added} lemmas checked)"


def main():
    N = 228
    nodrat = "--no-drat" in sys.argv
    native = sys.argv[sys.argv.index("--drat-trim") + 1] if "--drat-trim" in sys.argv else None
    gpath = os.path.join(HERE, f"sphere_{N}.json")
    cnfp = os.path.join(HERE, f"sphere_{N}.cnf")
    dratp = os.path.join(HERE, f"sphere_{N}.drat")
    colp = os.path.join(HERE, f"sphere_{N}_colourings.json")
    mpp = os.path.join(HERE, f"sphere_{N}_minpolys.json")
    log = Log(os.path.join(HERE, f"log_verify_{N}.txt"))
    T0 = time.time(); RES = {}

    def chk(name, ok, detail):
        RES[name] = ok
        log(f"[{'PASS' if ok is True else ('NOT RUN' if ok is None else 'FAIL')}] {name}: {detail}")

    log(f"verify_standalone.py on sphere_{N}   {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"python {platform.python_version()}, python-flint {flint.__version__}, {platform.platform()}")
    for p in (gpath, cnfp, dratp, colp, mpp):
        log(f"  input {os.path.relpath(p, HERE)}  sha256 {hashlib.sha256(open(p, 'rb').read()).hexdigest()}")
    G = json.load(open(gpath))
    n = G["n"]; E = [tuple(e) for e in G["edges"]]
    assert n == len(G["vertices"]) == N and G["m"] == len(E)

    # ================================================================ flat algebra of dimension 8
    def flat(x, k):  # nested [a, b] (a + b w_k) -> list of 2^k fmpq; basis index bit (k-1) <-> w_k
        if k == 0:
            p, q = x.split("/"); return [Q(int(p), int(q))]
        return flat(x[0], k - 1) + flat(x[1], k - 1)
    ds = G["field"]["d"]
    assert len(ds) == 3 and ds[0] == "5/1"
    dflat = [flat(d, k) for k, d in enumerate(ds)]                  # d_k as vector over basis of F_{k-1}
    def mono(i): return (i & 1, (i >> 1) & 1, (i >> 2) & 1)          # exponents of w1, w2, w3
    def idx(e): return e[0] + 2 * e[1] + 4 * e[2]

    def reduce(poly):  # poly: dict exps -> fmpq, exps unrestricted; reduce with w_k^2 = d_k (triangular: w3, w2, w1)
        out = {}; work = list(poly.items())
        while work:
            e, c = work.pop()
            if c == 0: continue
            for kk in (2, 1, 0):
                if e[kk] >= 2:
                    base = list(e); base[kk] -= 2
                    for j, dc in enumerate(dflat[kk]):             # d_k is a combination of monomials in w_1..w_{k-1}
                        if dc != 0:
                            ej = mono(j); work.append((tuple(base[t] + (ej[t] if t < kk else 0) for t in range(3)), c * dc))
                    break
            else:
                out[e] = out.get(e, Q(0)) + c
        v = [Q(0)] * 8
        for e, c in out.items(): v[idx(e)] += c
        return v

    TAB = [[reduce({tuple(a + b for a, b in zip(mono(i), mono(j))): Q(1)}) for j in range(8)] for i in range(8)]
    # left-multiplication matrices of the basis elements: L_i[r][j] = coefficient of b_r in b_i b_j
    L = [flint.fmpq_mat(8, 8, [TAB[i][j][r] for r in range(8) for j in range(8)]) for i in range(8)]
    def M(x):  # multiplication matrix of x (8-vector)
        acc = flint.fmpq_mat(8, 8)
        for i in range(8):
            if x[i] != 0: acc = acc + L[i] * x[i]
        return acc
    def col(v): return flint.fmpq_mat(8, 1, v)
    def vec(m): return [m[r, 0] for r in range(8)]
    # commutativity/associativity spot check of the table (it is a quotient of a polynomial ring, so this must hold)
    comm = all(TAB[i][j] == TAB[j][i] for i in range(8) for j in range(8))
    assoc = all(vec(L[i] * (L[j] * col(TAB[0][k]))) == vec(M(TAB[i][j]) * col(TAB[0][k])) for i in range(8) for j in range(8) for k in range(8))

    # ---------------------------------------------------------------- (a1) field + real embedding
    prim = None
    for name, th in (("w3", [Q(0)] * 4 + [Q(1)] + [Q(0)] * 3), ("w1+w2+w3", [Q(0), Q(1), Q(1), Q(0), Q(1), Q(0), Q(0), Q(0)])):
        cp = M(th).charpoly()
        c, facs = cp.factor()
        if len(facs) == 1 and facs[0][1] == 1 and facs[0][0].degree() == 8:
            prim = (name, cp); break
    w1 = ARB(5).sqrt()
    d2 = ARB(dflat[1][0]) + ARB(dflat[1][1]) * w1
    w2 = d2.sqrt() if d2 > 0 else None
    d3 = sum((ARB(dflat[2][j]) * (w1 if j & 1 else 1) * (w2 if j & 2 else 1) for j in range(4)), ARB(0)) if w2 is not None else None
    w3 = d3.sqrt() if (d3 is not None and d3 > 0) else None
    real_ok = w3 is not None
    chk("a1 F = Q(w1,w2,w3) is a field of degree 8 with real embedding w1,w2,w3 > 0",
        prim is not None and comm and assoc and real_ok,
        f"primitive element {prim[0] if prim else None}, char. poly irreducible of degree 8: {prim[1] if prim else None}; "
        f"table commutative {comm}, associative {assoc}; d2 = {d2.str(12, radius=False)} > 0, "
        f"d3 = {d3.str(12, radius=False) if d3 is not None else None} > 0 (rigorous balls): {real_ok}")
    BV = [(w1 if i & 1 else ARB(1)) * (w2 if i & 2 else ARB(1)) * (w3 if i & 4 else ARB(1)) for i in range(8)]
    def real(x): return sum((ARB(x[i]) * BV[i] for i in range(8) if x[i] != 0), ARB(0))

    # ---------------------------------------------------------------- (a2) sphere
    X = [[flat(c, 3) for c in v["exact"]] for v in G["vertices"]]
    MX = [[M(c) for c in P] for P in X]
    r2 = flat([["5/8", "1/8"], ["0/1", "0/1"]], 2) + [Q(0)] * 4       # (5 + sqrt5)/8 lifted to F
    assert G["r2"]["exact_F1"] == ["5/8", "1/8"]
    c0 = [r2[0] - Q(1, 2)] + r2[1:]                                    # r^2 - 1/2
    def dot(a, b):
        s = MX[a][0] * col(X[b][0]) + MX[a][1] * col(X[b][1]) + MX[a][2] * col(X[b][2]); return vec(s)
    ons = sum(1 for a in range(n) if dot(a, a) == r2)
    chk("a2 |X|^2 = r^2 = (5+sqrt5)/8 exactly for every vertex", ons == n, f"{ons}/{n}")

    # ---------------------------------------------------------------- (a3) all pairs
    t = time.time()
    def all_unit_pairs(Xs, MXs):
        nn = len(Xs)
        A = flint.fmpq_mat(8 * nn, 24, [MXs[a][tt][r, j] for a in range(nn) for r in range(8) for tt in range(3) for j in range(8)])
        Y = flint.fmpq_mat(24, nn, [Xs[b][tt][j] for tt in range(3) for j in range(8) for b in range(nn)])
        Gm = (A * Y).entries()                                          # row 8a+r, column b
        unit, coinc = [], 0
        for a in range(nn):
            rows = [Gm[(8 * a + r) * nn:(8 * a + r + 1) * nn] for r in range(8)]
            for b in range(a + 1, nn):
                g = [rows[r][b] for r in range(8)]
                if g == c0: unit.append((a, b))
                elif g == r2: coinc += 1
        return unit, coinc
    unit, coinc = all_unit_pairs(X, MX)
    Es = sorted(set(E)); wellformed = len(Es) == len(E) and all(0 <= a < b < n for a, b in E)
    keys = len(set(tuple(tuple(c) for c in P) for P in X))
    chk("a3 exact unit pairs == edge list (faithful); points distinct", wellformed and unit == Es and coinc == 0 and keys == n,
        f"{n * (n - 1) // 2} pairs computed exactly ({time.time() - t:.1f}s): {len(unit)} exact unit pairs; edge list has "
        f"{len(E)} edges (well-formed, no duplicates: {wellformed}); identical: {unit == Es}; coincident pairs {coinc}; "
        f"distinct coordinate vectors {keys}/{n}")

    # ---------------------------------------------------------------- (a4) decimals
    tol = ARB("1e-29"); bad = 0
    for a in range(n):
        for tt in range(3):
            if not abs(real(X[a][tt]) - ARB(G["vertices"][a]["decimal"][tt])) < tol: bad += 1
    wd = [w1, w2, w3]; badw = sum(1 for k in range(3) if not abs(wd[k] - ARB(G["field"]["w_decimal"][k])) < tol)
    chk("a4 stored 30-decimal coordinates match the exact values (within 1e-29, ball arithmetic)", bad == 0 and badw == 0,
        f"{3 * n - bad}/{3 * n} coordinates, {3 - badw}/3 generators")

    # ---------------------------------------------------------------- (b) CNF
    tri = G["symmetry_breaking_triangle"]
    cl = [[4 * i + c + 1 for c in range(4)] for i in range(n)]
    cl += [[-(4 * a + c + 1), -(4 * b + c + 1)] for a, b in E for c in range(4)]
    triok = True
    if tri:
        triok = all(tuple(sorted(p)) in set(E) for p in ((tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])))
        cl += [[4 * tri[0] + 1], [4 * tri[1] + 2], [4 * tri[2] + 3]]
    regen = (f"p cnf {4 * n} {len(cl)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cl)).encode()
    raw = open(cnfp, "rb").read()
    byte_eq = raw.replace(b"\r\n", b"\n") == regen
    ends = "CRLF" if b"\r\n" in raw else "LF"
    lines = raw.decode().split("\n"); hdr = lines[0].split()
    cert_cl = sorted(tuple(int(x) for x in l.split()[:-1]) for l in lines[1:] if l.strip())
    set_eq = hdr[:4] == ["p", "cnf", str(4 * n), str(len(cl))] and cert_cl == sorted(tuple(c) for c in cl)
    chk("b  certificate CNF == 4-colouring CNF regenerated from the edge list"
        + (f" + triangle {tuple(tri)} fixed to colours 1,2,3" if tri else ""),
        byte_eq and set_eq and triok,
        f"{4 * n} vars, {len(cl)} clauses (at-least-one colour per vertex; endpoints of each edge differ in each colour; "
        f"3 unit clauses); byte-identical after CRLF->LF: {byte_eq}; raw bytes identical: {raw == regen} "
        f"(certificate file line ends: {ends}); clause multiset identical: {set_eq}; "
        f"triangle is a triangle of G: {triok}. (Fixing a triangle's colours is WLOG: permute colours.)")

    # ---------------------------------------------------------------- (c) drat-trim
    if nodrat:
        chk("c  drat-trim verifies the DRAT refutation", None, "skipped (--no-drat)")
    else:
        import shutil
        t = time.time()
        if not (native or shutil.which("drat-trim")):
            okd, msg = py_drat_check(cnfp, dratp)
            chk("c  DRAT refutation verified by the built-in pure-Python checker (drat-trim not found) (=> G is not 4-colourable)",
                okd, f"{msg} in {time.time() - t:.1f}s")
        else:
            cmd = [native or "drat-trim", cnfp, dratp]
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=7200).stdout
                st = [l for l in out.splitlines() if l.startswith("s ")]
                info = [l for l in out.splitlines() if "lemmas in core" in l or "RAT lemmas" in l]
                chk("c  drat-trim verifies the DRAT refutation (=> G is not 4-colourable)", bool(st) and st[-1] == "s VERIFIED",
                    f"{' '.join(cmd[-3:])}: '{st[-1] if st else 'NO STATUS'}' in {time.time() - t:.1f}s; {info}")
            except (OSError, subprocess.SubprocessError) as ex:
                chk("c  drat-trim verifies the DRAT refutation", None, f"drat-trim not available ({ex!r})")


    # ---------------------------------------------------------------- (d) vertex-criticality
    cols = json.load(open(colp)); good = 0
    for v in range(n):
        s = cols.get(str(v))
        if s is None or len(s) != n or s[v] != "-": continue
        if all(s[u] in "0123" for u in range(n) if u != v) and all(s[a] != s[b] for a, b in E if v not in (a, b)): good += 1
    chk("d  every G - v has a stored proper 4-colouring (vertex-critical; with (c): chi(G) = 5)", good == n and len(cols) == n,
        f"{good}/{n} colourings proper")

    # ---------------------------------------------------------------- (e) minimal polynomials
    MP = json.load(open(mpp)); recs = MP["records"]; t = time.time()
    names = "xyz"; seen = {}; fails = []; hist = {}; worst = 0.0
    covered = set((r["vertex"], r["coord"]) for r in recs)
    for r in recs:
        a, tt = r["vertex"], names.index(r["coord"])
        co = [int(c) for c in r["coeffs_low_to_high"]]; P = flint.fmpz_poly(co)
        d = P.degree(); hist[d] = hist.get(d, 0) + 1
        key = (tuple(co), tuple(X[a][tt]), r["real_root"])
        if key in seen:
            if not seen[key]: fails.append((a, r["coord"], "see earlier"))
            continue
        ok = True; why = []
        if P.content() != 1 or co[-1] <= 0 or d != r["degree"] or 8 % d != 0: ok = False; why.append("normalisation/degree")
        c, facs = P.factor()
        if not (len(facs) == 1 and facs[0][1] == 1 and facs[0][0].degree() == d): ok = False; why.append("not irreducible")
        acc = [Q(0)] * 8                                                # Horner, exactly in F
        Ma = MX[a][tt]
        for cc in reversed(co):
            acc = vec(Ma * col(acc)); acc[0] += cc
        if any(x != 0 for x in acc): ok = False; why.append("P(alpha) != 0 exactly")
        al = real(X[a][tt]); pv = abs(P(al)); worst = max(worst, float(pv.upper()))
        if not pv < ARB("1e-25"): ok = False; why.append("|P(alpha)| not < 1e-25")
        if r["real_root"] != G["vertices"][a]["decimal"][tt] or not abs(al - ARB(r["real_root"])) < ARB("1e-29"):
            ok = False; why.append("real_root mismatch")
        near = sum(1 for z, m in P.complex_roots() if abs(z - flint.acb(ARB(r["real_root"]))) < ARB("1e-20")) if d > 0 else 0
        if near != 1: ok = False; why.append(f"{near} roots within 1e-20 of the decimal")
        seen[key] = ok
        if not ok: fails.append((a, r["coord"], why))
    allcov = covered == set((a, names[tt]) for a in range(n) for tt in range(3)) and len(recs) == 3 * n
    chk("e  minimal polynomials: primitive, irreducible over Q, P(alpha) = 0 exactly in F, |P(alpha)| < 1e-25, "
        "stored real root isolates alpha", not fails and allcov,
        f"{len(recs)} coordinate records ({len(seen)} distinct), all {3 * n} coordinates covered: {allcov}; degree histogram "
        f"{dict(sorted(hist.items()))}; max |P(alpha)| upper bound {worst:.3g}; failures {fails[:5]} ({time.time() - t:.1f}s)")

    # ---------------------------------------------------------------- (f) sanity re-solve
    try:
        from pysat.solvers import Glucose4
        t = time.time(); s = Glucose4(bootstrap_with=cl); r_ = s.solve(); s.delete()
        chk("f  sanity: Glucose 4 (python-sat) on the regenerated CNF is UNSAT (not a proof; (c) is)", r_ is False,
            f"solve -> {r_} in {time.time() - t:.1f}s")
    except ImportError:
        chk("f  sanity re-solve", None, "python-sat not installed")

    # ---------------------------------------------------------------- (g) negative controls
    v0 = E[0][0]
    Xp = [list(map(list, P)) for P in X]; Xp[v0][0] = list(Xp[v0][0]); Xp[v0][0][0] += Q(1, 10 ** 6)
    MXp = [row[:] for row in MX]; MXp[v0] = [M(c) for c in Xp[v0]]
    sph = vec(MXp[v0][0] * col(Xp[v0][0]) + MXp[v0][1] * col(Xp[v0][1]) + MXp[v0][2] * col(Xp[v0][2])) == r2
    unit_p, _ = all_unit_pairs(Xp, MXp)
    inc = [e for e in Es if v0 in e]; surv = sum(1 for e in inc if e in set(unit_p))
    # moving x changes X.Y by 1e-6 * Y_x, so exactly the incident edges whose other end has Y_x = 0 must survive
    expect = sum(1 for a, b in inc if all(c == 0 for c in X[b if a == v0 else a][0]))
    dropped = Es[1:]
    chk("g  negative controls: perturbed vertex fails a2/a3; edge list with one edge removed fails a3",
        (not sph) and surv == expect and dropped != unit,
        f"vertex {v0} x += 1e-6: on sphere {sph}; {surv}/{len(inc)} incident edges survive (expected {expect}: the "
        f"neighbours with x = 0, whose chord to it does not depend on its x); list minus {Es[0]} accepted: {dropped == unit}")

    # (f) is an optional sanity re-solve (python-sat); if it did not run, it does not count against the result
    allok = all(v is True or (v is None and k.startswith("f ")) for k, v in RES.items())
    log((f"ALL CHECKS PASS: sphere_{N}: n = {n}, edges = {len(E)}, chromatic number 5" if allok else
         f"NOT ALL CHECKS PASSED / RAN: sphere_{N}: n = {n}, edges = {len(E)}; failed or not run: "
         f"{[k for k, v in RES.items() if v is not True]}") + f" ({time.time() - T0:.1f}s)")


if __name__ == "__main__":
    main()
