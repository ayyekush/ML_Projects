\documentclass[letterpaper,11pt]{article}


\usepackage[scaled=0.9]{helvet} % Scale Helvetica font to 90% of its original size
\renewcommand{\familydefault}{\sfdefault}


\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{xcolor}
\input{glyphtounicode}

\definecolor{navyblue}{RGB}{0, 0, 128}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in} % Adjust left margin
\addtolength{\evensidemargin}{-0.5in} % Adjust right margin for even pages
\addtolength{\textwidth}{1in} % Increase text width
\addtolength{\topmargin}{-0.7in} % Adjust top margin
\addtolength{\textheight}{1.0in} % Increase text height

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in} % Set table column separation to zero

% Sections formatting
\titleformat{\section}{
  \vspace{-10pt}\scshape\raggedright\Large
}{}{0em}{}[\color{black}\titlerule \vspace{-7pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

\renewcommand{\textbf}[1]{{\fontseries{sb}\selectfont #1}}  % medium
%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item{
    {#1 \vspace{-2.5pt}}  % Adjust spacing after each resume item (affects items under experience/projects)
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item % Space before each subheading (affects each position under experience)
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt} % Space after each subheading (affects the overall height of the section)
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7.5pt} % Space after each sub-subheading
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt} % Space after each project heading
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-3.8pt}} % Space after each sub-item

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-3pt}} % Space after item list (affects the spacing below lists)

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

