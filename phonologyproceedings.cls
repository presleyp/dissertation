%% phonologyproceedings.cls
%% This document is heavily adapted from Max Bane's cascadilla.cls,
%% which is part of the cascadilla proceedings project, available here:
%% https://github.com/maxbane/cascadilla.cls

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This LaTeX class provides an extension of the "article" document class that
% can be used to typeset papers for the proceedings of the AMP 2015 conference.  It was created by Claire Moore-Cantwell for the proceedings of Phonology 2013 (with minor modifications by Gunnar Ólafur Hansson).  
% Direct questions about preparing submissions for the AMP 2015 Proceedings to Gunnar Ólafur Hansson (gunnar.hansson@ubc.ca)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Identification

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{phonologyproceedings}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Class Options

\RequirePackage{ifthen}
\RequirePackage{ifpdf}

\ifpdf
    \ClassWarningNoLine{phonologyproceedings}
    {`pdflatex' may produce a PDF file that does not use \MessageBreak
     the Times Roman font, which is required by the \MessageBreak
     AMP 2015 stylesheet. You may wish to use `latex' \MessageBreak
     to generate a DVI file instead, and convert that to \MessageBreak
     PDF}
\fi




\newboolean{hyphenate}
\newboolean{copyright}
\setboolean{copyright}{true}
\newboolean{times}
\setboolean{times}{true}

\DeclareOption{hyphenate}{\setboolean{hyphenate}{true}}
\DeclareOption{nocopyright}{\setboolean{copyright}{false}}
\DeclareOption{notimes}{\setboolean{times}{false}}

\ProcessOptions \relax

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Package Loading

