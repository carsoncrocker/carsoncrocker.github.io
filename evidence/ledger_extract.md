# Ledger extract

Verbatim rows from `LEDGER.md`, the project's working record of every claim and check, kept by Claude and read by me. The ledger is written in British spelling and in shorthand; it is reproduced as written. Each row is cited by its line number in `LEDGER.md` (as of 7 October 2026). Redactions are marked in square brackets: `[redacted: unreleased result]` for work that is not public yet, `[redacted: private correspondence]` for the content of private emails, and `[redacted: local path]` for file locations on my computer. Nothing else has been changed.

## What the ledger is {#L1}

Source: `LEDGER.md`, lines 1, 3, 4.

> # Research ledger: claims, checks, outcomes
> One line per claim. A claim is a RESULT only if its check is exact/machine-verifiable and the files are on disk.
> Status: RESULT (certified) · CLOSED (certified negative) · DEAD (refuted) · NOT NEW (prior art) · LEAD (unverified) · OPEN.

Supports: The ledger records one line per claim with its status; it is the project's record of what was checked.

## 15 Sep 2026: first attempts at famous problems {#L8}

Source: `LEDGER.md`, lines 8, 9, 12.

> | 2026-09-15 | Parts 509-vertex graph is not 4-colourable, vertex-critical | local rebuild | fresh CaDiCaL + Glucose, exact edges | RESULT (reproduction) |
> | 2026-09-15 | G509 −3 +2 / −2 +1 over 1389-point pool can reach 508 | search goal | exact level-1 sets + monotonicity, `verify_l1.py` | CLOSED: none exists |
> | 2026-09-15..18 | Some φ / (√3+1)/√2 / 2 pair is forced different, or a far pair forced same, in union (4486) or closure (12136) graphs | χ≥6 attack | exact SAT per candidate, models re-checked | CLOSED: zero forced pairs |

Supports: The project began on 15 September 2026 with attempts on famous problems (the Hadwiger-Nelson problem); these were closed without a new result.

## A ChatGPT lead that turned out false {#L13}

Source: `LEDGER.md`, line 13.

> | (ChatGPT) | c(3207)=c(3229) ⇒ UNSAT in 33,754-vertex graph ("φ virtual edge") | ChatGPT sandbox | later ChatGPT run found explicit 5-colouring with equal terminals; all 11 such pairs refuted | DEAD |

Supports: An AI-reported lead was refuted by a later check.

## 20 Sep 2026: a result found to be already known {#L16}

Source: `LEDGER.md`, line 16.

> | 2026-09-20 | 5-chromatic UDG of diameter ≤ 2.917 / radius 1.125 is new | other session | literature check: Parts, Polymath16 thread 17, Feb 2021: radius 1.00 | NOT NEW |

Supports: A certified graph thought to be new was found in a 2021 Polymath16 thread.

## Lessons written as rules {#L229}

Source: `LEDGER.md`, lines 229, 230, 231, 233.

> - LLMs are useful verifiers when forced to run code against a certificate with an adversarial prompt; they are poor judges when asked for an opinion on significance (they flatter).
> - "Certified by me, checked by me" is not independent. Release checklist adopted (7 rules) after the user asked whether our rules were right.
> - Literature check BEFORE compute (diameter result: days of compute vs 3-minute search).
> - Confident AI summaries drift: they re-promoted a refuted clue. Only files + certificates count.

Supports: Lessons are written back as rules: LLMs as code-running verifiers, independence, literature check before compute, files over AI summaries; the 7-rule release checklist came after Carson asked whether the rules were right.

## 27 Sep 2026: #188 lower bound k >= 7 {#L552}

Source: `LEDGER.md`, line 552.

