# AGENTS.md

LaTeX resume built to PDF (LaTeX + Biber) and DOCX (Pandoc). No package
manager, tests, or linters: **verify changes by compiling both outputs.**

Entry point is `main.tex`: contact info inline, four sections `\input` from
`sections/` (experience, education, selected-publications, technical-skills).

## Build and verify

CI builds both formats on every push/PR. Run both before committing:

```sh
# PDF; runs pdflatex + biber automatically (biblatex backend=biber)
latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode main.tex

# DOCX; requires pandoc on PATH (CI pins 3.14)
python3 scripts/build_docx.py

# Remove build intermediates (keeps main.pdf)
latexmk -c main.tex
```

- PDF needs a TeX distribution with latexmk + Biber. DOCX needs `pandoc` on PATH (CI pins 3.14); the script is stdlib-only Python 3 and writes `main.docx`.
- No `.gitignore`: clean intermediates and build artifacts (`main.aux`, `main.log`, `main.docx`, …) show as untracked — never commit them.

## Structure

- `main.tex` — entry point: contact header, section order via `\input`.
- `misc/typesetting.tex` — all packages, formatting, and custom commands (`\cventry`, `\contactsep`).
- `sections/*.tex` — one resume section each; Selected Publications draws from `bibliography/*.bib`.
- `scripts/build_docx.py` — converts the expanded LaTeX to DOCX; re-implements the custom macros for pandoc.

## scripts/build_docx.py is structure-coupled

- It redefines only `\contactsep` and `\cventry` for the conversion. A new command from `misc/typesetting.tex` used in sections breaks the build until it is added to the script's `macros` block.
- Bibliographies are handled only as `\begin{refsection}[bibliography/x.bib,...]...\end{refsection}` blocks; anything else raises "Unsupported bibliography structure".
- Each refsection must contain `\nocite`; the DOCX renders exactly what it selects — `\nocite{*}` renders the whole `.bib` (to hide an entry, remove it from the `.bib`), explicit keys render just those. PDF and DOCX agree.
- Only the body between `\begin{document}` and `\end{document}` is converted, so preamble changes don't affect DOCX output.

## Bibliography

- `sections/selected-publications.tex` renders explicit keys via `\nocite` inside a `refsection` over `conferences.bib` and `preprints.bib`. Adding an entry to a .bib file does nothing until its key is listed in `\nocite` — in both PDF and DOCX builds. `journals.bib` and `presentations.bib` are currently unused.
- biblatex options (authoryear, `sorting=ydnt`, DOI shown with URL suppressed when a DOI exists, `maxbibnames=99`) live in `misc/typesetting.tex`; hyperref must load after biblatex.

## Conventions

- Starred headings (`\section*{...}`); `\cventry{Institution}{Location}{Position/Degree}{Dates}` with spaced en-dashes (`2024 -- Present`).

## Releases

Pushing any tag publishes `NicholasMSynovic_resume.pdf`/`.docx` to a GitHub
Release. Tags are created by the owner only on request — never push tags.
Branch-run artifacts are named `curriculum-vitae` / `curriculum-vitae-docx`.

See README.md for user-facing setup and update instructions.
