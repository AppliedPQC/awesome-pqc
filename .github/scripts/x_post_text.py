import os
import re
import sys

URL = "https://github.com/AppliedPQC/awesome-pqc"
X_LIMIT = 280
X_URL_WEIGHT = 23


def main():
    body = os.environ.get("BODY", "").replace("\r\n", "\n")
    m = re.search(r"^## X post[ \t]*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    if not m or not m.group(1).strip():
        sys.exit("no text under '## X post'")
    text = m.group(1).strip()
    weight = len(text) + 2 + X_URL_WEIGHT
    if weight > X_LIMIT:
        sys.exit(f"post is {weight} characters with the link; X allows {X_LIMIT}")
    print(f"{text}\n\n{URL}")


if __name__ == "__main__":
    main()