> | 2026-09-27 (night, f97246) | Erdős #188: every red/blue colouring of the plane has a red unit pair or a blue 6-term unit-step AP, i.e. k >= 7 (published k >= 6, Tsaturian 2017) | lane P2, [redacted: local path] (lemma ladder L4 -> L3 -> L2 -> L6: no red pair at distance 4, 3, 2, 6; finish: radius-5 circle red); exact coords Q(omega, sqrt-11) | 4 CNFs UNSAT, drat-trim VERIFIED x4 (author) and re-run by reviewer; author exact clause checker BAD=0; BLIND verifier (E188_blind: own field arithmetic, every clause, Glucose4/Lingeling proofs drat-trim verified for L2/L3/L6; L4 via provided proof only; 24/24 corruptions rejected); adversarial review (E188_review): no fatal flaw, 3 packaging must-fixes | RESULT pending 48 h + expert check (not public). Credit Arman-Tsaturian 3D approach. FAILED/UNDONE: independent L4 solve not finished (machine saturated) |

Supports: Date of the lower bound; checks used (drat-trim, blind verifier, adversarial review); credit to the Arman-Tsaturian approach.

## 29 Sep 2026: #188 upper bound 242 {#L585}

Source: `LEDGER.md`, line 585.

> | 2026-09-29 02:20-07:37 (lane FE; blind RV4) | **Erdos #188 UPPER bound**: an explicit periodic red/blue colouring of the plane (hexagons of diameter 0.95, 19x19 period, 37 red closed cells, snap_B.npy sha256 4D48DBD4...) with no red unit pair and no blue unit-step K-term progression: FE certifies K = 985; RV4's independent verifier certifies K = 242 on the same colouring (published best 6330, CMXZ arXiv 2606.17194) | [redacted: local path] (ub188_verify.py, UB188_METHOD.txt, snap_B.npy, cert_snapB_half*.txt); [redacted: local path] (rv4_verify.py, rv4_claimA.py, REPORT.txt) | Claim A in interval arithmetic (min red-red distance 1.25673 > 1, diameter 0.95). Claim B: two independent codes (same method family: per-line residues + perturbation bound), full theta coverage, double precision with explicit margins; controls fail as expected; brute-force cross-checks. Genuine longest blue run found: 77 | RESULT (author-level, blind HOLDS WITH CAVEATS): 7 <= k <= 242. Owed: interval-arithmetic chord step, third independent check, adversarial review of the method, literature, 48 h |

Supports: First upper bound, 242 (vs published 6330), on 29 September.

## 30 Sep 2026: #188 upper bound 107 (was 166) and 85 {#L597}

Source: `LEDGER.md`, lines 597, 598.

> - 2026-09-30 03:30 **ERDŐS #188: k <= 107 (was 166)** - cand1 ([redacted: local path]): 39 red regular 24-gons (diam < 0.99895) per period ~19Lambda, free rational centres. Claim A exact; Claim B vpoly2 full pass (20000 theta boxes, 10 refined, max 106). BLIND (BLIND_A107, own inscribed-disk torus-covering method, 40,000 boxes) PASS - orientation-independent (red disks of radius h suffice); rounding via hand error bound, not full arb. ADVERSARIAL (RV_A107) HOLDS WITH CAVEATS, rigorous blue l106 witness (M = 106 tight for this colouring). Owed: 48 h (to 10-02), arb upgrade of blind rounding, state orientation, write-up for a later paper version (Sunday arXiv stays at 166).
> - 2026-09-30 ~10:00 **ERDŐS #188: k <= 85** - cfg_a42.json ([redacted: local path], sha256 54b3ee4a...2559b6): 42 red regular 24-gons (any orientation; inscribed disks suffice) on cand1's lattice. Verifier 1: vpoly2 full pass + 46 refined boxes, M = 84. Verifier 2 (BLIND_A85, independent, FULLY arb: 140,660,931 quadtree leaves re-checked at 96 bits, min margin 7.3e-10): PASS. Control 84 translates fails at 81.86-82.34 deg; blue l84 proved in arb at 81.8957 deg -> tight. 1M-line sweep max 84. Owed: human read of shared lattice-reduction argument, 48 h (to 10-02 ~10:00), write-up. Supersedes k <= 107.

Supports: Upper bounds 107 and 85 on 30 September.

## 1 Oct 2026: red cells of different sizes {#L601}

Source: `LEDGER.md`, lines 601-604.

