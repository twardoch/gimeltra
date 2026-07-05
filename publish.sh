#!/usr/bin/env bash
# this_file: publish.sh
# Build and publish to PyPI. Usually the release.yml workflow does this on a tag;
# run this only for a manual publish. Needs UV_PUBLISH_TOKEN (or ~/.pypirc).
set -euo pipefail
cd "$(dirname "$0")"

./build.sh
uv publish
