# Nicholas M. Synovic — Resume

LaTeX source for my resume, with modular sections, BibLaTeX-managed publication records, and automated PDF builds through GitHub Actions.

[Website](https://nicholassynovic.github.io/) · [LinkedIn](https://www.linkedin.com/in/nsynovic) · [GitHub](https://github.com/NicholasSynovic)

## Get the PDF

The [Compile Resume workflow](https://github.com/NicholasSynovic/resume/actions/workflows/build-pdf.yml) builds the resume on every push and pull request and can also be triggered manually.

To download a compiled copy:

1. Open the workflow and select a successful run.
2. Download the `resume` artifact.
3. Extract the archive to access `main.pdf`.

PDF artifacts are retained for 30 days.

## Contents

The resume includes sections covering:

- Academic preparation
- Academic recognition
- Teaching experience
- Research and work
- Journal articles
- Conference papers
- Preprint manuscripts
- Presentations
- Media appearances
- Competitions
- Service

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yml       # Automated PDF compilation and artifact uploads
├── bibliography/
│   └── journals.bib        # Bibliography data loaded by main.tex
├── misc/
│   └── typesetting.tex     # Packages, formatting, and reusable commands
├── sections/               # Individual CV sections
├── LICENSE
└── main.tex                # Document entry point and contact information
```

Content and presentation are maintained separately: `main.tex` assembles the document, `sections/` holds the CV entries, and `misc/typesetting.tex` controls the layout.

## Build Locally

### Requirements

Install a LaTeX distribution with:

- pdfLaTeX
- `latexmk`
- Biber
- The packages used by the document: `geometry`, `fontenc`, `titlesec`,
  `enumitem`, `xurl`, `biblatex`, and `hyperref`

The bibliography uses BibLaTeX with the Biber backend.

### Compile

Clone the repository and build from its root directory:

```sh
git clone [https://github.com/NicholasSynovic/cv.git](https://github.com/NicholasSynovic/cv.git)
cd cv

latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode main.tex
```

The compiled document is written to `main.pdf`.

Alternatively, compile explicitly:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

### Clean Build Files

Remove intermediate compilation files while keeping the PDF:

```sh
latexmk -c main.tex
```

## Updating the CV

### Content

Edit the corresponding `.tex` file in `sections/`. To add or reorder sections, update the `\input{sections/...}` statements in `main.tex`.

Contact information and profile links are defined directly in `main.tex`.

### Publications

Update `bibliography/journals.bib` and the relevant publication section. Additional bibliography files can be registered in `main.tex` with `\addbibresource{...}`.

Bibliography entries are sorted by year descending, then name and title. DOI links are enabled; when an entry has a DOI, its URL field is suppressed in the rendered bibliography.

### Formatting

Edit `misc/typesetting.tex` to change margins, headings, list spacing, bibliography formatting, or reusable commands.

The document uses an 11-point article layout on US letter paper with 0.75-inch margins.

The `\cventry` command formats an institution or employer, location, position or degree, and dates:

```tex
\cventry
    {Institution or Employer}
    {Location}
    {Position or Degree}
    {Dates}
```

## Continuous Integration

GitHub Actions compiles `main.tex` using `xu-cheng/latex-action` and uploads the resulting PDF as the `curriculum-vitae` artifact.

If compilation fails, available `main.log` and `main.blg` files are uploaded as `latex-build-logs` and retained for 7 days.

See [the workflow configuration](.github/workflows/build.yml) for build settings.

## License

This repository includes the GNU Affero General Public License, version 3. See [LICENSE](LICENSE) for the full terms.
