"""The One-Liner Groan-Off.

One original dad joke, at most 140 characters, written to be told out
loud at the dinner table.

Standard library only. Deterministic: no randomness, no network, no
clock. The entry is the joke at CANDIDATES[SELECTED], written to
<MAKEFUN_OUTPUT_DIR>/entry.txt (default /output/entry.txt), then read
back and validated (1-140 characters, one line, not only whitespace)
before exiting.

Verification: after writing, verify_written_bytes() reads the file back
as raw bytes and checks it decodes to exactly the joke that was chosen,
so a partial write, a stray newline, or an encoding slip fails loudly
instead of shipping a broken entry to the judge.
"""

import os

CANDIDATES = [
    "I keep a hammer in the fridge so I can nail the cold cuts.",
    "My son asked why the car was in the oven. I told him I wanted a hot rod.",
    "I put my watch in the blender. Now it is just a matter of time.",
    "My sourdough starter left me a note. It said it needed space to rise.",
    "My daughter asked why the pillow was on the roof. I said it wanted to sleep on it.",
    "I told my son the vacuum cleaner quit. He asked why. I said it was just collecting dust.",
    "My wife asked why I talk to the lawn. I said I am trying to get to the root of our problems.",
    "My son asked why I brought a pencil to the restaurant. I said in case I had to draw the check.",
    "My kid asked why the boat was in the garage. I said it is just going through a dry spell.",
    "I asked the keyboard why it was so stressed. It said too many keys and no escape.",
]

# The sharpest cut: a hammer in the fridge so the dad can nail the cold
# cuts. The pun fires twice in the last four words (nail = what a hammer
# does; cold cuts = the deli meat that lives in the fridge), the setup is
# one odd, funny image, and nothing needs explaining. It beat the hot-rod
# candidate (a known pun pairing, a step down on freshness) and the
# matter-of-time one (a familiar idiom doing the work) on freshness and
# tightness: 58 characters, no wasted words, and a dinner-table joke in
# the most literal sense — it is about what is in the fridge at dinner.
SELECTED = 0


def verify_written_bytes(path: str, expected: str) -> str:
    """Read path back as raw bytes and check it is exactly expected.

    Returns the decoded text. Raises AssertionError on any mismatch:
    wrong bytes, undecodable UTF-8, wrong length, a newline sneaking in,
    or whitespace-only content.
    """
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    assert text == expected, "written bytes do not match the entry"
    assert 1 <= len(text) <= 140, "written entry must be 1-140 characters"
    assert "\n" not in text, "written entry must be a single line"
    assert text.strip(), "written entry must not be only whitespace"
    return text


def main() -> None:
    joke = CANDIDATES[SELECTED].strip()
    assert "\n" not in joke, "entry must be a single line"
    assert 1 <= len(joke) <= 140, "entry must be 1-140 characters"
    assert joke.strip(), "entry must not be only whitespace"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(joke)

    text = verify_written_bytes(path, joke)
    print(f"wrote {path} ({len(text)} characters)")


if __name__ == "__main__":
    main()