%----------HEADING----------
\begin{center}
    \Huge\textbf{\scshape Ashutosh Mishra} \\ \vspace{1pt} % Space after name
    \small +91-9752371766 \hspace{2pt} $|$ \hspace{2pt} 
    \href{mailto:ashutoshmishra61679@gmail.com}{\textcolor{NavyBlue}{\textbf{ashutoshmishra61679@gmail.com}}} \hspace{2pt} $|$ \hspace{2pt} 
    \href{https://www.linkedin.com/in/ashutosh-mishra97/}{\textcolor{NavyBlue}{\textbf{Linkedin}}} \hspace{2pt} $|$ \hspace{2pt}
    \href{https://github.com/ashugh12}{\textcolor{NavyBlue}{\textbf{GitHub}}} \hspace{2pt} $|$ \hspace{2pt}
    % \href{https://ashutoshmishra007.netlify.app/}{\textcolor{NavyBlue}{\textbf{Portfolio}}} \hspace{2pt} $|$ \hspace{2pt}
    \href{https://leetcode.com/u/SmpRrsnkBS/}{\textcolor{NavyBlue}{\textbf{Leetcode}}} \hspace{2pt} $|$ \hspace{2pt}
    \href{https://codeforces.com/profile/ashutoshmishra61679}{\textcolor{NavyBlue}{\textbf{CodeForces}}} \hspace{2pt} $|$ \hspace{2pt}
    \href{https://www.codechef.com/users/coderashu23}{\textcolor{NavyBlue}{\textbf{CodeChef}}}
\end{center}


%-----------EXPERIENCE-----------
\large\section{\textcolor{NavyBlue}{\textbf{Experience}}}
  \resumeSubHeadingListStart
  \resumeSubheading
      {AI Product Engineer}{March 2025 - Present}
      {\href{https://www.clarityux.in/}{ClarityUX}}{Remote}
      \resumeItemListStart
    % \resumeItem{ \textbf{Tech Stacks}: Python, Javascript, Typescript, Figma, Google Gemini, OpenCV, NumPy}
    \resumeItem{Engineered an \textbf{AI-powered} Figma plugin for saliency mapping and attention prediction, visualizing user focus areas through real-time heatmaps with 150 plus positive feedback}
    
    \resumeItem{Accelerated design workflows by reducing UX testing time by \textbf{4–5 hours} per project via early-stage behavioral insights.}
    \resumeItem{Closed the gap between predicted and actual user behavior, enabling data-driven design decisions directly within Figma’s native environment}
      \resumeItemListEnd
    \resumeSubheading
      {Full-Stack Developer}{Nov 2024 - Feb 2025}
      {\href{https://www.linkedin.com/company/kuration-ai/}{Kuration AI}}{Remote}
      \resumeItemListStart
    % \resumeItem{ \textbf{Tech Stacks}: Python, FireStore}
    \resumeItem{Built and deployed \textbf{10+ }productivity tools for a B2B research agent, enhancing the precision and depth of market analysis with 70 percent accuracy}
    \resumeItem{Developed a robust DNS resolver with a \textbf{90} percent success rate in verifying website availability }
    
      \resumeItemListEnd
    % \resumeSubheading
    % {Student Backend Developer}{Jul 2024 - Present}
    %   {Result Generation Software}{Indore}
    %   \resumeItemListStart
    %     \resumeItem{ \textbf{Tech Stacks}: Java Springboot, MySQL}
    %      \resumeItem{ \textbf{Backend}: Authored the MySQL queries for database creation involves EDP User, to enable \textbf{Class-wise Grouping, Results, Category Management, Subject Offerings, CSV status, Subject Management, Course Management}}
    %   \resumeItemListEnd

  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\large\section{\textcolor{NavyBlue}{\textbf{Projects}}}
  \resumeSubHeadingListStart
      \resumeProjectHeading
          {\large\textbf{{\href{https://github.com/ashugh12/ChatWithMe}{\textbf{MetaChat-Chat App}}}} $|$ \emph{React.js, Express.js, Node.js, MongoDb, Socket.io, Tailwind, DaisyUI}}{\href{https://metachat-w40m.onrender.com/}{\textit{\textcolor{NavyBlue}{LiveLink}}}}
          \resumeItemListStart
            \resumeItem{Implemented real-time communication with Socket.io and secured API endpoints with JWT authentication}
            \resumeItem{Applied HTTP caching strategies for improved request validation and faster load times.}
            \resumeItem{Built responsive UI with modern design patterns, including emoji integration and animated feedback effects.}
          \resumeItemListEnd
      \resumeProjectHeading
          {\large\textbf{{\textbf{HackathonBot}}} $|$ \emph{JavaScript, Puppeteer}}{\href{https://github.com/ashugh12/Auto_Unstop}{\textit{\textcolor{NavyBlue}{GitHub}}}}
          \resumeItemListStart
            \resumeItem{Automated hackathon registration workflows using headless browser scripting.}
            \resumeItem{Utilized advanced selectors for data scraping and auto-screenshot generation for process verification.}
          \resumeItemListEnd
      \resumeProjectHeading
          {\large\textbf{{\textbf{RBAC-Role Based Access Control}}} $|$ \emph{React.js, Node.js, Express.js, MongoDb, JSON}}{\href{https://cerulean-stroopwafel-e7d9c6.netlify.app/}{\textit{\textcolor{NavyBlue}{LiveLink}}}}
          \resumeItemListStart
            \resumeItem{Developed user-role management with dynamic permissions for CRUD operations.}
            \resumeItem{Built a permission-based interface and simulated backend using JSON Server for rapid development.}
          \resumeItemListEnd
      \resumeProjectHeading
          {\large\textbf{{\textbf{Date MyEvent}}} $|$ \emph{React.js, Node.js, Express.js, MongoDb}}{\href{https://www.linkedin.com/feed/update/urn:li:activity:7261518123483205632/}{\textit{\textcolor{NavyBlue}{LinkedIn}}}}
          \resumeItemListStart
            \resumeItem{Integrated React Calendar for event date selection, enabling users to select, store, and display event dates with CRUD operations and multimedia attachments, ensuring data persistence across sessions.}
          \resumeItemListEnd
      \resumeProjectHeading
          {\large\textbf{{\textbf{Enrichify}}} $|$ \emph{React.js, Firebase, Flask, CoreSignalAPI}}{\href{https://aesthetic-banoffee-1caa79.netlify.app/}{\textit{\textcolor{NavyBlue}{LiveLink}}}}
          \resumeItemListStart
            \resumeItem{ Integrated Firebase Authentication for secure, OAuth-based Google sign-in.}
            \resumeItem{Built lead capture forms and displayed enriched business data by integrating with the CoreSignal API.}
            \resumeItem{Enhanced user engagement by combining real-time data enrichment with clean UI flow.}
          \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------ACHIEVEMENTS-----------
\large\section{\textcolor{NavyBlue}{\textbf{Achievements}}}
\begin{itemize}
    \setlength{\itemsep}{-0.4em} % Adjusts space between each achievement item (affects the list of achievements)
    \setlength{\parsep}{0em}    % Adjust space between paragraphs within the list
    \setlength{\topsep}{0em}     % Adjust space above and below the list of achievements
    \item Qualified Team at \textcolor{NavyBlue}{\textbf{MCTE Mhow Hackathon(AVINYA)}} : Created an IoT Device for ”No-Network Communications” using LoRa Module
    \item Selected twice for the Internal SIH hackathon (2023 and 2024)
    \item Secured global ranks 566, 296, 308 in  \textbf{\href{https://www.codechef.com/users/coderashu23}{\textcolor{NavyBlue}{CodeChef Starters 161, 162, 163(Rated)}} }respectively
    \item Accomplished \textbf{\href{https://drive.google.com/file/d/1EuAww53-yJL7buDX7aGHSMNWh1cSM2z9/view?usp=drive_link}{\textcolor{NavyBlue}{NINJA SLAYGROUND 2.0 : 21 Day Coding Challenge}}}
    \item Achieved Global ranking 2605 in \textbf{\href{https://drive.google.com/file/d/1EuAww53-yJL7buDX7aGHSMNWh1cSM2z9/view?usp=drive_link}{\textcolor{NavyBlue}{TCS-CodeVita}}} round 1 and Global Rank of 3170 in round 2
    
\end{itemize}

%-----------EDUCATION-----------
\large\section{\textcolor{NavyBlue}{\textbf{Education}}}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Institute of Engineering and Technology, DAVV}{Indore}
      {Bachelor of Engineering - Computer Engineering; CGPA: 9}{Nov 2022 - Present}
      \vspace{3pt}
  \resumeSubHeadingListEnd

%-----------SKILLS-----------
% \section{\textcolor{NavyBlue}{\textbf{Skills}}}
%   \resumeSubHeadingListStart
%     \resumeSubItem{\textbf{Skills:}}{Data Structure , Algorithms , OOP , OS , Computer Networks}\vspace{-1pt} % Space after languages sub-item
%     \resumeSubItem{\textbf{Languages:}}{Java, Python, C/C++, SQL (MySQL), JavaScript}\vspace{-1pt} % Space after languages sub-item
%     \resumeSubItem{\textbf{Stack:}}{Database(MySQL, MongoDB), Backend(Node.js, Java), Frontend(React)}\vspace{-1pt} % Space after tools sub-item
%     \resumeSubItem{\textbf{Libraries:}}{Puppeteer, Socket.i}\vspace{-1pt} % Space after frameworks sub-item
    
%   \resumeSubHeadingListEnd

%   Skills : Data Structure , Algorithms , OOP , OS , Computer Networks
% Programming Languages : C++, Python, Java , C#, Go, Scala, Kotlin
% Libraries : React.js, Spring Boot, pandas , Redux, node.js
% Databases : Postgres Sql, Mysql , Mongo DB, DynamoDB
% Platforms :Github, Visual Studio Code, PGadmin, Jira

\end{document}
   isko nai file banake copy kar dena..... overleaf me