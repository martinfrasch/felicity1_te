# Replace documentclass
s/\\documentclass\[.*\]{Definitions\/mdpi}/\\documentclass[10pt,a4paper]{article}/

# Remove MDPI internal commands (lines 28-46 range)
/^\\firstpage{/d
/^\\makeatletter/d
/^\\setcounter{page}{\\@firstpage}/d
/^\\makeatother/d
/^\\pubvolume{/d
/^\\issuenum{/d
/^\\articlenumber{/d
/^\\pubyear{/d
/^\\copyrightyear{/d
/^\\datereceived{/d
/^\\daterevised{/d
/^\\dateaccepted{/d
/^\\datepublished{/d
/^\\hreflink{/d
/^%\\externaleditor{/d
/^%\\datecorrected{/d
/^%\\dateretracted{/d

# Replace Title command
s/\\Title{/\\title{/

# Keep TitleCitation but comment it out
s/^\\TitleCitation{/%\\TitleCitation{/

# Replace Author command
s/^\\Author{/\\author{/

# Comment out AuthorNames
s/^\\AuthorNames{/%\\AuthorNames{/

# Comment out address command (will be in author)
s/^\\address{/%\\address{/

# Comment out corres
s/^\\corres{/%\\corres{/

# Replace abstract environment
s/^\\abstract{/\\begin{abstract}/
s/^}$/\\end{abstract}/

# Replace keyword
s/^\\keyword{/\\textbf{Keywords:} /