> ## 2026-10-01 — Erdős #188 upper bound: Currier's mixed-size idea (NUMERIC ONLY, not verified)
> - Source of idea: Gabriel Currier email 10-01 (smaller red cells in the gaps; [redacted: private correspondence]).
> - [redacted: local path] Blind hole-filling of cfg_a42 does nothing (84 stays). Joint move works: push big cells apart, insert a smaller 24-gon (rho 0.12-0.36) on the worst blue run, re-relax with separations 1+r_i+r_j+0.005 (mix3.py).
> - Numeric M: 84 -> 82 -> 81 -> 74 (best74.npy, 45 cells) -> 68 (best68.npy, 46 cells: 42 big + radii 0.12, 0.36 x3). dense.py (14,666 thetas, tstep 0.005) confirms 74 and 68. Would mean k <= 69.

Supports: Gabriel Currier's suggestion of smaller red cells in the gaps, received 1 October, and the first numeric results.

## 2 Oct 2026: #188 upper bounds 69 and 64, and the over-fitted search {#L607}

Source: `LEDGER.md`, lines 607-619.

> - 10-02: cfg_m68.json (sha 777f6c15...9324, 46 cells, h in {0.4952, 0.3569, 0.1189}) CERTIFIED no blue l_69 by BOTH verifiers:
>   V2MIX blind torus covering NJ=69 PASS (142,474,971 arb leaves, 0 fail; NJ=68 control fails ~153.9 deg); V1MIX Method 1 M=68
>   (needed a 2nd nested refinement at ~89.95 deg + final_m.py, not yet reviewed). Claim A exact PASS (tightest 1.62447 vs 1.61940).
>   Regressions: V2 identical to release on cfg_a42; V1 17/20 chunks identical, rest paused (resume_all.sh). So k <= 69 pending
>   adversarial review + 48 h (to 10-04). Search continues from best67.npy (numeric 67).
> - 10-02 afternoon: old numeric search over-fitted its sampler (best63.npy true run >= 68; V2 NJ=64 FAIL at 25.5/47.4/59.7/89.9 deg).
>   Fixed by HONEST search mix10.py (score = verifier stage-1 coverage per direction, exact in line offset; new best only after a
>   full 20000-box float sweep with refinement; failing boxes fed back = CEGAR). Honest path 68 -> 67 -> 66 -> 65 -> 64 -> 63.
>   cfg_h63.json (52 cells, evolved lattice): Claim A exact PASS (V1MIX claimA, margin 1.48e-2); V2MIX blind NJ=64 PASS
>   (40,008 arb boxes, 144,786,936 arb leaves, 0 failures, direction cover exact). => k <= 64 (one verifier). V1MIX Method 1, review, 48 h owed.
> - 10-02 evening: cfg_h63.json (sha 1aab4cbf...9511) now DOUBLE-VERIFIED: V1MIX Method 1 certified M=63 (main 879 s, refine 657 s,
>   boxes 8078/8079 ~72.7 deg needed one nested level at N=320000; final_m.py exit 0) + V2MIX blind NJ=64 PASS. Claim A PASS both.
>   => 7 <= k <= 64 pending adversarial review (incl. final_m.py / nested refinement) + 48 h (to ~10-04 evening). Honest search

Supports: k <= 69 and k <= 64 on 2 October; the search had over-fitted its sampler (claimed 63, true run at least 68) and was replaced by an honest score taken from the verifier.

## 1 Oct 2026: ChatGPT referee of the 85 note {#L624}

Source: `LEDGER.md`, line 624.

> - 09-30 23:12 CDT [10-01 04:12Z] (not in the 10-01 block) ChatGPT referee of the #188 k <= 85 note: "revision required", no counterexample; Claim A and the blue l84 witness confirmed; Method 1 float domain bounds incomplete; 9 points. All 9 fixed by 23:40 CDT: Method 1 domain ranges in arb, full re-run M=84; Method 2 140,660,931 leaves PASS in 292 s. [TX 10-01T04:12Z, 04:40Z; RELEASE_TRACKER.md row W1]

