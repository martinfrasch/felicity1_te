# arXiv Submission: MDPI Template Conversion - CONFIRMED WORKING ✅

**Date**: December 24, 2024  
**Status**: Successfully submitted to arXiv and accepted

## Problem

arXiv rejects manuscripts using MDPI template due to:
- Line numbers in margins (from `submit` option in documentclass)
- Cannot process `Definitions/` subdirectory structure
- MDPI-specific LaTeX commands not available on arXiv servers

## ✅ SUCCESSFUL SOLUTION

### Approach: Surgical Conversion to Standard Article Class

Convert MDPI template to standard `article` class while preserving 100% of scientific content.

### Step-by-Step Process That Works

#### 1. Extract from Overleaf Ground Truth
- Use working Overleaf version as source of truth
- Ensures no content loss during conversion
- Extract clean copy before modifications

#### 2. Convert Document Class
```latex
FROM: \documentclass[bioengineering,article,submit,pdftex,moreauthors]{Definitions/mdpi}
TO:   \documentclass[10pt,a4paper]{article}
```

#### 3. Replace with Standard Packages
```latex
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amsthm}
\usepackage{wasysym}
\usepackage{color}
\usepackage{multirow}
\usepackage{url}
\usepackage[margin=1in]{geometry}
\usepackage[numbers,sort&compress]{natbib}
\usepackage{booktabs}
```

All these packages are standard and available on arXiv.

#### 4. Reconstruct Author Section
```latex
\author{Author1$^{1}$*, Author2$^{2}$, Author3$^{2,3}$\\
\\
\small $^{1}$Institution 1\\
\small $^{2}$Institution 2\\
\small $^{3}$Institution 3\\
\\
\small *Correspondence: email@example.com}
```

Convert from MDPI's `\Author{}` command to standard `\author{}`.

#### 5. Fix Unicode Characters (CRITICAL!)
```bash
# Replace multiplication symbol
sed -i 's/×/$\\times$/g' main_arxiv.tex

# Replace arrow symbol  
sed -i 's/→/$\\to$/g' main_arxiv.tex
```

Unicode characters will cause compilation failure on arXiv. Must convert to LaTeX commands.

#### 6. Remove MDPI-Specific Commands
- Remove `\reftitle{References}` (natbib handles this automatically)
- Remove any other MDPI template-specific commands
- Replace with standard LaTeX equivalents

#### 7. Fix Bibliography Commands
Ensure ONLY ONE instance of each at the END of document:
```latex
\bibliographystyle{plain}
\bibliography{fetus}
```

Remove any duplicate bibliography commands elsewhere in the file.

#### 8. Preserve ALL Figures
- Include all PDF figures from main manuscript
- **CRITICAL**: Include PNG supplement files (heatmaps, etc.)
- Verify all figures are copied to submission directory
- Do not assume any figure is unused without user confirmation

### Compilation Sequence

```bash
cd submission_directory
pdflatex main_arxiv.tex
bibtex main_arxiv
pdflatex main_arxiv.tex
pdflatex main_arxiv.tex
```

Should produce clean output with no errors or warnings.

### Final Package Structure

```
arxiv_submission.zip
├── main_arxiv.tex          (converted manuscript)
├── fetus.bib               (bibliography database)
├── figure1.pdf             (main figures)
├── figure2.pdf
├── ...
└── supplement.png          (supplement figures)
```

**CRITICAL**: All files at root level, NO subdirectories!

### Verification Checklist

Before submitting to arXiv:
- ✓ No line numbers in output PDF
- ✓ All scientific content preserved (100%)
- ✓ All figures included (both PDF and PNG)
- ✓ All citations resolved correctly
- ✓ No compilation errors or warnings
- ✓ No Unicode character errors
- ✓ Standard packages only (no MDPI dependencies)
- ✓ Files at root level (flat structure)
- ✓ Clean compilation: pdflatex → bibtex → pdflatex → pdflatex

### Common Pitfalls to Avoid

1. **❌ Don't just change `submit` to `accept`**
   - arXiv still can't process MDPI template structure
   - Must fully convert to standard article class

2. **❌ Don't remove supplement figures**
   - User may need PNG files for supplement even if not in main text
   - Always verify with user before removing any figures

3. **❌ Don't ignore Unicode characters**
   - Characters like × and → will cause compilation failures
   - Must replace with LaTeX commands ($\times$, $\to$)

4. **❌ Don't create subdirectories**
   - arXiv expects flat file structure
   - No Definitions/, figures/, or other subdirectories

5. **❌ Don't leave duplicate bibliography commands**
   - Will cause "Illegal, another \bibdata command" error
   - Keep only one \bibliography{} at document end

### Why This Works

The MDPI template is fundamentally incompatible with arXiv because:
- It relies on custom class files in Definitions/ subdirectory
- It uses proprietary commands not in standard LaTeX
- arXiv's processing pipeline cannot handle template dependencies

**The only reliable solution is complete conversion to standard article class.**

Attempting partial fixes (like just removing line numbers while keeping MDPI template) will fail.

### Success Confirmation

**This approach was CONFIRMED WORKING on arXiv submission system on December 24, 2024.**

- ✅ Manuscript compiled successfully on arXiv servers
- ✅ No line number rejection
- ✅ No template incompatibility errors  
- ✅ No missing file errors
- ✅ All content preserved from original Overleaf version
- ✅ User confirmed submission accepted

### Key Formula for Success

```
Surgical conversion to article class
+ Unicode character fixes  
+ Standard packages only
+ Flat file structure
= arXiv submission success
```

### Files Generated

- `arxiv_FINAL_CLEAN.zip` - Final submission package
- `ARXIV_SUBMISSION_README.txt` - Detailed documentation
- `main_arxiv.tex` - Converted manuscript
- Output: 37-page PDF, 8.1 MB

This approach successfully resolved arXiv submission issues and resulted in accepted manuscript.
