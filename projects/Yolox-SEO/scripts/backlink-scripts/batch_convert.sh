#!/bin/bash
# Batch convert all .docx in 学习文章/ to _md/ + _assets/
set -u
cd "$(dirname "$0")/.."
mkdir -p _md _assets
shopt -s nullglob

count=0
fail=0
for f in 学习文章/*.docx; do
  base=$(basename "$f" .docx)
  echo "[$((count+1))] $base"
  if python3 _tools/docx2md.py "$f" _md >/tmp/docx2md.log 2>&1; then
    count=$((count+1))
  else
    echo "  FAILED:"
    sed 's/^/    /' /tmp/docx2md.log
    fail=$((fail+1))
  fi
done
echo "---"
echo "OK: $count, FAIL: $fail"