Supports: ChatGPT acted as an outside referee; its points were fixed.

## 3 Oct 2026: a faster search tool, and a false best caught {#L626}

Source: `LEDGER.md`, line 626.

> - 10-03 00:20 CDT [05:19Z] #188 search tooling: mix13.py (agent-built) replaces the two-tier seeds 141/142, which had been stuck at 63 since 23:30. 4.3x faster (early exit on usually-failing directions) and flags the same 16 bad directions as the old scorer. 00:40: a sub-63 candidate is caught by the sweep at its true value, 68. [TX 10-03T04:26-05:40Z; [redacted: local path]]

Supports: A rebuilt search tool was 4.3x faster; a false candidate was caught at its true value.

## 3 Oct 2026: a question storm on #188 {#L629}

Source: `LEDGER.md`, lines 629, 630.

> - 10-03 02:07-02:56 CDT #188 T188 question storm. Q1 targeted residue shifts: NEGATIVE (fixing the hot set raises other directions to 63-69). Q3 NEAR/FAR SATELLITES: red pieces may sit closer than 1 if every cross distance is < 1 ("gap > 1 is not WLOG", from FRESH Q2). One satellite (r 0.2985 next to cell 46) gives HONEST 61 with full sweep 0 bad boxes and exact near/far margin 0.005 ([redacted: local path], 02:29 CDT [07:29Z]) => k <= 62, float-level. 2-3 satellites stay at 61. [[redacted: local path]; TX 10-03T07:20-07:56Z]
> - 10-03 02:25-13:33 CDT mix14 (mix13 + near/far relax, mix_relax_nf.py). Seed 201 (1 h) ends (61,11). Seeds 202/203 (10 h each) end at 61: 203 reaches (61,1); 202 bloats to 110 pieces. PLATEAU ~10 h, no stop rule (AUDIT §b row 2). 09:32 CDT [14:32Z]: a "60" swept at its true value, 66 (158 failing ranges): false best caught. [[redacted: local path], m14_202.log, m14_203.log; TX 10-03T08:31Z, 13:27Z, 14:32Z; [redacted: local path] l.85]

Supports: A storm of parallel questions produced the near/far 'satellite' idea; another false best was caught by the sweep.

## 3 Oct 2026: probes that did not move {#L636}

Source: `LEDGER.md`, line 636.

> - 10-03 PROBES with NO MOVEMENT: PAE (almost-equidistant: R^6 18 = known, not extendable to 19; R^7 untested); PG7 (4,400 LCF graphs, all 3-colourable; record 171 stands); PMATCH (nothing realised, positive control never passed => uninformative). [[redacted: local path], PG7\REPORT.txt, PMATCH\REPORT.txt]

Supports: Short probes end with a one-line verdict; a probe whose positive control never passed is recorded as uninformative.

## 3 Oct 2026: choosing #189 from a list of loose bounds {#L638}

Source: `LEDGER.md`, line 638.

> - 10-03 01:38-01:40 CDT [06:38-06:40Z] PROCESS ERROR: #173 relaunched as a probe from a general-criteria scout (NEXT_ERDOS_SHORTLIST_2026-10-03.md), although it was marked crowded on 09-28. Carson: "Is that what we did?". Stopped within ~2 min, so no folder exists. The re-scout for loose numbers produced LOOSE_BOUND_TARGETS_2026-10-03.md (top pick #189), and memory target-selection-pattern.md was written. [TX 10-03T06:38-06:56Z; PLAYBOOK_v2.md l.44]

Supports: #189 was the top pick of a re-scout for loose bounds; a relaunch of a crowded target was caught and stopped.

## 4 Oct 2026: the bound is the run plus one {#L639}

Source: `LEDGER.md`, line 639.

> - 10-04 12:33 CDT [17:33Z] Claude said "reached 62 and then 61", treating a longest blue run as the bound. Carson: "arent we at 62". Rule: the bound is run + 1. [TX 10-04T17:32-17:33Z; C_errors.md row 21]

Supports: Carson caught Claude treating a blue run as the bound.