% We're just an extension of the built-in article class.
% The stylesheet requires US Letter paper and 10pt body fontsize
% (which is happily LaTeX's default fontsize)

\LoadClass[letterpaper]{article}
% Set up the margin widths/heights using the geometry package
\RequirePackage[letterpaper,left=1.25in,right=1.25in,top=1.0in,bottom=1.0in,foot=-1in]{geometry}

% Stylesheet requires Times Roman font
\ifthenelse{\boolean{times}}{
    \RequirePackage{times}
}{}

% Stylesheet requires the the first paragraphs of all sections be indented.
% The standardly available indentfirst package does that for us.
\RequirePackage{indentfirst}

% We'll need fancyhdr for typesetting the copyright notice, and the headers and footers
\RequirePackage{fancyhdr}

% We'll use titlesec to format section titles
\RequirePackage{titlesec}

% We use natbib for formatting the bibliography (plus a hacked .bst file)
\RequirePackage{natbib}

% Table/figure captions are labeled bold
\RequirePackage[labelfont=bf]{caption}

% Use covington package for example numbering
\RequirePackage{covington}

\RequirePackage{fancyhdr}
\pagestyle{fancy}
\footskip = 24pt
\textheight = 585pt

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Main Definitions

\newcommand{\blankline}{\quad\\}

% Booleans for whether various strings have been set
\newboolean{haveAuthor}
\newboolean{haveTitle}
\newboolean{haveInstitution}
\newboolean{haveShorttitle}
\newboolean{haveShortauthor}
\newboolean{haveCopyrightauthor}

\newboolean{afterPar}

% Commands for setting author, title, completed date, institution and copyright year
\renewcommand{\author}[1]{\gdef\@cascauthor{#1}\gdef\@author{#1}\setboolean{haveAuthor}{true}}
\renewcommand{\title}[1]{\gdef\@casctitle{#1}\gdef\@title{#1}\setboolean{haveTitle}{true}}
\newcommand{\shortauthor}[1]{\gdef\@shortauthor{#1}\setboolean{haveShortauthor}{true}}
\newcommand{\shorttitle}[1]{\gdef\@shorttitle{#1}\setboolean{haveShorttitle}{true}}
\newcommand{\completed}[1]{\gdef\@cascdate{#1}}
\newcommand{\institution}[1]{\gdef\@institution{#1}\setboolean{haveInstitution}{true}}
\newcommand{\copyrightyear}[1]{\gdef\@copyrightyear{#1}}
\renewcommand{\thanks}[1]{\def\thefootnote{\fnsymbol{footnote}}\footnotetext[1]{#1}}

% If authors have different affiliations, indicated by superscripts linking authors' names and institution titles (as shown in Example.tex), use \copyrightauthor{} to set a superscript-free author list for use in the copyright footnote
\newcommand{\copyrightauthor}[1]{\gdef\@copyrightauthor{#1}\setboolean{haveCopyrightauthor}{true}}


%% Redefine \maketitle
\renewcommand{\maketitle}{%
    \begin{center}
\blankline\blankline
        \ifthenelse{\boolean{haveTitle}}{
            \fontsize{18}{18}
            \selectfont
            \textbf{\@title}\\
            %\vspace{18pt}
            \ifthenelse{\boolean{haveAuthor}}{
                \fontsize{14pt}{16pt}
                \selectfont
                \blankline
            }
            \normalsize
            \selectfont
        }{}
    
        \ifthenelse{\boolean{haveAuthor}}{
            \fontsize{14pt}{14pt}
            \selectfont
            \@author
            \normalsize
            \selectfont
        }{}
    
        \ifthenelse{\boolean{haveInstitution}}{
            \vspace{-0.5pt}
            \normalsize
            \selectfont
            \emph{\@institution}
        }{}
        
        \blankline
    \end{center}
}


\lhead{\ifthenelse{\boolean{haveShortauthor}}{\@shortauthor}{
	\ifthenelse{\boolean{haveAuthor}}{\@author}{PLEASE ENTER AN AUTHOR}      }}
\chead{}
\rhead{\ifthenelse{\boolean{haveShorttitle}}{\@shorttitle}{
	\ifthenelse{\boolean{haveTitle}}{\@title}{PLEASE ENTER A TITLE}      }}
\lfoot{}
\rfoot{\thepage}
\cfoot{}
\renewcommand{\headrulewidth}{0.4pt} 


% We are using justified text *without* any hyphenation (i.e., only
% word and letter spacing). The following parameter settings discourage TeX's
% layout algorithm from breaking lines with syllabic hyphens. Can be suppressed
% by the "hyphenate" class option.
\ifthenelse{\boolean{hyphenate}}{}{
    \hyphenpenalty=5000
    \tolerance=1000
}

% Paragraph indents should be one quarter inch
\parindent=0.25in

% Footnotes should be set in 9pt, which is \small
\let\footnotesize\small

% Adjust footnotes so that numbers appear flush with margin.
% Implementation inspired by answers at:
% http://tex.stackexchange.com/questions/40976/align-footnote-mark-with-text-margin
\renewcommand{\@makefntext}[1]{%
  \settowidth{\@tempdima}{\@thefnmark} \parindent \dimexpr\@tempdima+.75em\relax%
  \noindent\makebox[1em][l]{\textsuperscript{\@thefnmark}}#1
}


% Reduce the spacing around captions in tables and figures
\setlength{\abovecaptionskip}{12pt}
\setlength{\belowcaptionskip}{-5pt}

% The following bit of code increases the size of the bottom margin on the
% first page only, to make room for the copyright statement
\ifthenelse{\boolean{copyright}}{
    \setlength{\textheight}{8.75in}
    \AtBeginDocument{\setlength{\textheight}{9in}}
}{}

% The first page of the article gets a copyright statement, as in
% the cascadilla stylesheet
% Suppressed by the "nocopyright" class option.
\newcommand\CascadillaCopyright {
    \fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[L]{\vspace{-0.2in}\small\copyright{}\ \@copyrightyear\ \ifthenelse{\boolean{haveCopyrightauthor}}{\@copyrightauthor}{\@author}\\Proceedings of \textit{AMP 2015}\\Completed \@cascdate}
    \renewcommand{\headrulewidth}{0pt}
    }
}
\ifthenelse{\boolean{copyright}}{
    \AtBeginDocument{\CascadillaCopyright{}}
    \AtBeginDocument{\thispagestyle{plain}}
}{}


% Tell natbib to indent hanging lines by a quarter inch
\setlength{\bibhang}{0.25in}

% Format section headings according to the stylesheet

\titlelabel{\thetitle\ }
\titleformat{\section}{\fontsize{12pt}{0}\bf}{\thesection}{1em}{}
\titleformat{\subsection}[runin]
{\fontsize{11pt}{0}\itshape}{\textnormal{\textbf{\thesubsection}}}{1em}{}
\titleformat{\subsubsection}[runin]
{\fontsize{11pt}{0}\itshape}{\textnormal{\textbf{\thesubsubsection}}}{1em}{}
\titlespacing{\section}{0pt}{11pt}{10pt}
\titlespacing{\subsection}{0pt}{11pt}{10pt}
\titlespacing{\subsubsection}{0pt}{11pt}{10pt}

% Commands for immediate subsections, which require different spacing than
% normal headings
\newcommand{\immedsubsection}[1]{\vspace{-9pt}\subsection{#1}}
\newcommand{\immedsubsubsection}[1]{\vspace{-9pt}\subsubsection{#1}}

% Provide a command for the bibliography
\newcommand{\cascadillabibliography}[1]{\small\renewcommand{\baselinestretch}{2}\bibliographystyle{cascadilla}\bibliography{#1}}

% Set up citation punctuation for, e.g., (Shosted, 2006:13).
\AtBeginDocument{
    \bibpunct[:]{(}{)}{;}{a}{,}{,}
}