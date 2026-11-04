# Ledger extract, 2 to 4 November 2026

Verbatim rows from `LEDGER.md` dated 2026-11-03 and 2026-11-04, cited by line number in `LEDGER.md` (as of 4 November 2026). The ledger is written in British spelling and in shorthand; it is reproduced as written. Redactions are marked in square brackets: `[redacted: private correspondence]` for content of private correspondence and findings not yet shared with the people concerned, and `[redacted: person]` for the name of someone who has not been told. Nothing else has been changed.

## A published circuit-distance claim, reproduced {#L1070}

Source: `LEDGER.md`, lines 1070 and 1081.

> | 2026-11-03 | GATE: [redacted: person] c11 | CONFIRMED: c11 circuit distance = 10 in both bases at R=1-4 (exhaustive search finds nothing of weight <=9; weight-10 witnesses replay in Stim with drop-one controls). [redacted: private correspondence] No claim for R>=5. |
> | 2026-11-03 22:00 CST | [redacted: person] progress + WSL restart | [redacted: unfinished runs] Results banked before that: [redacted: unfinished runs] c11 R5 X and Z W9 NONE (d=10 holds through R=5); [redacted: unfinished runs] |

Supports: A search for undetected fault sets of weight 9 or fewer found none through 5 rounds for the circuit of a published claim, and weight-10 witnesses exist. These are search results, not a complete machine-checked proof for every case.

## The C9 color-code schedule: no meaningful hardware gain {#L1065}

Source: `LEDGER.md`, line 1065.

> | 2026-11-03 overnight | GATE: C9 simulation A | Result (data/n1103/CC_HW/REPORT.txt): no real hardware gain. Only uniform p=3e-3 Z memory shows -13.7% LER/round (CI 5.9-20.9%); X, p=2e-3, SI1000 show nothing; SI1000 p=2e-3 slightly worse. Equal depth/CNOTs, so per-time = per-round. Reason: both circuits fail first at 4 faults. Gate verdict per OPERATING_PLAN: NO GAIN -> keep the distance result, no v1.2 hardware claim; [redacted: private correspondence] One decoder only; no blind check yet. |

Supports: In simulation the new schedule shows no meaningful logical-error-rate gain across the settings tried; one setting shows a small gain, and the others show none or a slight loss. One decoder only.

## The d=11 schedule search stopped without a result {#L1067}

Source: `LEDGER.md`, line 1067.

> | 2026-11-03 05:24 CST | GATE: d=11 (B) | Both searches ended TIMEOUT: allbnb (all plaquettes free, 13962 s, 8780 iters) and seedab (seeded a+b fixes, change budget 21). No distance-10 schedule found, no impossibility proof. Gate verdict: FAILURE -> no relaunch; d-dependence write-up (fix needed on all 3 sides at d=11; strip-only repairs proved impossible; side fixes clash) stays in CC_HW/REPORT.txt; the schedule lane moves to its next idea at the 19:30 run. No spend added. |

Supports: Both d=11 searches hit their time limits; no schedule was found and nothing was proved impossible.

## A tropical-norm bound dropped as superseded {#L1087}

Source: `LEDGER.md`, line 1087.

> | 2026-11-04 | Tropical storm: DROP | NOVELTY.md: Bachoc-Bellitto-Moustrou-Pecher arXiv:1708.00291 Cor. 2 likely gives chi(R^n) = 2^n for this norm (so 16 in R^4), which supersedes our >= 12; significance 2/10. Not released. [redacted: unfinished runs] |

Supports: A lower bound I had found for the chromatic number of R^4 in a tropical norm appears to be superseded by earlier published work and was not released.

## c_7 <= 1345 published {#L1079}

Source: `LEDGER.md`, lines 1077 and 1079.

> | 2026-11-03 | c_7<=1345 HARDENED | RELEASE-READY (DHJ7/HARDEN/HARDEN_VERDICT.txt): cake_lpr + lrat-check independent PASS; blind re-encoding PASS (UNSAT, DRAT verified); lemma audit PASS; Codex maths PASS. [redacted: private correspondence] Next: Zenodo release under Carson's name (delegated). |
> | 2026-11-03 | c_7<=1345 PUBLISHED (Zenodo, delegated rule 6) | DOI 10.5281/zenodo.23933131. Files: note.pdf (3 pp, sha256 9c9d8b8b564ede61d89c99b274bb459010f5a326b7251f812b377fbc1f468495), replay.sh, SHA256SUMS_archives.txt, SHA256SUMS_big.txt, dhj7_c7_1345_small.tar.gz, L7_1346_d6.cnf.xz, L7_1346.lrat.xz, B7_1346_d6.cnf.xz, B7_1346.drat.xz. Codex hostile review: PASS on final text (rounds: FIX x4 then PASS; evidence-supplied); readability 8/8/8 (median 8). Novelty re-check 11-03: nothing below 1348 found; CORRECTION: Tao blog 4 Mar 2009 states c_7<=1348 (REPORT/verdict said 1350), note cites 1348 and the paper 3x450=1350. Fresh-folder full replay PASS in WSL (~10 min CPU); final replay.sh quick re-run PASS. [redacted: private correspondence] |

Supports: The deposit contains the proof files and a replay script; the proof was checked by drat-trim, cake_lpr and lrat-check, and a separately written encoding gave an unsatisfiable result whose proof drat-trim verified. The published figure being improved is 1348.

## Zenodo records updated {#L1085}

Source: `LEDGER.md`, lines 1085 and 1086.

> | 2026-11-03 | two-gross v3.2 (CLOSE item 18) | Already PUBLISHED 11-01/02 as doi:10.5281/zenodo.23875528 (no new publish). Verified live: files incl. twogross16_v3_2.zip md5 d4e11380..., description matches ZENODO_UPDATE.md. [redacted: private correspondence] |
> | 2026-11-03 | Towell audit links on Zenodo (CLOSE items 19, 20) | Metadata edits in place (no new DOI, files untouched): #189 doi:10.5281/zenodo.23178517 and latest v2 doi:10.5281/zenodo.23253656 (PR 7, issue 62); #188 v5 doi:10.5281/zenodo.23405962 (PRs 8, 10, issue 62; v5 is the version Towell audited; v4b 23151059 not edited). Paragraphs by Codex, hostile check PASS (round 3). Facts checked on GitHub 11-03: PRs 7, 8, 10 MERGED by Towell 11-02 in his own repo; plasma-ai/erdos#62 OPEN. Wording: not blind, AI-assisted, not peer review, no endorsement implied |

Supports: The two-gross v3.2 deposit is live; the Zenodo deposits for Erdős #188 and #189 now link Towell's audits, whose pull requests Towell merged on 2 November (UTC).
