#!/usr/bin/env bash
set -euo pipefail
task_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
task_temp="$(mktemp -d -t codex-homework-XXXXXXXX)"
trap 'rm -rf -- "$task_temp"' EXIT
for task_source in "$task_dir"/Homework*.tex; do
  cp -- "$task_source" "$task_temp/document.tex"
  if command -v xelatex >/dev/null 2>&1; then
    for task_pass in 1 2 3; do
      (cd "$task_temp" && xelatex -interaction=nonstopmode -halt-on-error -file-line-error document.tex > compiler.txt 2>&1) || { cat "$task_temp/compiler.txt"; exit 1; }
    done
  elif command -v tectonic >/dev/null 2>&1; then
    tectonic --keep-logs --outdir "$task_temp" "$task_temp/document.tex"
  else
    echo 'Install XeLaTeX (with ctex and Fandol) or Tectonic first.' >&2
    exit 1
  fi
  cp -- "$task_temp/document.pdf" "${task_source%.tex}.pdf"
  echo "Compiled: ${task_source%.tex}.pdf"
done
