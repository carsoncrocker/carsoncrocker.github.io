# Corrections and withdrawn claims

Claims that looked new or true at first and did not survive a later check. Each mistaken claim was caught before release, except the first three items below, which we found after publishing; in one case the underlying computation was later published as a reproduction of the known result. Each item gives the evidence. This list contains only the items that can be described without revealing unreleased work; items that concern unreleased results will be added when those results are published.

## A prior posting we missed: DistQLDPC's entries for two Xu et al. codes predate our release (found 17 Oct 2026, after publishing) {#w-distqldpc}

On 14 Oct we published exact distances for five lifted-product quantum codes and said none had been established before. On 17 Oct we found that Yu-Fang Chen's public repository DistQLDPC had listed distance 16 for two of them, Xu et al.'s [[714,100]] and [[1020,136]], on 11 Oct 2026. Their entries are the same codes as ours, up to relabelling qubits, and their values agree with ours. Our prior-work check for that release covered papers, the qLDPC challenge board and one benchmark repository, and missed DistQLDPC's entries; other code databases were added to the check on 15 Oct, the day after (see the next item). We withdraw the novelty claim for these two codes; our values are an independent recomputation, and the Zenodo record has a new version saying so. The other three values are unaffected.

- DistQLDPC, `data/matrices/README.md` at commit 3add5ab (11 Oct 2026), listing both codes with d = 16: [README.md at 3add5ab](https://github.com/guluchen/DistQLDPC/blob/3add5ab/data/matrices/README.md). The [[714,100]] entry was first added in commit 1e40928, the same day.
- Our record: version 1.1, [doi:10.5281/zenodo.23445463](https://doi.org/10.5281/zenodo.23445463); version 1.0, [doi:10.5281/zenodo.23379787](https://doi.org/10.5281/zenodo.23379787). The version 1.0 record now carries a note crediting DistQLDPC and pointing to version 1.1 (added 18 Oct 2026).

## A prior posting we missed: Lee's database entry for [[360,12]] = 24 predates our release (found 15 Oct 2026, after publishing) {#w-lee360}

On 13 Oct we published the exact distance 24 for IBM's [[360,12]] bivariate bicycle code and called it new; our note said the best posted lower bound was 16. On 15 Oct we found that Gideon Lee's public database bicycle-race, first released on 11 Oct 2026, already lists this code (from Bravyi et al.'s Table 3) with distance 24, "exact-recomputed-here". We had already cited Lee's companion paper but did not inspect the database it links. This was the first item on this page caught after publishing rather than before. We withdraw the novelty claim; our result is now described as an independent recomputation, the Zenodo record gets a new version saying so, and every code novelty check now includes GitHub code databases.

- Lee's database, first release (commit aed705a, 11 Oct 2026), file `data/literature/status_v8.jsonl`, line 6: [status_v8.jsonl at aed705a, line 6](https://github.com/gideonlsx/bicycle-race/blob/aed705a/data/literature/status_v8.jsonl#L6).
- Our record: [doi:10.5281/zenodo.23342751](https://doi.org/10.5281/zenodo.23342751).

## A related posting we missed: Shukla's 231-vertex graph on the same sphere (credited on this site 15 Oct 2026, after publishing) {#w-shukla}

On 8 Oct 2026 we published a 228-vertex 5-chromatic unit-distance graph on the sphere of radius cos(π/10). The description of that record omitted closely related work by Chandan Kumar Shukla. His preprint, posted on 8 October 2026, the same calendar date as our deposit, reports a 231-vertex vertex-critical 5-chromatic graph with 938 edges on this sphere, obtained by SAT-based vertex minimisation of the 372-vertex graph of Voronov, Neopryatnaya and Dergachev, and a 961-vertex vertex-critical 5-chromatic graph on the second icosahedral sphere. The 231-vertex graph in our package has 924 edges, so it is a different graph. The Zenodo description was updated on 18 Oct 2026 to credit his preprint and to reword the sentence about Voronov et al.; the package itself is unchanged.

- Shukla, Preprints.org 202610.0589: [doi:10.20944/preprints202610.0589.v1](https://doi.org/10.20944/preprints202610.0589.v1).
- Our record: [doi:10.5281/zenodo.23241819](https://doi.org/10.5281/zenodo.23241819).

## A quantum code distance already found by Liang et al. (14 Oct 2026) {#w-bb18}

An overnight run computed the exact distance 18 of the [[248,10]] "bb18" code listed in the 10,000-atom paper of Cain, Preskill, Bluvstein et al. (printed there as at most 18), and two separately written programs agreed. Our literature check said the qLDPC challenge board had no entry for it. A fuller novelty sweep later that day found that the same code, up to an equivalence we checked, appears with exact distance 18 in Liang, Liu, Song and Chen (PRX Quantum, 2025), and that the board has listed it since July 2026. The claim of a new result was dropped before release; the computation stays in the released package as a reproduction of their value. The board file is `248-10-18.json`. Our board checks now use the repository's full file index for every code size.

- Liang et al., [arXiv:2503.03827](https://arxiv.org/abs/2503.03827), Table 3.
- The released package lists it as a control: [doi:10.5281/zenodo.23379787](https://doi.org/10.5281/zenodo.23379787).

## A claimed 63 for Erdős #188 (2 Oct 2026) {#w-188-63}

The search reported a coloring whose longest blue run, on its sample of lines, was 63, which would have given k ≤ 64. The rigorous verifier (Method 2) failed on it in 14,013 direction boxes, and it contains blue runs of at least 68 points: the search had over-fitted its own sample. It was never announced. The search score was replaced by the verifier itself.

- Published note, section "How the coloring was found", and the package file `upper_bound/logs/m63_NJ64.utf8.txt`: [doi:10.5281/zenodo.23151059](https://doi.org/10.5281/zenodo.23151059).
- Ledger, 2 Oct 2026: [ledger_extract, L607-619](ledger_extract.html#L607).

## A small-disk 5-chromatic unit-distance graph (20 Sep 2026) {#w-polymath}

Another AI session produced a certified 5-chromatic unit-distance graph in a small disk, and ChatGPT rated it potentially new. Within minutes a prior-art search found a smaller one by Parts in the Polymath16 thread (February 2021). Marked NOT NEW.

- Ledger: [ledger_extract, L16](ledger_extract.html#L16).
- Timeline: [log_quotes, "found to be already known"](log_quotes.html#t-polymath).

## A construction overtaken by Tomon's paper (5 Oct 2026) {#w-tomon}

One theorem prepared for release was already implied by a paper of István Tomon posted on 2 October 2026, found on 5 October before anything was released. The theorem was dropped and the paper cited.

- Tomon, [arXiv:2610.03517](https://arxiv.org/abs/2610.03517), Theorem 1.3 and Corollary 1.4.
- Ledger, `LEDGER.md` line 657, verbatim with redactions:

> - 10-05 ~01:00 CDT TOMON arXiv 2610.03517 (2 Oct 2026; Thm 1.3 / Cor 1.4) [redacted: unreleased result] is SUBSUMED. [redacted: unreleased result]

## Higher-dimension claims overtaken by Davies's paper (9 Oct 2026) {#w-davies}

A note extending OpenAI's planar transfer argument originally claimed new lower bounds for the chromatic number of R^n for every n from 3 to 11. AI referees (ChatGPT, Gemini and separate Claude reviewers) passed the argument, but a separate literature check, run just before release, found a paper by James Davies posted the day before that proves stronger results for dimension 4 and up, unconditionally. The note was cut to dimension 3, the case his paper does not cover, and credits him before it was released on 10 October.

- Davies, [arXiv:2610.12301](https://arxiv.org/abs/2610.12301) (8 Oct 2026), Theorem 1.1 and Table 1.
- The released note, "Related work" paragraph: [doi:10.5281/zenodo.23273952](https://doi.org/10.5281/zenodo.23273952).

## A better bound for Graham's $100 problem, already beaten (10 Oct 2026) {#w-graham}

An overnight run certified a new lower bound for Erdős problem #1186 (Graham's $100 problem: in every 2-coloring of 1..n, how many one-color 3-term arithmetic progressions must there be?). It improved the published 0.0511 to 0.0527, with an exact certificate that passed two checkers. A blind reviewer then found a proof claim posted five days earlier on the problem's proof-claims page by Carlos Toledo, who reports the exact value 117/2192. The search had read the problem page but not its proof-claims page. Dropped. Every novelty check now includes the proof-claims page.

- Toledo's claim: [erdosproblems.com/forum/thread/1186/proof-claims](https://www.erdosproblems.com/forum/thread/1186/proof-claims) (5 Oct 2026; [doi:10.5281/zenodo.23171167](https://doi.org/10.5281/zenodo.23171167)).
- Ledger, `LEDGER.md` line 761: "NOT NOVEL ... NT9's novelty check missed the proof-claims page."

## Bounds for rational spaces, overtaken by Davies's paper (10 Oct 2026) {#w-qn}

The same night produced correct, checked lower bounds for the number of colors needed for rational space Q^n (at least 11 for n = 5, 15 for n = 6, 25 for n = 7). A blind checker confirmed the proofs, and then pointed out that Davies's paper proves that rational and real space need the same number of colors from dimension 5 up, with much larger values. Dropped. This was the second time in two days that the same new paper overtook our work, so new papers in the area are now read in full before any follow-up search starts.

- Davies, [arXiv:2610.12301](https://arxiv.org/abs/2610.12301), Theorem 1.1.
- Night log, `NIGHT_2026-10-10.md` line 52: "QBLIND NOVELTY KILL: Davies ... gives chi(Q^d) = chi(R^d) ..."

## A value already proved by Cabello (30 Sep 2026) {#w-cabello}

One exact value I had computed was already proved by Adán Cabello in 2012. Dropped.

- Cabello, [arXiv:1112.5149](https://arxiv.org/abs/1112.5149), Theorem 2.
- Release tracker (`RELEASE_TRACKER.md`, line 28), verbatim with redactions:

> **09-30: [redacted: unreleased result] is KNOWN (Cabello 2012, arXiv 1112.5149 Thm 2) - not ours.**

## Table entries that followed from published graphs (29 Sep 2026) {#w-ckr}

Entries of a table I first counted as new followed from graphs that Cherkashin, Kulikov and Raigorodskii had already published. An adversarial reviewer agent recomputed every entry and read the sources; those entries are no longer counted as new.

- Error log of the case-study draft (`case_study/v04_parts/C_errors.md`, row 10), verbatim with redactions:

> **[redacted: unreleased result] over-claimed.** [redacted: unreleased result] "OURS-routine" cells follow from Cherkashin–Kulikov–Raigorodskii graphs plus a trivial bound. It recomputed all [redacted: unreleased result] cells and read the sources. A new status, IMPLIED, was introduced.
