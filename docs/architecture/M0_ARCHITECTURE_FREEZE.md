# M0 — Product Thesis & Architecture Freeze

**Project:** PAMILANGA EVIDENCE  
**Version:** v0.1  
**Status:** FROZEN  
**Freeze date:** 2026-10-03

## Thesis

> Autonomous systems can make decisions. We make those decisions provable.

## Product architecture

**TRACE** — captures evidence events while preserving provenance, timing, ordering, and integrity.

**REPLAY** — reconstructs recorded runs and identifies the earliest meaningful behavioural divergence.

**PROVE** — builds evidence relationships, records supported causal hypotheses, evaluates evidence sufficiency, and emits an Evidence Object.

**ASSURE** — compares evidence across runs and exposes recurring divergence and evidence gaps.

## Technical chain

Capture → Provenance & Temporal Integrity → Evidence Graph → First Divergence → Causal Hypotheses → Deterministic / Counterfactual Replay → Evidence Sufficiency → Evidence Object

## Epistemic invariants

- OBSERVED != DERIVED != HYPOTHESIS.
- FIRST DIVERGENCE != ROOT CAUSE.
- Missing evidence must remain visible.
- Event time and capture time must remain distinct.
- Claims must not exceed available evidence.

## v0.1 demonstrator

A domain-neutral Physical AI validation rig will produce a nominal run (RUN-N01) and a controlled failure run with a stale observation. TRACE records the chain; later stages reconstruct and compare it.

## M0 exit

Product boundary, module responsibilities, Evidence Event contract, Evidence Object contract, demonstrator scenario, and initial validation protocol are frozen for v0.1.

Changes after this point require implementation or validation evidence.