## 4 Oct 2026: #188 upper bound 60, two verifiers {#L645}

Source: `LEDGER.md`, lines 645, 646, 647.

> - 10-04 15:51 CDT V2MIX on cfg_k60: NJ=60 PASS (40,198 boxes, refinement to level 5 near 21.356 deg, 147,421,290 arb leaves, 0 failures, min margin 1.85e-9, exact direction cover) => k <= 60 (one verifier). [[redacted: local path]]
> - 10-04 ~18:11-21:19 CDT V1MIX on cfg_k60: main pass W=0.04 (chain2.log); 448 boxes refined -> 24 still at M 71 (20:39); level-2 (64x) -> 14 left near 21.36 deg (21:08); level-3 needed strip width W=0.002, not finer angles (21:18). combine_k60.py re-reads all 527 raw records: final M 59, 0 unresolved (424/24/210 per level) -> "PASS: every direction box certified with M <= 59, so k <= 60" at 21:19 CDT [02:19Z]. => 7 <= k <= 60 DOUBLE-VERIFIED (V1 + V2; Claim A by claimA_nf + indep_nearfar). The 48 h runs to ~10-06 21:20 CDT. [[redacted: local path], fastk60.log, combine_k60.out; TX 10-05T02:19Z; AUDIT.md l.116]
> - 10-04 21:48 CDT [02:48Z] Review of combine_k60.py: every tamper test (deleted record, nudged value, fake checksum, wrong level, dropped value) refuses PASS. One weakness fixed: `python -O` stripped the asserts, so the checks no longer use assert. [TX 10-05T02:48Z]

Supports: k <= 60 certified by Method 2 and confirmed by Method 1 on 4 October; tamper tests on the combiner; the 48-hour hold.

## 4-5 Oct 2026: ChatGPT referee and sign-off for #188 {#L649}

Source: `LEDGER.md`, lines 649, 651.

> - 10-04 19:38 CDT [10-05 00:38Z] CHATGPT REFEREE on k <= 62 (release_188_v4 as built 14:49): signs the 62 bound (own Claim A for all three files; 218 exact rational directions for cfg_t61; Method 2 re-run PASS). Would NOT sign "Claim B proved in two ways" while Method 1 for 62 was "[TO FILL]"; it also flags an uncertified blue-l61 sentence and 77 files missing from the manifest. 3 MUST. Fixed in the 60 version (509 files, all in SHA256SUMS; Method 2 = proof, Method 1 = second check). [TX 10-05T00:38-00:59Z; C_errors.md row 2]
> - 10-04 23:22 CDT [04:22Z] CHATGPT SIGNS OFF 7 <= k <= 60: 204 near pairs, none ambiguous; V2 40,198 boxes reproduced; combined V1 records; all four lower-bound proofs in DRAT and LRAT. Packaging MUST 3 only partly done (zip/manifest) at that point. 23:54 CDT [04:54Z] ChatGPT PAPER review of the 15-page note: "no gap in the stated proof"; wording MUST-fixes applied. [TX 10-05T04:22Z, 04:54Z; C_errors.md l.174-175]

Supports: ChatGPT would not sign 'proved in two ways' while one method was unfinished; it signed off 7 <= k <= 60.

## 5 Oct 2026: #189 lower bound found {#L654}

Source: `LEDGER.md`, line 654.

> - 10-05 00:40-07:20 CDT NIGHT RUN (NIGHT_2026-10-05.md, MORNING_REPORT_2026-10-05.md authoritative). ERDOS #189 FIRST LOWER BOUND: every 2-colouring of R^2 has a monochromatic area-1 rectangle, so 3 <= r <= 21. First a 367-pt Eisenstein disc (01:50, cadical UNSAT, then glucose DRAT + LRAT VERIFIED at 02:40), then the point-minimal cert180 (180 pts, a Z[sqrt-3] coset of the Eisenstein lattice scaled 192^(-1/4), 676 rectangles; glucose DRAT drat-trim VERIFIED + lrat-check VERIFIED + lingeling proof; blind exact checker PASS; adversarial SOUND). NOVELTY.md: novel as far as determinable; four print-only sources unread. Does NOT settle the "every area in one class" form. 3 colours blocked. Owed: 48 h (~10-07 03:00), [redacted: private correspondence]. [[redacted: local path], NOVELTY.md; NIGHT_2026-10-05.md HITS; MORNING_REPORT_2026-10-05.md]

