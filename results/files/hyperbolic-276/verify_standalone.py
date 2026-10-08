"""Standalone verifier for the 276-vertex 5-chromatic unit-distance graph in the hyperbolic plane.

usage:  python verify_standalone.py hyp_EI_276.json [--log FILE] [--no-drat] [--no-solve] [--drat-timeout SEC]

Needs only: Python 3 and python-flint; python-sat (pysat) is optional (secondary re-solve).  drat-trim is used for the proof check if it is on
PATH; otherwise the pure-Python forward checker py_drat_check below (standard library, under a minute).  It does not import any project code; everything is re-derived from hyp_EI_276.json and the certificate
files in the same folder.

Checks (all exact unless stated):
 F  field / distance: c's minimal polynomial m irreducible; c = largest real root isolated by a Sturm sequence over Q
    and enclosed in an interval of width < 2^-400; 2c-1 > 0, 1-c^2 > 0, C = c/(1-c) > 1 (interval arithmetic);
    if w = sqrt(D) is used, K[w]/(w^2-D) is a field (charpoly of c+w over Q irreducible of degree 2[K:Q]);
    the stated polynomial P of cosh d is irreducible and P(c/(1-c)) = 0 exactly in K; d = arccosh(C) printed.
 G  geometry: exact <X,X> = -1 for every vertex; t > 0 (interval arithmetic); every listed edge has -<X,Y> = C exactly;
    every non-edge pair has -<X,Y> != C exactly (the graph is the full distance-d graph on its vertex set);
    vertices pairwise distinct (exact); edge list well-formed; 30-digit decimal hyperboloid and Poincare-disk
    coordinates agree with the exact ones to 1e-29.
    Soundness of exact equality/inequality: arithmetic is in K = Q[c]/(m) (resp. K[w]/(w^2-D)), which is a field, so
    evaluation at the real root c (and w = +sqrt(D)) is an injective ring map: equal in the field <=> equal as reals.
    Real point: X = (t, R*xh, R*s*yh), R = sqrt(2c-1), s = sqrt(1-c^2), so <X,Y> = -t t' + (2c-1) xh xh' + (2c-1)(1-c^2) yh yh'.
 S  SAT certificate: the CNF is regenerated from the edge list (variable 4v+k+1 = "vertex v has colour k", k=0..3;
    one at-least-one clause per vertex; clauses (-x_ak, -x_bk) for every edge and colour; symmetry breaking: the three
    vertices of one listed triangle get colours 0,1,2 as unit clauses, which is without loss of generality because
    color classes can be permuted).  A satisfying assignment would give a proper 4-coloring; conversely any
    4-coloring can be permuted to satisfy the units.  The regenerated clause set must equal the certificate CNF.
    drat-trim must report "s VERIFIED" for (CNF, DRAT).  Secondary (not a certificate): Glucose 4 re-solves the CNF.
 C  vertex deletions: every stored colouring of G - v is a proper 4-coloring of G - v.
 N  negative controls: a perturbed vertex, a dropped CNF clause and a corrupted colouring must each be detected.
"""
import sys, os, json, time, hashlib, subprocess, shutil
import flint
from flint import fmpq, fmpq_poly, fmpz_poly, arb

ARGS = sys.argv[1:]
GPATH = ARGS[0]
LOGP = ARGS[ARGS.index("--log") + 1] if "--log" in ARGS else None
NODRAT = "--no-drat" in ARGS
NOSOLVE = "--no-solve" in ARGS
DRAT_TO = int(ARGS[ARGS.index("--drat-timeout") + 1]) if "--drat-timeout" in ARGS else 1200
BASE = os.path.dirname(os.path.abspath(GPATH))
ROOT = BASE
flint.ctx.prec = 1600

LOG = []
RES = {}


def log(s=""):
    print(s, flush=True); LOG.append(s)


