<!-- this_file: TODO.md -->

# TODO

The 2026 modernization pass is done (see `CHANGELOG.md`). Remaining ideas:

## Nice to have
- [ ] Migrate the flat `gimeltra/` package to a `src/gimeltra/` layout to match
      the portfolio template. Keep the data files and entry point working.
- [ ] Add a `--to-script`/`-o` validation error that lists valid codes when an
      unknown script code is passed (currently unknown targets pass through).
- [ ] Add a JSON/round-trip fuzz test that converts a corpus through every
      script pair and checks for crashes.
- [ ] Publish to PyPI (the `release.yml` workflow is ready; needs the PyPI
      trusted-publisher / environment configured).
- [ ] Consolidate the legacy root `_config.yml` + `Gemfile` Jekyll setup with
      the new `docs/` site (decide which GitHub Pages source to serve).

## Data
- [ ] Document any known gaps in the TSV per script (letters without a mapping).
- [ ] Add a validity check in `update.py` that flags duplicate or conflicting
      cluster rules when regenerating the JSON.