Supports: #189 certificate found in an overnight run; checks; what is not settled.

## 5 Oct 2026: authors told before posting {#L659}

Source: `LEDGER.md`, line 659.

> - 10-05 EXPERTS on #188. Gabriel email sent 07:43 CDT (scheduled; 7 <= k <= 60, Wednesday post, no arXiv). [redacted: private correspondence] The note was rebuilt by 18:02 CDT. [redacted: private correspondence] [TX 10-05T05:17Z, 16:34Z, 22:54Z, 23:02Z, 10-06T03:23Z; B_results.md l.80-81; [redacted: local path] mtime 17:57]

Supports: The prior-work author was written to before the planned post.

## 5 Oct 2026: ChatGPT sign-off for #189 {#L660}

Source: `LEDGER.md`, line 660.

> - 10-05 15:03 CDT [20:03Z] CHATGPT SIGNS OFF #189 3 <= r <= 21: own geometry rebuild (exactly 676 rectangles, identical CNF), UNSAT with a different solver (CaDiCaL), DRAT checked. 3 MUST (packaging: .lrat/lingeling proofs missing, DOI placeholder, outdated AI disclosure). [TX 10-05T20:03-20:05Z; C_errors.md row 6, l.177]

Supports: ChatGPT rebuilt the #189 formula with its own code and re-solved it.

## 6 Oct 2026: #189 Lean proof {#L663}

Source: `LEDGER.md`, line 663.

> - 10-05 23:12 CDT -> 10-06 00:12 CDT #189 LEAN 4 FORMALISATION ([redacted: local path]): theorem Erdos189.erdos189_two_colours, sorry-free. Geometry of all 676 rectangles by kernel computation; the SAT part by bv_decide (CaDiCaL + Lean's verified LRAT checker). Axioms: propext, Classical.choice, Quot.sound, Erdos189.sat_explicit._native.bv_decide.ax_1_5 (trusts the compiled verified checker). Lean 4.35.0-rc3 / Mathlib v4.35.0-rc3; clean build exit 0 (BUILD_LOG: lake build 199 s; README: 65 s wall for the project with Mathlib from cache). [[redacted: local path], BUILD_LOG.txt]

Supports: Sorry-free Lean 4 proof of the two-color statement, with the bv_decide axiom.

## Lessons from the backfill {#L664}

Source: `LEDGER.md`, line 664.

> - LESSONS (from this backfill): (1) A float-level "honest" score still needs the rigorous verifier: false bests at 68 (10-03 00:40), 66 (10-03 09:32) and 62 (10-04 ~15:20) were all caught only by the sweep or V2. (2) Run the second verifier on every bound you claim: V1 never ran on t61, so "two methods" for 62 was false. (3) Write the ledger row when the result lands, not afterwards: four days went unrecorded and had to be rebuilt from transcripts. (4) Check the ledger's dead list before relaunching a target (#173). [this block; AUDIT.md; C_errors.md rows 1, 2, 17, 20]

Supports: Lessons written back as rules, including 'run the second verifier on every bound you claim'.

## 6 Oct 2026: a proof checker's false VERIFIED (stale header) {#L668}

Source: `LEDGER.md`, line 668.

> - 10-06 02:47-06:10 CDT [redacted: unreleased result] tampered CNF NOT VERIFIED (after a stale-header false VERIFIED - pitfall); [redacted: unreleased result]

Supports: On unreleased work, a proof checker printed VERIFIED on a tampered file because its header was stale.

## 6 Oct 2026: #189 passes cake_lpr {#L676}

Source: `LEDGER.md`, line 676.