def chk(name, ok, detail=""):
    RES[name] = bool(ok)
    log(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


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


T0 = time.time()
G = json.load(open(GPATH))
n = G["n_vertices"]
E = [tuple(e) for e in G["edges"]]
m_int = G["distance"]["c_min_poly_low_to_high"]
P_int = G["distance"]["cosh_d_min_poly_low_to_high"]
D = G["field"]["w_squared"]
log(f"verify_standalone.py  {os.path.basename(GPATH)}  ({time.strftime('%Y-%m-%d %H:%M:%S')})")
log(f"python-flint {flint.__version__}; graph: {n} vertices, {len(E)} edges; c: {G['distance']['c_min_poly']} (largest real root); "
    f"cosh d: {G['distance']['cosh_d_min_poly']}; w^2 = {D}")
log(f"sha256 {os.path.basename(GPATH)} = {sha(GPATH)}")

# ============================================================ F: field and distance
log("\n--- F: field and distance")
M = fmpq_poly(m_int)
deg = M.degree()
fac = fmpz_poly(m_int).factor()
chk("F1 m irreducible over Q", len(fac[1]) == 1 and fac[1][0][1] == 1 and fac[1][0][0].degree() == deg, str(fac))


def sturm_seq(p):
    s = [p, p.derivative()]
    while s[-1].degree() > 0:
        r = divmod(s[-2], s[-1])[1]
        if r == 0: break
        s.append(-r)
    return s


SS = sturm_seq(M)


def var(x):
    vals = [q(x) for q in SS]
    sg = [1 if v > 0 else -1 for v in vals if v != 0]
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)


B = fmpq(1) + max(abs(fmpq(int(a)) / abs(m_int[-1])) for a in m_int[:-1])      # Cauchy bound: all roots in (-B, B)
nreal = var(-B) - var(B)
cnt = lambda x: var(x) - var(B)                                               # number of real roots in (x, B]
assert nreal >= 1
lo, hi = -B, B                                                                # invariant: cnt(lo) >= 1, cnt(hi) = 0
while cnt(lo) > 1 or hi - lo > fmpq(1, 10 ** 6):
    mid = (lo + hi) / 2
    if cnt(mid) >= 1: lo = mid
    else: hi = mid
assert cnt(lo) == 1 and cnt(hi) == 0 and M(lo) * M(hi) < 0                   # m squarefree (irreducible): simple root
while hi - lo > fmpq(1, 2 ** 400):
    mid = (lo + hi) / 2
    if (M(mid) < 0) == (M(lo) < 0): lo = mid
    else: hi = mid
cA = arb(lo).union(arb(hi))
chk("F2 largest real root c isolated (Sturm over Q) and enclosed", cnt(lo) == 1 and cnt(hi) == 0 and cA.rad() < arb(2) ** -399,
    f"{nreal} real roots; c = {cA.mid().str(40, radius=False)} (enclosure radius < 2^-399)")
RA = (2 * cA - 1).sqrt(); SA = (1 - cA * cA).sqrt()
CA = cA / (1 - cA)
chk("F3 2c-1 > 0, 1-c^2 > 0, C = c/(1-c) > 1 (interval)", (2 * cA - 1) > 0 and (1 - cA * cA) > 0 and CA > 1,
    f"cosh d = C = {CA.mid().str(40, radius=False)}, d = {CA.acosh().mid().str(40, radius=False)}")


def K(p):
    return divmod(p if isinstance(p, fmpq_poly) else fmpq_poly(p), M)[1]


def kinv(a):
    g, u, _ = a.xgcd(M)
    assert g == 1
    return K(u)


CX = fmpq_poly([0, 1]); ONE = fmpq_poly([1])
if D is not None:
    # multiplication by c + w on the Q-basis c^i, c^i w of K[w]/(w^2-D)
    cols = []
    for j in range(2 * deg):
        u = K(CX ** (j % deg)) if j < deg else fmpq_poly(0)
        v = fmpq_poly(0) if j < deg else K(CX ** (j % deg))
        pu, pv = K(CX * u + D * v), K(u + CX * v)                             # (c+w)(u+vw) = (cu + Dv) + (u + cv) w
        cols.append([pu.coeffs()[i] if i < len(pu.coeffs()) else 0 for i in range(deg)] +
                    [pv.coeffs()[i] if i < len(pv.coeffs()) else 0 for i in range(deg)])
    Mx = flint.fmpq_mat(2 * deg, 2 * deg, [cols[j][i] for i in range(2 * deg) for j in range(2 * deg)])
    cp = Mx.charpoly()
    cpz = cp.numer()
    f2 = cpz.factor()
    chk(f"F4 K[w]/(w^2-{D}) is a field (charpoly of c+w over Q irreducible, degree {2 * deg})",
        len(f2[1]) == 1 and f2[1][0][1] == 1 and f2[1][0][0].degree() == 2 * deg, str(cpz))
