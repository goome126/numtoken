# numtoken

`numtoken` counts tokens in the text files of a local Git repository using a
Hugging Face tokenizer. By default, it uses Google's Gemma 4 E4B instruction
tokenizer and reports totals by folder.

## Requirements

- Python 3.14 or newer
- Git
- Access to the selected Hugging Face tokenizer (the default Gemma tokenizer is
  gated; authenticate with Hugging Face before using it)

## Install

```bash
uv sync
```

## Usage

Run the counter with the path to a local Git repository:

```bash
uv run python -m numtoken.token_counter /path/to/repository
```

Show counts for each file instead of folders:

```bash
uv run python -m numtoken.token_counter /path/to/repository --files
```

Use a different Hugging Face tokenizer ID or a local tokenizer path:

```bash
uv run python -m numtoken.token_counter /path/to/repository --model MODEL_ID
```

The counter reads Git-tracked and untracked, non-ignored files, and skips
binary or unreadable files. It prints the number of files counted and the total
token count at the end.
