#!/usr/bin/env python3
"""Convert the repository's LaTeX CV to main.docx using Pandoc."""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pandoc(*args, source=None):
    return subprocess.run(
        ["pandoc", *args],
        input=source,
        text=True,
        stdout=subprocess.PIPE,
        check=True,
        cwd=ROOT,
    ).stdout


def expand_inputs(path, parents=()):
    path = path.resolve()
    path.relative_to(ROOT)
    if path in parents:
        raise RuntimeError(f"Circular LaTeX input: {path}")
    text = path.read_text(encoding="utf-8")

    def replace(match):
        name = Path(match[1])
        if not name.suffix:
            name = name.with_suffix(".tex")
        return expand_inputs(ROOT / name, (*parents, path))

    return re.sub(r"\\input\s*\{([^}]+)\}", replace, text)


def namespace_ids(node, prefix):
    if isinstance(node, dict):
        if node.get("t") == "Div" and node["c"][0][0]:
            node["c"][0][0] = prefix + "-" + node["c"][0][0]
        for value in node.values():
            namespace_ids(value, prefix)
    elif isinstance(node, list):
        for value in node:
            namespace_ids(value, prefix)


def main():
    source = expand_inputs(ROOT / "main.tex")
    body = source.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    macros = r"""
\newcommand{\contactsep}{; }
\newcommand{\cventry}[4]{\par\textbf{#1}, #2\par\textit{#3}, #4\par}
"""
    bibliographies = {}

    def bibliography(match):
        resolved = []
        for name in match[1].split(","):
            path = Path(name.strip())
            if not path.suffix:
                path = path.with_suffix(".bib")
            file = (ROOT / path).resolve()
            file.relative_to(ROOT)
            if not file.is_file():
                raise FileNotFoundError(file)
            resolved.append(file)
        marker = f"DOCXBIB{len(bibliographies)}"
        doc = json.loads(
            pandoc(
                "--from=markdown",
                "--to=json",
                "--citeproc",
                *[f"--bibliography={file}" for file in resolved],
                source='---\nnocite: "@*"\n---\n',
            )
        )
        blocks = []
        for block in doc["blocks"]:
            if block["t"] == "Div" and block["c"][0][0] == "refs":
                blocks.extend(block["c"][1])
            else:
                blocks.append(block)
        namespace_ids(blocks, marker)
        bibliographies[marker] = blocks
        return "\n\\section*{" + marker + "}\n"

    body = re.sub(
        r"\\begin\{refsection\}\s*\[([^\]]+)\].*?\\end\{refsection\}",
        bibliography,
        body,
        flags=re.S,
    )
    if r"\printbibliography" in body or r"\begin{refsection}" in body:
        raise RuntimeError(
            "Unsupported bibliography structure; update the DOCX converter"
        )
    doc = json.loads(pandoc("--from=latex", "--to=json", source=macros + body))
    blocks = []
    inserted = set()
    for block in doc["blocks"]:
        if block["t"] == "Header":
            inlines = block["c"][2]
            if len(inlines) == 1 and inlines[0]["t"] == "Str":
                marker = inlines[0]["c"]
                if marker in bibliographies:
                    blocks.extend(bibliographies[marker])
                    inserted.add(marker)
                    continue
        blocks.append(block)
    if inserted != set(bibliographies):
        raise RuntimeError("Some bibliography placeholders were not replaced")
    doc["blocks"] = blocks
    pandoc(
        "--from=json",
        "--to=docx",
        "--standalone",
        "--output=main.docx",
        source=json.dumps(doc),
    )
    output = ROOT / "main.docx"
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("DOCX output is missing or empty")


if __name__ == "__main__":
    main()