else:
    log("[----] F4 no square-root adjoined (coordinates in K = Q(c))")
PZ = fmpz_poly(P_int)
fP = PZ.factor()
acc = fmpq_poly(0)
for i, a in enumerate(P_int):
    acc += a * CX ** i * (1 - CX) ** (len(P_int) - 1 - i)
chk("F5 cosh d = c/(1-c) is a root of the stated irreducible polynomial P (exact: P(C)(1-c)^deg P = 0 in K)",
    K(acc) == 0 and len(fP[1]) == 1 and fP[1][0][1] == 1 and fP[1][0][0].degree() == len(P_int) - 1 and M(1) != 0,
    f"P = {G['distance']['cosh_d_min_poly']}")
dA = CA.acosh()
dj = arb(G["distance"]["d_decimal"])
chk("F6 d = arccosh(c/(1-c)) agrees with the stated d_decimal (to 1e-45)", abs(dA - dj) < arb(10) ** -45,
    f"d = {dA.mid().str(45, radius=False)}")

# ============================================================ exact elements
R1 = K([-1, 2]); R2 = K(R1 * K([1, 0, -1]))
CK = K(CX * kinv(K([1, -1])))
Dp = fmpq_poly([D]) if D is not None else None


def parse(a):
    if D is None:
        return K([fmpq(*map(int, (q.split("/") + ["1"])[:2])) for q in a]), fmpq_poly(0)
    return tuple(K([fmpq(*map(int, (q.split("/") + ["1"])[:2])) for q in part]) for part in a)


V = [[parse(a) for a in v] for v in G["vertices_exact"]]
hasw = [any(x[1] != 0 for x in v) for v in V]
if D is not None:
    log(f"[INFO] vertices with a non-zero w = sqrt({D}) component: {sum(hasw)}/{n}")
WT = [fmpq_poly([-1]), R1, R2]
A = [[(K(WT[k] * v[k][0]), K(WT[k] * v[k][1])) for k in range(3)] for v in V]      # weighted copies


def qf(a, aw, j):
    """exact <X, X_j> in K[w]/(w^2-D) as (u, v); a = weighted coordinates of X, aw = X has a non-zero w part."""
    b = V[j]
    u = fmpq_poly(0); w = fmpq_poly(0)
    for k in range(3):
        u += a[k][0] * b[k][0]
        if aw or hasw[j]:
            u += Dp * a[k][1] * b[k][1]
            w += a[k][0] * b[k][1] + a[k][1] * b[k][0]
    return K(u), K(w)


NEG1 = (K([-1]), fmpq_poly(0))
NEGC = (K(-CK), fmpq_poly(0))

# ============================================================ G: geometry
log("\n--- G: geometry")
okE = all(isinstance(a, int) and isinstance(b, int) and 0 <= a < b < n for a, b in E) and len(set(E)) == len(E)
chk("G0 edge list well-formed (0 <= a < b < n, no duplicates)", okE, f"{len(E)} edges")
nn = sum(1 for i in range(n) if qf(A[i], hasw[i], i) == NEG1)
chk("G1 exact <X,X> = -1 for every vertex", nn == n, f"{nn}/{n}")


def evA(x):
    u, w = x
    val = sum((arb(q) * cA ** k for k, q in enumerate(u.coeffs())), arb(0))
    if D is not None and w != 0:
        val += sum((arb(q) * cA ** k for k, q in enumerate(w.coeffs())), arb(0)) * arb(D).sqrt()
    return val