> - 10-06 ~21:15 #189 cake_lpr (formally verified CakeML LRAT checker, github tanyongkiam/cake_lpr, built from source matching its cake_lpr.sha256 at basis_ffi.c rev a4323b2 + cake_lpr.S of a36874a; HEAD basis_ffi.c drifted from the sha file upstream): cert180.cnf + cert180.lrat -> 's VERIFIED UNSAT' (~3 min). Controls: 3 clauses weakened in place (same ids) -> all FAIL. So #189 now: drat-trim + lrat-check + cake_lpr (verified) + Lean bv_decide.

Supports: #189 LRAT proof passes the formally verified checker cake_lpr; controls fail.

## 6 Oct 2026: the 'full run' correction {#L679}

Source: `LEDGER.md`, line 679.

> - 10-06 ~22:45 CORRECTION to the 10-04 22:23 row: release_188_v4 'verify_all.sh full' clean-copy run did NOT pass as one run - it passed manifest, Claim A x2, Method 2, Method 1 records + recheck, then stopped at step 5 (drat-trim not on PATH; release_188_v4_cleanfull.log, exit 1, 1406 s). Lower bound passed in a SEPARATE run (release_188_v4_cleanlower.log, 4 DRAT + LRAT VERIFIED). Caught by external review 10-06. Single full run relaunched 22:40 with drat-trim on PATH: [redacted: local path] spot_check.py fixed (A samples until N red points; numpy-only fallback) and tested both paths.

Supports: A clean run described as one full pass had really been two separate runs; corrected in the ledger.

## 6 Oct 2026: #188 cake_lpr, and the vacuous tamper test {#L680}

Source: `LEDGER.md`, line 680.

> | 2026-10-06 22:50 | #188 cake_lpr | L4x/L3x/L2x/L6x LRATs: s VERIFIED UNSAT under cake_lpr (formally verified checker), header=body all four. Control v1 (weaken clause idx 100) was VACUOUS: clause not used by proof -> passed. Control v2 (fresh var added to used clause id 799) FAILS as required. Lesson: controls must touch a clause the proof uses. | [redacted: local path], cake188_control.log |

Supports: #188 lower-bound LRATs pass cake_lpr; header equals body; the first control was vacuous.

## 6 Oct 2026: AI logs archived with checksums {#L681}

Source: `LEDGER.md`, line 681.

> | 2026-10-06 23:35 | LOG ARCHIVE | Snapshot of Claude Code sessions since 10-05 15:05 (5 sessions + subagent logs, 748 files, 375 MB) -> [redacted: local path], checksums [redacted: local path] Current session still running: re-snapshot at end. | [redacted: local path] |

Supports: Claude Code session logs are archived with SHA-256 checksums.

## 7 Oct 2026: one clean full run {#L682}

Source: `LEDGER.md`, line 682.

> | 2026-10-07 00:00 | #188 FULL RUN | Single uninterrupted clean-copy run of release_188_v4 'PYTHON=[redacted: local path] bash verify_all.sh full' in fresh [redacted: local path] steps 0-5 all OK (sha256, Claim A x2, Claim B Method 2 with 60 translates, Method 1 records M<=59 + 3 recomputed identical, lower bound VERIFIED). SUMMARY: PASS (full), exit 0, 2606 s. Closes the 10-06 22:45 CORRECTION. | [redacted: local path] |

Supports: Single uninterrupted full run of the #188 package passed (2606 s, about 43 minutes).

## 7 Oct 2026: third blind verifier and attacker for #188 {#L683}

Source: `LEDGER.md`, lines 683, 684.

