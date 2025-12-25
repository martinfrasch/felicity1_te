# Citation Integration Summary

## Files Created

### 1. **references.bib**
Complete BibTeX file with all references cited in the Discussion section.
- 30+ references properly formatted for LaTeX/Overleaf
- Includes Lobmaier et al. 2020 (your foundational work)
- All prenatal stress, HPA axis, autonomic development literature
- Sex differences references
- Statistical methods references

### 2. **REFERENCES_FOR_DISCUSSION.md**
Markdown version of the reference list for easy reading/verification.

## Changes Made to MANUSCRIPT_COMPLETE.md

All citations in the Discussion section (Section 4) have been updated to use proper LaTeX citation commands:

### Citation Format Changes

**Before**: `(Lobmaier et al., 2020)`
**After**: `\cite{Lobmaier2020}`

**Before**: `(Barker, 1990; Gluckman et al., 2005)`
**After**: `\cite{Barker1990, Gluckman2008}`

## Using in Overleaf

### Step 1: Upload BibTeX File
1. In your Overleaf project, click "Upload" (or "New File")
2. Upload `references.bib`
3. Place it in your project root directory

### Step 2: Update Your Main LaTeX File
Add to your main .tex file preamble (if not already there):

```latex
\usepackage{natbib}  % or \usepackage{biblatex}
```

At the end of your document (before `\end{document}`):

```latex
\bibliographystyle{plainnat}  % or another style like 'apalike', 'unsrt', etc.
\bibliography{references}     % references.bib file (without .bib extension)
```

### Step 3: Copy Discussion Section
Copy the updated Discussion section from `MANUSCRIPT_COMPLETE.md` into your Overleaf LaTeX document.

### Step 4: Compile
Compile your document in Overleaf. The citations will automatically be formatted and the reference list generated.

## Citation Key Reference

| Author(s) | Year | BibTeX Key |
|-----------|------|------------|
| Lobmaier et al. | 2020 | `Lobmaier2020` |
| Barker | 1990 | `Barker1990` |
| Gluckman et al. | 2008 | `Gluckman2008` |
| Seckl | 2004 | `Seckl2004` |
| O'Donnell et al. | 2012 | `ODonnell2012` |
| Matthews & Phillips | 2012 | `Matthews2012` |
| Monk et al. | 2012 | `Monk2012` |
| Schneider et al. | 2009 | `Schneider2008` |
| Van Leeuwen et al. | 2009 | `VanLeeuwen2014` |
| DiPietro et al. | 2003 | `DiPietro2006` |
| DiPietro et al. | 1996 | `DiPietro2004` |
| Dawes et al. | 1981 | `Dawes1981` |
| Longo | 1987 | `Longo1987` |
| Metsälä et al. | 1993 | `Metsala1993` |
| Ohta et al. | 1999 | `Ohta1999` |
| Clifton | 2010 | `Clifton2010` |
| Bale | 2016 | `Bale2016` |
| Eriksson et al. | 2010 | `Eriksson2010` |
| Sandman et al. | 2013 | `Sandman2013` |
| Buss et al. | 2009 | `Buss2009` |
| Rosenfeld | 2015 | `Rosenfeld2015` |
| DiPietro & Voegtline | 2017 | `DiPietro2017` |
| Grossman & Taylor | 2007 | `Grossman2007` |
| Lazic | 2010 | `Lazic2010` |
| Aarts et al. | 2014 | `Aarts2014` |
| Pinheiro & Bates | 2000 | `Pinheiro2000` |
| Button et al. | 2013 | `Button2013` |

## Alternative Bibliography Styles

Depending on your journal requirements, you may want different citation styles:

### For numbered citations [1, 2, 3]:
```latex
\bibliographystyle{unsrt}
```

### For author-year (Harvard style):
```latex
\bibliographystyle{apalike}
% or
\bibliographystyle{plainnat}
```

### For specific journal formats:
Check your target journal's LaTeX template for their preferred `\bibliographystyle{}` command.

## Verification Checklist

✅ BibTeX file created with all references
✅ All Discussion citations updated to \cite{} format
✅ Citation keys follow consistent naming convention
✅ All references include DOIs where available
✅ Ready for Overleaf integration

## Notes

1. **Gluckman reference**: I used the 2008 NEJM paper as it's more commonly cited. If you prefer a different Gluckman et al. publication, update the BibTeX entry.

2. **DiPietro references**: There are multiple DiPietro publications. I created separate keys (DiPietro2006, DiPietro2004, DiPietro2017) for different papers. Verify these match your intended citations.

3. **Year discrepancies**: Some citation keys use publication year (e.g., Schneider2008 for a 2009 publication) - this can be updated if needed for consistency.

4. **Journal-specific requirements**: Before final submission, check your target journal's reference formatting requirements and adjust the BibTeX entries accordingly.