TA = [evA(v[0]) for v in V]
tp = sum(1 for t in TA if t > 0)
chk("G2 t > 0 for every vertex (interval arithmetic)", tp == n, f"{tp}/{n}")
t1 = time.time()
Es = set(E)
edge_ok = 0; edge_bad = []; extra = []
for i in range(n):
    for j in range(i + 1, n):
        g = qf(A[i], hasw[i], j)
        if (i, j) in Es:
            if g == NEGC: edge_ok += 1
            else: edge_bad.append((i, j))
        elif g == NEGC:
            extra.append((i, j))
chk("G3 every listed edge: -<X,Y> = cosh d exactly", edge_ok == len(E), f"{edge_ok}/{len(E)}; failures {edge_bad[:5]}")
chk("G4 faithful: every non-edge pair has -<X,Y> != cosh d exactly", not extra,
    f"{n * (n - 1) // 2 - len(E)} non-edge pairs checked, {len(extra)} at distance d {extra[:5]}; {time.time() - t1:.0f}s for all pairs")
keys = set(tuple(tuple(str(q) for q in part.coeffs()) for x in v for part in x) for v in V)
chk("G5 vertices pairwise distinct (exact coordinates)", len(keys) == n, f"{len(keys)} distinct of {n}")
hd = G["vertices_hyperboloid_decimal"]; pd = G["vertices_poincare_disk_decimal"]
tol = arb(10) ** -29; worst = 0.0; okd = True
for i in range(n):
    X = [TA[i], RA * evA(V[i][1]), RA * SA * evA(V[i][2])]
    Pz = [X[1] / (1 + X[0]), X[2] / (1 + X[0])]
    for val, s in list(zip(X, hd[i])) + list(zip(Pz, pd[i])):
        dlt = abs(val - arb(s))
        if not (dlt < tol): okd = False
        worst = max(worst, float(dlt.mid()) + float(dlt.rad()))
chk("G6 30-digit decimal hyperboloid and Poincare-disk coordinates agree with the exact coordinates (< 1e-29)", okd,
    f"max |exact - decimal| <= {worst:.2g}")
maxr = max((float(u) ** 2 + float(v) ** 2) ** 0.5 for u, v in pd)
log(f"[INFO] Poincare disk: max |z| = {maxr:.10f}; max t = {max(float(t.mid()) for t in TA):.6g}")

# ============================================================ S: SAT certificate
log("\n--- S: SAT certificate")
tri = G["symmetry_breaking_triangle"]
tri_ok = tri is None or all(tuple(sorted(p)) in Es for p in [(tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])])
chk("S0 symmetry-breaking vertices form a triangle of the graph", tri_ok, f"triangle {tri}")
want = [tuple(4 * v + k + 1 for k in range(4)) for v in range(n)]
want += [(-(4 * a + k + 1), -(4 * b + k + 1)) for a, b in E for k in range(4)]
if tri: want += [(4 * tri[0] + 1,), (4 * tri[1] + 2,), (4 * tri[2] + 3,)]
cnfp = os.path.join(ROOT, os.path.basename(G["certificate_files"]["cnf"])); dratp = os.path.join(ROOT, os.path.basename(G["certificate_files"]["drat"]))
log(f"sha256 {os.path.basename(cnfp)} = {sha(cnfp)}")
log(f"sha256 {os.path.basename(dratp)} = {sha(dratp)} ({os.path.getsize(dratp)} bytes)")
hdr = None; got = []
for line in open(cnfp):
    t = line.split()
    if not t or t[0] == "c": continue
    if t[0] == "p": hdr = t; continue
    assert t[-1] == "0"
    got.append(tuple(int(x) for x in t[:-1]))
norm = lambda cl: sorted(tuple(sorted(c)) for c in cl)
cnf_ok = hdr == ["p", "cnf", str(4 * n), str(len(got))] and norm(got) == norm(want)
chk("S1 certificate CNF == 4-colouring CNF regenerated from the edge list (+ triangle units)", cnf_ok,
    f"{4 * n} vars, {len(want)} clauses regenerated, {len(got)} in file")


if NODRAT:
    log("[SKIP] S2 drat-trim not run (--no-drat)")
