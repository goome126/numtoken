#!/usr/bin/env python3
"""Count Gemma tokens in all git-tracked text files of a local repository."""
import argparse
import os
import subprocess
import sys

from transformers import AutoTokenizer

# Gemma tokenizers are gated on Hugging Face; run `huggingface-cli login` first.
DEFAULT_MODEL = "google/gemma-4-E4B-it"


def repo_files(repo: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
    ).stdout
    return [p for p in out.decode("utf-8", errors="replace").split("\0") if p]


def read_text(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None
    if b"\0" in data:  # binary file
        return None
    return data.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="Path to a local git repository")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="HF tokenizer id or local path")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.exists(os.path.join(repo, ".git")):
        print(f"Not a git repository: {repo}", file=sys.stderr)
        return 1

    tokenizer = AutoTokenizer.from_pretrained(args.model)

    total = 0
    counted = 0
    skipped = 0
    file_counts: dict[str, int] = {}
    dir_counts: dict[str, int] = {}
    for rel in repo_files(repo):
        path = os.path.join(repo, rel)
        if not os.path.isfile(path):
            continue
        text = read_text(path)
        if text is None:
            skipped += 1
            continue
        n = len(tokenizer(text, add_special_tokens=False)["input_ids"])
        total += n
        counted += 1
        file_counts[rel] = n
        parent = os.path.dirname(rel)
        while parent:
            dir_counts[parent] = dir_counts.get(parent, 0) + n
            parent = os.path.dirname(parent)

    print("\nTokens per folder:")
    for d, n in sorted(dir_counts.items()):
        print(f"{n:>10}  {d}/")

    print("\nTokens per file:")
    for f, n in sorted(file_counts.items()):
        print(f"{n:>10}  {f}")

    print(f"\nFiles counted: {counted} (binary/unreadable skipped: {skipped})")
    print(f"Total tokens:  {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
