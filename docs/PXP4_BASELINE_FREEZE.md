# PXP-4 Baseline Freeze

**Date**: 2026-07-16
**Pre-PXP-4 HEAD**: `8e2c2ef7f1836a0964af498e9b0ccb87d2ac663f`
**Origin/main HEAD**: `8e2c2ef7f1836a0964af498e9b0ccb87d2ac663f` (pushed)
**Branch**: `main`

## Baseline Tests

| Check | Result |
|---|---|
| 51 export pipeline tests | ALL PASS |
| Build | PASS (portal v1.0.3) |
| Validate pages | PASS (9 routes) |
| Validate public export | PASS (24 records, schema v1.0.0) |
| Git diff --check | No whitespace errors |

## Current Public Export

| Metric | Value |
|---|---|
| Eligible records | 24 |
| Schema version | 1.0.0 |
| Duplicate IDs | 0 |
| Forbidden fields | 0 |

## Registry Baseline

| Metric | Value |
|---|---|
| Live total | 627 |
| Published (current + public) | 24 |
| Remaining (draft + internal) | 603 |

## Git State

| Property | Value |
|---|---|
| Local HEAD | `8e2c2ef` |
| Origin/main HEAD | `8e2c2ef` |
| Pushed | Yes |
| Working tree | Clean (only pre-existing untracked migration artifacts) |
| Secrets committed | None |
| Browser profile gitignored | Yes |
