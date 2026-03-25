#!/usr/bin/env python3
"""Script 08: PDF build test with tectonic.

Creates a minimal stub .tex file, compiles, and deletes.
Session: Hugo
"""

import logging
import subprocess
from pathlib import Path

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)


def main():
    log.info("=" * 60)
    log.info("Script 08: Tectonic PDF Build Test")
    log.info("=" * 60)

    stub_dir = Path("analysis_note")
    stub_dir.mkdir(exist_ok=True)
    stub_path = stub_dir / "test_build.tex"

    # Create minimal stub
    stub_content = r"""\documentclass[11pt]{article}
\usepackage{amsmath}
\begin{document}
\section{Test}
This is a test build. The Lund jet plane density is:
\begin{equation}
  \rho(x, y) = \frac{1}{N_{\mathrm{jet}}} \frac{d^2 n}{dx\, dy}
\end{equation}
where $x = \ln(1/\Delta\theta)$ and $y = \ln(k_T / \mathrm{GeV})$.

A citation would go here~\cite{Dreyer:2018nbf} but we skip the bib for this test.
\end{document}
"""
    stub_path.write_text(stub_content)
    log.info("Created stub: %s", stub_path)

    # Compile with tectonic
    try:
        result = subprocess.run(
            ["tectonic", str(stub_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            log.info("Tectonic build SUCCEEDED")
            pdf_path = stub_dir / "test_build.pdf"
            if pdf_path.exists():
                log.info("PDF exists: %s (%.1f KB)", pdf_path, pdf_path.stat().st_size / 1024)
        else:
            log.info("Tectonic build FAILED (exit code %d)", result.returncode)
            log.info("stdout: %s", result.stdout[:500])
            log.info("stderr: %s", result.stderr[:500])
    except FileNotFoundError:
        log.info("tectonic not found in PATH")
    except subprocess.TimeoutExpired:
        log.info("tectonic timed out after 120s")

    # Clean up
    for ext in [".tex", ".pdf", ".aux", ".log"]:
        p = stub_dir / f"test_build{ext}"
        if p.exists():
            p.unlink()
            log.info("Deleted %s", p)

    log.info("\nTectonic test complete.")


if __name__ == "__main__":
    main()