> | 2026-10-07 | V3_188 BLIND 3rd Claim B verifier | CERTIFIED no blue l_60 for cfg_k60 over all directions [0,180): own design, integer interval engine (2463 s-intervals, rational unit vectors) + separate Fraction/mpmath rechecker (9,287,913 witnesses, 0 bad, tiling + angle coverage OK). Controls: k=80 pass; k=59 FAILS with explicit exact blue l_59 at ~149.53 deg (so 60 is tight for this colouring); shrunk apothems / deleted cell -> failures; checker cross-test OK. Claim A also re-passed (mpmath). Caveat: saw README 204/44 figures. | [redacted: local path] |
> | 2026-10-07 | BREAK188 attacker | No counterexample: own evaluator from README; scans 0-180 deg (0.05 deg, fine 0.002 deg on hot bands) max blue run 59 only at ~149.52-149.69 deg (agrees with V3's l_59 at ~149.53); 42 local optimisations toward 60 stay >=2.87e-3 inside red. Claim A: 830 pair ranges, none contains 1; max cell diam 0.99895; 204 near pairs match README; min slack ~5e-3. Float64+80-digit, not a proof. Note: the '21.36 deg' hint was a frame mismatch (both V3 and BREAK find hardest/true max near 149.5 deg). | [redacted: local path] |

Supports: A third blind verifier and an adversarial search, both written without reading the other verifiers.

## 7 Oct 2026: the #188 package that was published {#L695}

Source: `LEDGER.md`, line 695.

> | 2026-10-07 ~08:45 | #188 release_188_v4b | v4 + extra_checks/ (cake_lpr logs+controls, blind V3 verifier, adversarial search, README) + logs/FULL_RUN_2026-10-06.log; README cake_lpr line updated; SHA256SUMS regenerated (1119). Clean full run PASS (exit 0, 1832 s). Zip [redacted: local path], unzip manifest OK; [redacted: local path]. This is the file for Zenodo DOI 23151059. | [redacted: local path] |

Supports: The published #188 package is release_188_v4b, with the extra checks.

## 7 Oct 2026: both packages published on Zenodo {#L699}

Source: `LEDGER.md`, lines 699, 700.

> | 2026-10-07 ~10:00 | #189 PUBLISHED on Zenodo | https://zenodo.org/records/23178517, DOI 10.5281/zenodo.23178517 (doi.org resolves). File FINAL_189_release_189_lb.zip md5 bdf689e72eab72cb15f79ae006b111a9 = local [redacted: local path] Dataset, CC BY 4.0, open, creator Crocker Carson, date 2026-10-07, AI disclosure in description. All DOI references consistent: #188 23151059 (note.tex, README, site), #189 23178517 (note.tex, README, site). |
> | 2026-10-07 ~14:30 | #188 PUBLISHED on Zenodo | https://zenodo.org/records/23151059, DOI 10.5281/zenodo.23151059 (doi.org resolves). File FINAL_188_release_188_v4b.zip md5 be0250af6221657930cdcea6854c2f21 = local [redacted: local path] Dataset, CC BY 4.0, open, 2026-10-07, AI disclosure, American spelling. First upload attempt stalled at 90% (failed, 0 bytes); re-upload OK. |

Supports: Publication of both packages on Zenodo, 7 October 2026.

## 7 Oct 2026: this site launched {#L701}

Source: `LEDGER.md`, line 701.

> | 2026-10-07 ~15:00 | SITE LIVE | https://carsoncrocker.github.io (repo carsoncrocker/carsoncrocker.github.io, public, GitHub Pages from main). Pages: index.html, tracker.html (Log page withheld until Carson writes posts). [redacted: local path and account details] |

Supports: The site went live on 7 October 2026.

## 29 Sep 2026: #188 upper bound 166 (night log, not LEDGER.md) {#N29-183}

Source: `NIGHT_2026-09-29.md` (the running log of that night), line 183. The ledger itself records 166 only as the bound that 107 replaced (row L597).

> * 13:25 UB188_FINAL VERDICT READY (K = 166), technical: snap_C (36 red, sha256 e24c9638...) Claim A exact (Q(sqrt3)) + Claim B certified by verifier3 (interval arithmetic, exact theta tiling, 20000 boxes, 0 failures): no red unit pair, no blue l_166 -> Erdos #188 k <= 166 (snap_B backup: k <= 188). Corroboration: RV4 code on snap_C 293, FE 395. Certified blue runs 140 (snap_C) / 155 (snap_B). Owed: 48 h, human read of reduction, clean-machine rerun, Carson gate; [redacted: private correspondence]. [redacted: local path]

Supports: the upper bound 166 on 29 September.
