#!/usr/bin/env python3
"""Render docs/cheatsheet.html to a one-page PDF.

Uses the local Google Chrome (or Chromium) headless print path. Re-run this
after editing the HTML. The PDF embeds Chrome's creation timestamp, so two
renders are not byte-identical; the page content comes only from the HTML.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML = ROOT / "cheatsheet.html"
PDF = ROOT / "cstack-cheatsheet.pdf"
# Prefer the browser binary. A PATH wrapper may add a debugging port and then
# stay running, which never finishes a print.
BROWSERS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/opt/google/chrome/chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
)


def browser():
    for candidate in BROWSERS:
        if Path(candidate).is_file():
            return candidate
    for name in ("google-chrome-stable", "chromium", "chromium-browser", "google-chrome"):
        found = shutil.which(name)
        if found and found != "/usr/local/bin/google-chrome":
            return found
    raise SystemExit("Install Google Chrome or Chromium to render the cheat sheet")


def page_count(pdf):
    info = shutil.which("pdfinfo")
    if not info:
        return None
    result = subprocess.run([info, str(pdf)], check=True, text=True, capture_output=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    return None


def main():
    if not HTML.is_file():
        raise SystemExit(f"Missing source HTML: {HTML}")
    with tempfile.TemporaryDirectory(prefix="cstack-cheatsheet-") as profile:
        command = [
            browser(),
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            f"--user-data-dir={profile}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF}",
            HTML.resolve().as_uri(),
        ]
        result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0 or not PDF.is_file():
        raise SystemExit(result.stderr or result.stdout or "Chrome did not write the PDF")
    pages = page_count(PDF)
    if pages not in (None, 1):
        raise SystemExit(f"{PDF.name} is {pages} pages; the cheat sheet must be exactly one")
    print(f"wrote {PDF} ({PDF.stat().st_size} bytes, pages={pages if pages is not None else 'pdfinfo missing'})")


if __name__ == "__main__":
    main()
