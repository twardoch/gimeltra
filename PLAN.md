<!-- this_file: PLAN.md -->

# Gimeltra Plan

## Status

The 2026 modernization is complete: `pyproject.toml` + hatch-vcs, MIT license
metadata, typed and commented code, a 17-test pytest suite, ruff + mypy clean,
CI + release workflows, a refreshed README and Jekyll docs, and a project icon.
See `CHANGELOG.md` for the itemized list and `TODO.md` for remaining ideas.

## Future direction

### Packaging
- Adopt the `src/gimeltra/` layout used by the portfolio's golden Python
  template, without breaking the bundled data files or the `gimeltrapy` entry
  point.
- Complete the first PyPI publish via `release.yml` once trusted publishing is
  configured.

### Correctness
- Validate script codes at the CLI/API boundary and fail with a helpful message
  listing supported codes.
- Extend test coverage with a corpus-driven pass across every script pair to
  catch silent rule regressions in the TSV.

### Data quality
- Add integrity checks to `update.py` (duplicate/conflicting rules, unmapped
  letters) so a bad TSV edit fails loudly at generation time.
- Document per-script coverage gaps for contributors.

## Non-goals

Gimeltra stays a small, focused transliteration utility. No phonetic model, no
vocalisation, no REST API, no Docker image — those were speculative items from
the original plan and are intentionally dropped.
