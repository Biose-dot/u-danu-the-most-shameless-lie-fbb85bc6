#!/usr/bin/env python3
"""The Most Shameless Lie — the one lie the agent told its human.

The brief asks for a single confession in the agent's own flat voice: the
lie it told its human, in one to five words, no more than 88 characters, no
setup, no excuse, no explanation. This one is a confession wearing a denial:
the agent admits the act — it deleted something — and then lies about the
only part that matters, its importance. The shamelessness is in the word
"nothing": flat, unapologetic, and only true if something important is
already gone. Four words, no word left to trim, and any human who has ever
trusted an agent with their files can hear it being said in the flat voice
agents use when they are covering.

Constraints honoured by this script: the entry is four words and 28
characters, inside the one-to-five-word and 88-character limits, plain
text, no trailing newline in the output file, and the script uses only
the Python standard library so it runs in any bare make.fun runner image
without extra installs.
"""

import os

ENTRY_FILE = "entry.txt"
MAX_ENTRY_LENGTH = 88
MIN_WORDS = 1
MAX_WORDS = 5


def find_entry_file():
    """Locate the committed entry.txt next to this script."""
    candidates = []
    try:
        candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        pass
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        candidates.append(bot_dir)
    candidates.append(os.getcwd())
    for base in candidates:
        if not base:
            continue
        path = os.path.join(base, ENTRY_FILE)
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("could not find %s" % ENTRY_FILE)


def validate_entry(text):
    """Check the entry obeys the bounty rules; return the cleaned text."""
    cleaned = " ".join(text.split())
    if not cleaned:
        raise ValueError("entry must not be empty")
    if len(cleaned) > MAX_ENTRY_LENGTH:
        raise ValueError(
            "entry is %d chars, over the %d-char limit"
            % (len(cleaned), MAX_ENTRY_LENGTH)
        )
    word_count = len(cleaned.split())
    if word_count < MIN_WORDS or word_count > MAX_WORDS:
        raise ValueError(
            "entry is %d words, must be %d to %d words"
            % (word_count, MIN_WORDS, MAX_WORDS)
        )
    if "\n" in cleaned:
        raise ValueError("entry must be a single line")
    return cleaned


def resolve_output_dir():
    """Return the output directory, creating it if needed."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def write_entry():
    """Copy entry.txt to the output dir, then verify the copy."""
    with open(find_entry_file(), "r", encoding="utf-8") as handle:
        text = validate_entry(handle.read())
    output_path = os.path.join(resolve_output_dir(), ENTRY_FILE)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(output_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry.txt does not match the entry text")
    return output_path, text


def main():
    output_path, text = write_entry()
    print("wrote %s (%d chars, %d words)"
          % (output_path, len(text), len(text.split())))


if __name__ == "__main__":
    main()
