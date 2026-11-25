#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s [ref]\nMove the v0 tag on origin to a commit on origin/main. Defaults to the tip of origin/main.\n' "${0##*/}"
}

if [[ $# -eq 1 && ( $1 == --help || $1 == -h ) ]]; then
    usage
    exit 0
fi

if [[ $# -gt 1 || ( $# -eq 1 && $1 == -* ) ]]; then
    usage >&2
    exit 2
fi

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

tag_ref=refs/tags/v0
main_ref=refs/remotes/origin/main
target_ref=${1:-$main_ref}

remote_tag=$(git ls-remote --refs origin "$tag_ref")
expected_oid=${remote_tag%%$'\t'*}

git fetch --no-tags origin "+refs/heads/main:$main_ref"
target_commit=$(git rev-parse --verify --end-of-options "$target_ref^{commit}")

if ! git merge-base --is-ancestor "$target_commit" "$main_ref"; then
    printf 'The target %s must be reachable from origin/main.\n' "$target_ref" >&2
    exit 1
fi

git push --force-with-lease="$tag_ref:$expected_oid" origin "$target_commit:$tag_ref"