else:
    cmd = None
    if shutil.which("drat-trim"): cmd = ["drat-trim", cnfp, dratp]
    t1 = time.time()
    if cmd is None:
        okd, msg = py_drat_check(cnfp, dratp)
        chk("S2 DRAT refutation verified by the built-in pure-Python checker (drat-trim not found)", okd,
            f"{msg} in {time.time() - t1:.1f}s")
    else:
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=DRAT_TO).stdout if cmd else ""
            st = [l for l in out.splitlines() if l.startswith("s ")]
            info = [l for l in out.splitlines() if "lemmas in core" in l or "WARNING" in l][:3]
            chk("S2 drat-trim verifies the DRAT refutation of the CNF", st and st[-1] == "s VERIFIED",
                f"'{st[-1] if st else 'NO STATUS / drat-trim not found'}' in {time.time() - t1:.1f}s {info}")
        except subprocess.TimeoutExpired:
            chk("S2 drat-trim verifies the DRAT refutation of the CNF", False, f"TIMEOUT after {DRAT_TO}s")
if NOSOLVE:
    log("[SKIP] S3 independent re-solve not run (--no-solve)")
else:
    try:
        from pysat.solvers import Glucose4
        t1 = time.time()
        s = Glucose4(bootstrap_with=[list(c) for c in want]); r = s.solve(); s.delete()
        chk("S3 (secondary, not a certificate) Glucose 4 re-solves the regenerated CNF: UNSAT", r is False, f"{time.time() - t1:.1f}s")
    except ImportError:
        log("[SKIP] S3 secondary re-solve not run (python-sat not installed)")

# ============================================================ C: vertex deletions
log("\n--- C: G - v colourings (vertex-criticality)")
colp = G["certificate_files"]["colourings"] and os.path.join(ROOT, os.path.basename(G["certificate_files"]["colourings"]))
if colp and os.path.exists(colp):
    log(f"sha256 {os.path.basename(colp)} = {sha(colp)}")
    cols = json.load(open(colp))
    good = 0; badv = []
    for key, s in cols.items():
        v = int(key)
        ok = len(s) == n and s[v] == "-" and all(s[u] in "0123" for u in range(n) if u != v) and \
            all(s[a] != s[b] for a, b in E if v not in (a, b))
        good += ok
        if not ok: badv.append(v)
    chk("C1 every stored G - v colouring is a proper 4-colouring of G - v", not badv, f"{good}/{len(cols)} stored colourings valid")
    log(f"[INFO] G - v shown 4-colourable for {good}/{n} vertices -> "
        + ("vertex-critical (every vertex needed)" if good == n else "NOT shown vertex-critical (no claim of criticality)"))
else:
    log(f"[----] C1 no G - v colourings supplied for this graph (certificate_files.colourings = {colp}): vertex-criticality not claimed")

# ============================================================ N: negative controls
log("\n--- N: negative controls")
i0 = n - 1
bad = [(K(V[i0][0][0] + fmpq(1, 10 ** 6)), V[i0][0][1])] + V[i0][1:]
Abad = [(K(WT[k] * bad[k][0]), K(WT[k] * bad[k][1])) for k in range(3)]
nb = [j for a, b in E for j in ((b,) if a == i0 else (a,) if b == i0 else ())]
surv = sum(1 for j in nb if qf(Abad, hasw[i0], j) == NEGC)
chk("N1 vertex with t + 1e-6 fails the exact edge checks", surv == 0, f"{surv}/{len(nb)} incident edges survive")
chk("N2 CNF with one edge clause removed is detected as different", norm(got[:-4] + got[-3:]) != norm(want) if len(got) > 4 else True)
if colp and os.path.exists(colp) and cols:
    key, s = next(iter(cols.items())); v = int(key)
    a, b = next(e for e in E if v not in e)
    s2 = list(s); s2[b] = s2[a]
    chk("N3 corrupted G - v colouring (one edge made monochromatic) is rejected", any(s2[x] == s2[y] for x, y in E if v not in (x, y)))

allp = all(RES.values())
log(f"\n{'ALL CHECKS PASS' if allp else 'SOME CHECK FAILED: ' + str([k for k, x in RES.items() if not x])} "
    f"({len(RES)} checks, {time.time() - T0:.0f}s)")
if LOGP:
    open(LOGP, "w", encoding="utf-8").write("\n".join(LOG) + "\n")
sys.exit(0 if allp else 1)
