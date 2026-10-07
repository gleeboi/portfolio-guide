import html, re
E = html.escape
SEC = [
("what-this-guide-does","What This Guide Does","What This Guide Does",""),
("what-you-will-build","What You Will Build","What You Will Build",""),
("three-person-workflow","The Three-Person Workflow","Three-Person Workflow",""),
("what-to-prepare","What to Prepare Before You Start","What to Prepare",""),
("step-1-give-chatgpt-your-information","Step 1: Give ChatGPT Your Information","ChatGPT","Step 1"),
("step-2-find-missing-information","Step 2: Ask ChatGPT to Find Missing Information","Missing Information","Step 2"),
("step-3-build-your-claude-prompt","Step 3: Ask ChatGPT to Build Your Claude Prompt","Claude Prompt","Step 3"),
("step-4-prepare-the-claude-workspace","Step 4: Open Claude and Prepare the Workspace","Claude Workspace","Step 4"),
("step-5-send-the-master-prompt","Step 5: Send the Master Website Prompt","Master Prompt","Step 5"),
("step-6-review-the-website","Step 6: Review the Website Claude Creates","Review","Step 6"),
("step-7-recruiter-technical-qa","Step 7: Ask Claude to Run a Recruiter + Technical QA","Recruiter + Technical QA","Step 7"),
("step-8-test-links-files-mobile","Step 8: Test Links, Files, Mobile and Content","Test Links & Files","Step 8"),
("step-9-understand-your-files","Step 9: Understand Your Website Files","Website Files","Step 9"),
("step-10-create-the-github-repository","Step 10: Create the GitHub Repository","GitHub Repository","Step 10"),
("step-11-upload-to-github","Step 11: Upload the Website to GitHub","Upload to GitHub","Step 11"),
("step-12-turn-on-github-pages","Step 12: Turn On GitHub Pages","GitHub Pages","Step 12"),
("step-13-open-and-test-the-live-website","Step 13: Open and Test the Live Website","Live Website","Step 13"),
("step-14-updating-the-website-later","Step 14: Updating the Website Later","Updating Later","Step 14"),
("troubleshooting","Troubleshooting: Common Problems","Troubleshooting",""),
("safe-changes","How to Ask Claude for Safe Changes","Safe Changes",""),
("gleeboi-worked-example","The GLEEBOI Worked Example","GLEEBOI Example",""),
("final-recruiter-checklist","Final Recruiter Checklist","Recruiter Checklist",""),
("screenshots-used","Screenshots Used in This Guide","Screenshots Used",""),
("final-workflow","Final Workflow: From CV to Live Portfolio","Final Workflow",""),
]
# screenshot slots: title|capture|show;show|why|real file (None = placeholder only)
SS = {
1:("Start a new ChatGPT conversation","ChatGPT → New chat","New chat button;empty conversation","Keeps the portfolio project in its own thread.",None),
2:("Upload your CV to ChatGPT","ChatGPT message box → + / attachment button","Attachment button;CV file attached","Shows where the CV is attached.","01-chatgpt-upload.png"),
3:("Send the information-extraction prompt","ChatGPT message box with the Step 1 prompt pasted","Pasted prompt;Send button","Shows the exact prompt going in with the CV.",None),
4:("Review ChatGPT's extracted information","ChatGPT reply with categorized CV data","Category headings;“Not provided” labels","Shows what a clean information layer looks like.","02-chatgpt-extraction.png"),
5:("Ask ChatGPT for missing information","ChatGPT reply with the Portfolio Information Checklist","A / B / C / D groups","Shows gaps found before building.",None),
6:("Ask ChatGPT to create the Claude prompt","ChatGPT reply containing the Claude master prompt","Prompt text;copy icon","Shows where the Claude build brief comes from.","11-chatgpt-claude-prompt.png"),
7:("Open the Claude workspace","claude.ai → new conversation","Message box;attachment control","Shows the starting point in Claude.","03-claude-workspace.png"),
8:("Upload files to Claude","Claude message box with files attached","CV;project documentation","Claude needs evidence before building.",None),
9:("Prepare the Claude conversation","Claude conversation with files uploaded, before sending","Uploaded file names","Confirms the files are there before the prompt.",None),
10:("Paste the master prompt into Claude","Claude message box with the master prompt","Pasted prompt;Send","Shows the build instruction being sent.","04-claude-prompt.png"),
11:("Claude generating the website","Claude mid-response while building files","Progress / file creation","Sets the expectation that building takes a moment.",None),
12:("Review Claude's generated files","Claude output with files or preview","File list;preview area","Shows what to inspect first.",None),
13:("Ask Claude to perform QA","Claude message box with the Step 7 prompt","Pasted QA prompt","Shows the switch from creator to critic.",None),
14:("Ask Claude for a targeted change","Claude message box with a narrow change request","Scope limits in the prompt","Shows a safe, narrow request.",None),
15:("Open GitHub","github.com signed in","Home page;profile menu","Shows the starting point on GitHub.",None),
16:("Open the “+” menu","GitHub top-right + menu","+ icon","Shows where repository creation starts.",None),
17:("Select New repository","GitHub + menu → New repository","New repository item","Shows the exact menu choice.",None),
18:("Name the repository","New repository form","Repository name;Visibility;Add README","Naming decides the site URL.","05-github-new-repository.png"),
19:("Create the repository","New repository form, bottom","Create repository button","Final click of repository creation.",None),
20:("Repository file structure","Repository Code tab after upload","index.html;assets;README.md","Shows the files in the right place.","06-github-repository.png"),
21:("Upload files","Repository → Add file → Upload files, or the “uploading an existing file” link","Upload entry point","Shows how to start the upload.","12-github-quick-setup.png"),
22:("Commit changes","Upload page bottom","Commit changes button","Saves the upload.",None),
23:("Open repository Settings","Repository tab bar","Settings tab","Shows where Pages is reached.",None),
24:("Open Pages","Settings left sidebar","Pages","Shows where to find Pages.","07-github-pages.png"),
25:("Select Deploy from a branch","Settings → Pages → Build and deployment","Source dropdown;Deploy from a branch","Selects the branch-based flow.",None),
26:("Select main","Pages → Branch dropdown","main","Chooses which branch is published.",None),
27:("Select /(root)","Pages → folder dropdown","/(root)","Chooses the publishing folder.","08-github-pages-source.png"),
28:("Save the Pages configuration","Pages settings","Save button","Applies the configuration.",None),
29:("View deployment status","Repository → Actions or Pages banner","Deployment status","Shows the build finished.",None),
30:("Open the live website","Browser at the published URL","Address bar;homepage","Proof the site is live.","09-live-site.png"),
31:("Desktop website test","Browser at desktop width","Hero;navigation","Shows the desktop result.",None),
32:("Mobile responsive test","Phone or phone-sized viewport","Hero;menu button","Shows the mobile layout.","10-mobile-test.png"),
33:("CV download test","Click Download CV","CV opening","Confirms the CV path works.",None),
34:("External link test","Click LinkedIn / GitHub links","Destination page","Confirms links go to the right place.",None),
35:("Broken image test","Scroll the whole site","Images loading","Confirms no broken images.",None),
36:("Final recruiter test","Private window, whole site","First screen","Final check as a stranger would see it.",None),
}
def slug(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
def fname(n):
    return SS[n][4] or f"extra-{n:02d}-{slug(SS[n][0])}.png"
import os
BASE=os.path.dirname(os.path.abspath(__file__))
AD=BASE+'/assets/screenshots/'
USED=[]
CAP={2:("ChatGPT conversation with project files attached","Project files attached in a ChatGPT conversation"),
4:("Portfolio information organized in ChatGPT","ChatGPT showing portfolio information organized into labelled categories"),
6:("A Claude build prompt created in ChatGPT","ChatGPT writing a prompt to give to Claude"),
7:("Claude’s new-conversation screen","Claude’s start screen with the message box"),
10:("A prompt pasted into Claude","Claude with the master prompt pasted into the message box"),
18:("GitHub’s New repository form","GitHub’s New repository form with owner, name and visibility settings"),
20:("The repository file list","Repository Code tab showing index.html, assets and README.md"),
21:("GitHub’s quick-setup page","GitHub quick-setup page with the link for uploading an existing file"),
30:("The live portfolio","The published portfolio site open in a browser"),
32:("The portfolio on a phone","The portfolio site displayed on a phone")}
def shot(n):
    f=SS[n][4]
    if not f or not os.path.exists(AD+f) or n not in CAP: return ''
    k=len(USED)+1; cap,alt=CAP[n]; USED.append((k,cap,f,n))
    return f'<figure class="guide-screenshot" id="shot-{k:02d}"><img src="assets/screenshots/{f}" alt="{E(alt)}" loading="lazy"><figcaption><span class="badge">REAL SCREENSHOT</span> {k:02d} · {E(cap)}.</figcaption></figure>'
def shots(*ns):
    h=''.join(shot(n) for n in ns)
    return f'<div class="shots">{h}</div>' if h else ''
def call(kind,label,title,body): return f'<aside class="callout callout-{kind}"><strong>{label}</strong><h3>{E(title)}</h3><p>{body}</p></aside>'
def code(label,text,meta=''):
    return f'<div class="code-block"><div class="code-head"><span class="prompt-label">{label}</span><button class="copy-code" type="button">Copy</button></div>{('<p class="prompt-meta">'+meta+'</p>') if meta else ''}<pre><code>{E(text.strip())}</code></pre></div>'
def table(head,rows,cls=''):
    h=''.join(f'<th scope="col">{E(x)}</th>' for x in head)
    r=''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)
    return f'<div class="table-wrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
def ul(items): return '<ul>'+''.join(f'<li>{i}</li>' for i in items)+'</ul>'
def tree(t): return f'<pre class="tree"><code>{E(t.strip())}</code></pre>'
def checks(group,items):
    return '<ul class="checklist">'+''.join(f'<li><label><input type="checkbox" data-check="{group}-{i}"> <span>{E(x)}</span></label></li>' for i,x in enumerate(items))+'</ul>'
RESET='<button class="btn reset-checklist" type="button">Reset checklist</button>'

P1='''I am building a professional personal portfolio website.
I have uploaded my current CV. Treat it as a source of truth.
Extract and organize the information into:
1. Name and professional title
2. Professional summary
3. Education
4. Work experience
5. Internships
6. Technical skills
7. Programming languages
8. Tools and platforms
9. Projects
10. Certifications
11. Contact information
12. Portfolio-relevant achievements
13. Missing information that I should provide
Do not invent facts. If something is not in the CV, label it as "Not provided."
Keep the wording concise and suitable for a Data Scientist / Machine Learning Engineer portfolio.'''
P2='''Using the CV information above, create a "Portfolio Information Checklist".
Separate the checklist into:
A. Already known
B. Missing but necessary
C. Optional
D. Information I should NOT invent
For every missing item, explain why it matters to a recruiter.
Pay special attention to:
- project links
- GitHub repositories
- certification verification links
- project outcomes
- tools actually used
- employment dates
- contact links
- CV download file
- professional title
- short hero tagline
Do not fill the missing fields with guesses.'''
P3='''Create a master prompt for Claude to build my portfolio website.
The prompt must include:
- professional identity
- target roles
- visual direction
- technical constraints
- required sections
- exact verified contact links
- CV download requirements
- project presentation requirements
- certification requirements
- responsive/mobile requirements
- accessibility requirements
- performance requirements
- SEO requirements
- file/folder structure
- rules against invented information
- a final QA checklist
Write the prompt so Claude can execute it as a senior front-end developer,
UI/UX designer and technical recruiter.
Do not invent any personal information.'''
P5='''Before changing any existing file:
1. Inspect the current structure.
2. Preserve useful content.
3. Do not remove sections unless they are explicitly approved.
4. Do not invent facts.
5. Do not replace real links with placeholders.
6. After editing, check every internal and external link.
7. Return a concise change summary.'''
P7='''Perform a final QA review of this portfolio.
Act simultaneously as:
1. a technical recruiter
2. a senior machine learning engineer
3. a front-end engineer
4. a UX reviewer
Check:
- first impression
- professional branding
- clarity of target role
- project credibility
- technical terminology
- broken or placeholder links
- CV download
- certification verification
- mobile responsiveness
- accessibility
- SEO basics
- performance risks
- console errors
- missing alt text
- navigation
- spelling and grammar
- inconsistent dates
- invented or unsupported claims
Do not rewrite everything automatically.
First produce:
A. Critical issues
B. Important improvements
C. Optional polish
Then fix only A and B unless I explicitly approve C.'''
P18='''Only update the Certifications section.
Add this new certification using the information in the uploaded certificate.
Do not redesign the site.
Do not change the hero.
Do not change navigation.
Do not rewrite my existing experience.
Do not invent a date or credential number.
After editing, verify that:
1. the certification card is responsive
2. the credential link works
3. the existing design remains unchanged'''
P20='''Improve only the Projects section.
Goals:
- make project cards easier to scan
- keep the current color palette
- keep the current typography
- preserve all existing project information
- do not change the hero or navigation
- do not invent metrics
- keep all existing project links
Before editing, inspect the current HTML and CSS.
After editing, list exactly which files changed and what changed.'''
CVT='''assets/
└── cv/
    └── Abdulazeem_Ayomide_Data_Scientist_CV.pdf'''
T9='''portfolio/
├── index.html
├── css/
│   ├── style.css
│   ├── animations.css
│   └── responsive.css
├── js/
│   ├── app.js
│   └── particles.js
├── assets/
│   ├── images/
│   ├── icons/
│   ├── svg/
│   ├── cv/
│   └── certifications/
└── README.md'''
T15='''yourusername.github.io/
├── index.html
├── css/
├── js/
├── assets/
└── README.md'''
T15b='''yourusername.github.io/
└── portfolio/
    └── index.html'''


def cdc(c,d,k):
    return '<div class="cdc">'+''.join(f'<div><b>{t}</b><p>{x}</p></div>' for t,x in (('COPY',c),('DO',d),('CHECK',k)))+'</div>'
def dd(do,dont):
    return f'<div class="dd"><aside class="do"><b>🟢 DO THIS</b><p>{do}</p></aside><aside class="dont"><b>🔴 DON’T DO THIS</b><p>{dont}</p></aside></div>'
PAGES_ILL='<figure class="illustration"><figcaption><span class="badge ill">ILLUSTRATION</span> The path to a live site (a concept diagram, not a screenshot).</figcaption><ol class="path"><li>Repository</li><li>Settings</li><li>Pages</li><li>Build and deployment</li><li>Deploy from a branch</li><li><code>main</code></li><li><code>/(root)</code></li><li>Save</li><li>Wait for deployment</li><li>Open the generated URL</li></ol></figure>'
CDC={5:cdc('The Step 1 prompt below.','Upload your CV in a new ChatGPT conversation, then paste and send the prompt.','Anything missing from the CV is labelled “Not provided” — nothing is invented.'),
6:cdc('The Step 2 prompt below.','Send it in the same conversation.','You have a checklist split into A–D, with a reason for each missing item.'),
7:cdc('The Step 3 prompt below.','Send it to ChatGPT, then copy the Claude master prompt it writes.','The master prompt includes rules against invented information and a final QA checklist.'),
9:cdc('Your master prompt, plus the instruction block below.','Send it in the Claude conversation where your files are already uploaded.','Claude returns a concise change summary.'),
11:cdc('The QA prompt below.','Send it as a separate message after the first build.','You received A (critical), B (important) and C (optional) lists; only A and B get fixed unless you approve C.'),
14:cdc('Your repository name, for example <code>yourusername.github.io</code>.','Use + → New repository → Create repository.','Visibility is Public if your plan requires it.'),
15:cdc('Your website files.','Upload them to the repository.','<code>index.html</code> is at the top level, not inside another folder.'),
16:cdc('Branch <code>main</code> and folder <code>/(root)</code>.','Settings → Pages → Deploy from a branch → Save.','Source, branch and folder show what you selected.'),
17:cdc('Your published URL.','Open it, refresh, then try a private window and your phone.','Navigation, CV, links, images and CSS all work.'),
18:cdc('The update prompt below.','Send it to Claude with the new source material.','The card is responsive, the link works, and the rest of the design is unchanged.')}
DD={1:dd('Use your real CV, projects, certifications and contact information.','Ask AI to invent qualifications, projects or work experience.'),
4:dd('Remove passwords, API keys and other secrets before uploading.','Upload files containing private keys or bank information.'),
9:dd('Give Claude the files first, then the prompt.','Let Claude replace real links with placeholders.'),
15:dd('Upload the files so <code>index.html</code> is at the top level.','Upload a folder that contains your website folder.'),
16:dd('Select Deploy from a branch, <code>main</code> and <code>/(root)</code>.','Publish secrets — Pages sites are public.'),
17:dd('Allow a few minutes for deployment.','Assume the deployment failed straight away.'),
20:dd('Name the section and list what must not change.','Ask “Make the website better.”')}
CATS=['PREPARE']*4+['BUILD']*5+['TEST']*3+['DEPLOY']*4+['LAUNCH']*2+['REFERENCE']*3+['REFERENCE','LAUNCH','REFERENCE','LAUNCH']
LAUNCH='<div class="launch"><h3>🚀 Ready to Launch?</h3><p>Work through this last check before you send your link to anyone.</p>'+checks('launch',['Portfolio opens correctly','Resume downloads','GitHub works','LinkedIn works','Projects are accurate','Contact information is correct','Mobile layout works','No placeholder content remains','GitHub Pages is live'])+RESET+'<p><a class="btn primary cta" href="https://gleeboi.github.io" target="_blank" rel="noopener">OPEN MY LIVE PORTFOLIO →</a></p><p class="small">This button opens the GLEEBOI worked-example portfolio. Your own portfolio will have its own URL.</p><p>You gave ChatGPT the truth, gave Claude the plan, gave GitHub the files, and kept the final approval. When something changes, use the small-change workflow in Step 14 instead of starting again.</p></div>'
B={}
B[1]=('<p>This is not a guide that assumes you already know HTML, CSS, JavaScript, Git or GitHub. It treats the website as a small project and explains the handoff between AI tools and the human.</p><p>The basic idea is simple:</p>'
+ul(['<strong>You</strong> provide the truth: your CV, projects, certifications, links, experience and preferences.','<strong>ChatGPT</strong> helps organize your information, identify gaps, prepare instructions and review the finished portfolio.','<strong>Claude</strong> acts as the website-building partner. It can generate and edit the HTML/CSS/JavaScript files from your instructions.','<strong>GitHub</strong> stores the website files and can publish them through GitHub Pages.','You perform the final human check before sending the link to recruiters.'])
+'<h3>The overall journey</h3><div class="flow"><span>CV + project files</span><span>ChatGPT organizes the information</span><span>Claude builds the website</span><span>GitHub stores the files</span><span>GitHub Pages publishes</span><span>Live portfolio</span></div>'
+call('good','GOOD','What this guide is designed to do','Take someone from “I have a CV but I do not know how to build a portfolio” to a live GitHub Pages website.')
+call('tip','TIP','How to use the guide','Read it once from beginning to end if this is your first portfolio. After that, use the troubleshooting and update sections as a reference.')
+call('warning','WARNING','Golden rule','AI can write the website, but it should never invent your education, employment, certification dates, project results, links or years of experience.')
+call('tip','NOTE','Version note','GitHub Pages instructions were checked against current GitHub documentation while the PDF was prepared. GitHub’s interface can change, so labels may occasionally move while the underlying workflow remains similar.'))
B[2]=('<p>The finished result is a professional static portfolio website. A static site is a collection of files that the browser can load directly. For this workflow, you do not need a backend server.</p><p>The GLEEBOI example uses a futuristic, restrained data/AI aesthetic rather than a generic template. The original design brief specifies HTML5, CSS3 and vanilla JavaScript, with no Bootstrap, Tailwind or React, and emphasizes a premium visual language inspired by products such as OpenAI, Vercel, Linear, Anthropic, GitHub, Framer and Stripe without copying them.</p><h3>Recommended portfolio sections</h3>'
+table(['Section','Purpose'],[['Hero','Immediately tells a recruiter who you are and what you do.'],['About','Provides professional context without turning into a long biography.'],['Quick Facts','Gives a fast snapshot of education, location, focus, tools and interests.'],['Skills','Shows relevant technical capabilities.'],['Experience','Shows professional or internship evidence.'],['Projects','Provides proof that you can apply your skills.'],['Certifications','Provides verifiable learning evidence.'],['CV / Resume','Lets recruiters download your current CV.'],['Contact','Makes it easy to email, view LinkedIn or visit GitHub.']])
+'<p>A strong portfolio is not simply a pretty homepage. Its job is to reduce recruiter uncertainty: Who are you? What can you do? Have you built anything? Can I verify it? How do I contact you?</p>')
B[3]=('<p>Think of the process as a small team where each member has a different responsibility.</p>'
+table(['Role','Main job','Do not delegate blindly'],[['You','Provide accurate information, make decisions, approve final content.','Your identity, truth, final approval.'],['ChatGPT','Organize information, identify missing details, draft instructions, review.','Do not assume unknown facts.'],['Claude','Generate and edit the website files, implement design and functionality.','Do not allow invented facts or destructive rewrites without checking.']])
+call('tip','TIP','A useful mental model','ChatGPT is the planner/editor. Claude is the builder. GitHub is the storage + publishing layer. You are the product owner.')
+'<p>This separation makes the workflow easier to debug. If the website looks wrong, ask Claude to fix the implementation. If the information is wrong, return to ChatGPT and your source documents.</p>')
B[4]=('<p>Create one folder on your computer called something like <strong>Portfolio Materials</strong>. Put copies of your source files there.</p><h3>Recommended materials</h3>'
+ul(['Your latest CV in PDF format.','Project reports, slide decks, notebooks or documentation you want represented.','Certificates and credential links.','Your GitHub profile URL.','Your LinkedIn URL.','A professional email address.','A professional photograph only if you genuinely want one on the site.','Any existing portfolio files if you are updating an old website rather than starting from zero.'])
+'<p>For the GLEEBOI example, the portfolio work referenced a CV, Python certificates, a hospitality capstone slide deck and capstone documentation. The original prompt explicitly instructed Claude to analyze uploaded files rather than invent project details.</p>'
+call('warning','WARNING','Privacy check','Remove passwords, private API keys, personal identification numbers, bank information and other secrets before uploading files to any AI tool.'))
B[5]=('<p>Start with your CV because it is the most compact source of your professional identity.</p><p>In ChatGPT:</p>'
+ul(['Start a new conversation for the portfolio project.','Upload your CV using the attachment button.','Tell ChatGPT that the CV is the source of truth for your professional history.','Ask it to extract your information into clear categories.'])
+shots(1,2)+'<h3>Copy-ready prompt</h3>'+code('CHATGPT PROMPT · COPY-READY',P1,'<strong>Purpose:</strong> organize your CV into clear categories. <strong>Use when:</strong> right after uploading your CV in a new ChatGPT conversation.')+shots(3,4)
+call('good','GOOD','Why this step matters','You are creating a clean information layer before asking Claude to design anything. This reduces contradictions and prevents the website prompt from becoming a pile of guesses.'))
B[6]=('<p>A portfolio needs more than a CV. Ask ChatGPT to identify the missing pieces before you build.</p>'+code('CHATGPT PROMPT · COPY-READY',P2,'<strong>Purpose:</strong> find what is missing before you build. <strong>Use when:</strong> after ChatGPT has organized your CV information.')
+'<h3>Example of a good result</h3>'+table(['Field','Status','Action'],[['GitHub','Known','Use the exact URL.'],['LinkedIn','Known','Use the exact URL.'],['Project result','Missing','Ask the user or inspect project documentation.'],['Certification date','Missing','Use credential evidence if available.'],['Years of experience','Unknown','Do not invent.']])+shots(5))
B[7]=('<p>Now ask ChatGPT to convert the organized information into a detailed build brief for Claude.</p>'+code('CHATGPT PROMPT · COPY-READY',P3,'<strong>Purpose:</strong> turn your organized information into a build brief for Claude. <strong>Use when:</strong> once the missing information is sorted out.')
+'<p>For GLEEBOI, the source brief establishes the identity as Data Scientist | Machine Learning Engineer, the tagline <em>Building intelligent solutions through data, machine learning, and artificial intelligence.</em>, and the futuristic but restrained visual direction.</p>'+shots(6))
B[8]=('<p>Open Claude and create a conversation dedicated to the portfolio. The exact interface may change, but the important concept is that Claude needs access to the source files and a clear build instruction.</p><p>Before sending the master prompt:</p>'
+ul(['Upload the CV.','Upload relevant project documentation.','Upload certificates if you want Claude to inspect them.','Upload existing website files if you are updating an existing site.','Tell Claude what is authoritative and what is only inspiration.'])
+shots(7,8,9)+call('warning','WARNING','Do not rush the prompt','If Claude does not have the files it needs, the model may produce a visually impressive site with incomplete or invented content. Give it the evidence first.'))
B[9]=('<p>The master prompt should tell Claude what to build, what not to change, what files to create, and how to verify the result.</p><h3>A strong prompt has six layers</h3>'
+ul(['<strong>Identity:</strong> who the website represents.','<strong>Design:</strong> visual system, typography, spacing, motion and responsive behavior.','<strong>Content:</strong> sections and exact information.','<strong>Engineering:</strong> HTML/CSS/JavaScript structure, accessibility and performance.','<strong>Evidence:</strong> CV, projects and credentials.','<strong>QA:</strong> a final verification pass before declaring the work finished.'])
+'<p>The GLEEBOI prompt specifically requests HTML5, CSS3 and vanilla JavaScript, with no Bootstrap, Tailwind or React, and a clean production-ready structure.</p><h3>Important instruction to include</h3>'+code('CLAUDE PROMPT · COPY-READY',P5,'<strong>Purpose:</strong> stop Claude from inventing facts or damaging existing files. <strong>Use when:</strong> include it in the master prompt, especially when editing existing files.')+shots(10,11))
B[10]=('<p>Do not immediately publish the first version. First inspect it like a recruiter and then like a developer.</p><h3>Recruiter review</h3>'
+ul(["Can I understand the person's role within five seconds?",'Is the professional title clear?','Is the strongest project visible without hunting?','Can I find the CV quickly?','Can I contact the person quickly?','Does the site look intentional rather than like a template?'])
+'<h3>Technical review</h3>'+ul(['Do all navigation links work?','Do project buttons go to the correct destinations?','Does the CV open?','Do images load?','Does the site work on a phone?','Are there console errors?','Are files referenced with correct relative paths?'])
+shots(12)+call('tip','TIP','The five-second test','Open the homepage and look at it for only five seconds. Then close it. If you cannot explain who the person is, what they do and where to find their proof, the first screen needs work.'))
B[11]=('<p>Use a separate QA instruction after the first build. This turns the model from creator into critic.</p>'+code('CLAUDE PROMPT · COPY-READY',P7,'<strong>Purpose:</strong> turn Claude from creator into critic. <strong>Use when:</strong> after the first build, as a separate message.')
+'<p>The original GLEEBOI brief similarly asks for a final review from the perspective of a Google AI recruiter, senior ML engineer and technical hiring manager, including first impression, technical credibility, project quality, ATS keywords, missing sections, wording and design.</p>'+shots(13))
B[12]=('<p>Before GitHub, test the site locally or inside the preview environment available to you.</p><h3>Test every clickable item</h3>'
+ul(['Logo / home link','Navigation links','View Projects','Download CV','Email','LinkedIn','GitHub','Project repository links','Credential verification links'])
+'<h3>Test the CV path</h3>'+tree(CVT)+'<p>If the HTML contains:</p>'+code('HTML',"href=\"assets/cv/Abdulazeem_Ayomide_Data_Scientist_CV.pdf\"")
+'<p>then that exact folder and filename must exist relative to the HTML page. Capitalization and spelling matter on many hosting environments.</p><h3>Pre-publish test checklist</h3>'
+checks('prepublish',['Navigation works','CV opens','External links work'])+shots(31,32,33,34,35))
B[13]=('<p>You do not need to become a professional front-end developer to understand the basic structure.</p>'+tree(T9)
+table(['File / folder','What it does'],[['<code>index.html</code>','The main page structure and content.'],['<code>style.css</code>','Main visual styling.'],['<code>animations.css</code>','Motion and transition rules, if separated.'],['<code>responsive.css</code>','Phone/tablet layout rules, if separated.'],['<code>app.js</code>','Interactive behavior.'],['<code>particles.js</code>','Background particle/neural effect, if used.'],['<code>assets/</code>','Images, icons, CVs, certificates and other files.'],['<code>README.md</code>','Human-readable project documentation.']]))
B[14]=('<p>GitHub Pages can publish a repository as a website. For a personal user site, GitHub’s quickstart uses the repository name <code>username.github.io</code>.</p><h3>Click-by-click</h3>'
+'<ol><li>Open GitHub in your browser and sign in.</li><li>Click the <strong>+</strong> menu in the upper-right corner.</li><li>Choose <strong>New repository</strong>.</li><li>If you are creating a personal user site, enter your GitHub username followed by <code>.github.io</code>.</li><li>Choose the appropriate visibility. For GitHub Free user sites, GitHub’s documentation states that the repository must be public.</li><li>Optionally add a README.</li><li>Click <strong>Create repository</strong>.</li></ol>'
+table(['Setting','Value'],[['Owner','Your GitHub account'],['Repository name','<code>yourusername.github.io</code>'],['Description','Professional portfolio website'],['Visibility','Public, when required by your plan']])
+shots(15,16,17,18,19)+call('tip','TIP','Do not confuse the repository with the website','The repository is where your files live. GitHub Pages is the publishing service that turns those files into the live website.'))
B[15]=('<p>Once the repository exists, upload the actual website files. The most important file is normally <code>index.html</code>. GitHub Pages looks for an entry file such as <code>index.html</code> at the top level of the publishing source.</p><h3>Recommended upload structure</h3>'+tree(T15)
+'<p>If you upload a folder containing another folder, check that you did not accidentally create this:</p>'+tree(T15b)+'<p>That can cause a deployment to publish the wrong location depending on the selected source.</p>'+shots(20,21,22))
B[16]=('<p>GitHub’s current documentation describes the branch-based flow as: repository → Settings → Pages → Build and deployment → Source → Deploy from a branch → choose branch and folder → Save.</p><h3>Click-by-click</h3>'
+'<ol><li>Open your website repository.</li><li>Click <strong>Settings</strong>.</li><li>In the left sidebar, find the <strong>Pages</strong> area under the repository settings.</li><li>Under <strong>Build and deployment</strong>, find <strong>Source</strong>.</li><li>Select <strong>Deploy from a branch</strong>.</li><li>Select the branch containing your website, commonly <code>main</code>.</li><li>Select the publishing folder. For files stored at the repository root, select <code>/(root)</code>.</li><li>Click <strong>Save</strong>.</li></ol>'
+PAGES_ILL+call('warning','WARNING','Important','GitHub Pages sites are public on the internet. Do not publish secrets or sensitive information in your repository.'))
B[17]=('<p>After saving the Pages configuration, GitHub builds and deploys the site. GitHub notes that publishing can take a few minutes and that changes can take up to about ten minutes to appear.</p><p>When the site is live:</p>'
+ul(['Open the published URL.','Refresh the page.','Open the site in an incognito/private window.','Test on your phone.','Test the CV download.','Test LinkedIn and GitHub links.','Click every navigation item.','Look for broken images.','Look for missing CSS.','If something changed recently, allow a few minutes for deployment before assuming the deployment failed.'])
+'<h3>Live site verification</h3>'+checks('live',['Site loads over the published URL','Desktop layout works','Mobile layout works'])+shots(29,30))
B[18]=('<p>You do not need to rebuild the portfolio every time you earn a certificate or finish a project.</p><h3>Use a small-change workflow</h3>'
+'<ol><li>Add the new source material.</li><li>Ask ChatGPT to extract the new information and identify where it belongs.</li><li>Ask Claude to modify only the relevant section.</li><li>Tell Claude not to alter unrelated sections.</li><li>Review the changed files.</li><li>Test locally/preview.</li><li>Commit the change to GitHub.</li><li>Check the live site.</li></ol>'+code('CLAUDE PROMPT · COPY-READY',P18,'<strong>Purpose:</strong> add one new certificate without touching anything else. <strong>Use when:</strong> when you earn a new certificate.'))
B[19]=(table(['Problem','Likely cause','First action'],[['Site is blank','index.html missing, wrong source folder, or HTML error.','Confirm index.html is at the top of the publishing source.'],['CSS is not loading','Wrong relative path.','Check href paths and capitalization.'],['Images are broken','Wrong image path or filename.','Check exact asset path and filename.'],['CV does not open','Wrong path or file not uploaded.','Compare the href with the actual repository path.'],['Old version appears','Deployment still processing or browser cache.','Wait a few minutes, then hard refresh/private window.'],['Claude removed something','Prompt allowed broad rewriting.','Restore from the previous version and use a targeted change prompt.'],['Claude invented details','Source material was incomplete or prompt was vague.','Remove the claim and instruct Claude to use only evidence.'],['Mobile layout is broken','Responsive CSS is incomplete.','Ask Claude to audit at mobile widths and fix only responsive rules.']])
+call('tip','TIP','Debugging order','Check the repository structure first, then the publishing source, then file paths, then the code itself. Do not randomly change five things at once.'))
B[20]=('<p>The quality of the result often depends on how narrowly you define the change.</p><h3>Bad request</h3>'+code('AVOID','Make the website better.')+'<h3>Better request</h3>'+code('CLAUDE PROMPT · COPY-READY',P20,'<strong>Purpose:</strong> an example of a narrowly scoped change request. <strong>Use when:</strong> whenever you want to improve one section.')
+'<p>This is the difference between giving Claude a destination and giving it a runway.</p>'+shots(14)+call('good','GOOD','Version control habit','Before a major change, keep a copy of the working version or use Git commits so you can return to a known-good state.'))
B[21]=('<div class="example-banner">WORKED EXAMPLE · GLEEBOI</div><p><strong>This is what GLEEBOI did. Now replace it with your own information.</strong> The following example shows how the guide translates into a real portfolio brief. <strong>Replace the personal information with your own verified details</strong> — do not copy these values.</p><div class="two-col"><div class="example-data"><h3>Example data</h3><h4>Identity</h4>'
+table(['Field','Worked example'],[['Brand','GLEEBOI'],['Professional title','Data Scientist | Machine Learning Engineer'],['Hero tagline','Building intelligent solutions through data, machine learning, and artificial intelligence.'],['Location','Lagos, Nigeria'],['Education','B.Sc. Plant Science &amp; Biotechnology'],['Languages','Python, SQL, R'],['Focus','Machine Learning, Data Analytics, Statistical Modeling, Artificial Intelligence']])
+'<h4>Contact example</h4>'+table(['Channel','Value'],[['Email','ayomideabdulazeem@gmail.com'],['LinkedIn','linkedin.com/in/abdulazeem-ayomide-28a5b6375'],['GitHub','github.com/gleeboi']])
+'</div><div class="your-data"><h3>Your data</h3><p>Fill these in from your own CV and accounts:</p>'+ul(['Brand / name','Professional title','Hero tagline','Location','Education','Languages and tools','Focus areas','Email, LinkedIn, GitHub'])+'</div></div>'
+'<p>The original brief also specifies tools such as Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Power BI, Git and Jupyter Notebook, plus interests in predictive analytics, AI applications, data-driven solutions and machine learning systems.</p>'
+call('warning','WARNING','Evidence rule','The GLEEBOI brief explicitly says not to invent certification details, CV content, experience or project results. That rule should be copied into any portfolio workflow.'))
CK={'Identity':['Professional title is immediately visible.',"Hero message explains the person's value.",'Name/brand is consistent everywhere.','No exaggerated or unsupported claims.'],
'Projects':['At least one strong project is easy to find.','Each project explains the problem and approach.','Technologies are accurate.','Links work.','Results are supported by source material.'],
'Evidence':['CV download works.','Certifications are verifiable.','GitHub profile is correct.','LinkedIn profile is correct.'],
'Engineering':['No broken navigation.','No broken images.','No missing CSS.','No obvious console errors.','Mobile layout is usable.','Accessibility basics are addressed.'],
'Publishing':['index.html is in the correct publishing source.','GitHub Pages source is configured correctly.','The live URL opens.','The latest changes are visible.']}
B[22]=''.join(f'<h3>{k}</h3>'+checks('final-'+k.lower(),v) for k,v in CK.items())+RESET+shots(36)+call('good','GOOD','Final rule','Do not send the portfolio link to recruiters until you have tested it as if you were a recruiter who has never met you.')
def sec23():
    rows=[]
    for k,cap,f,n in USED:
        sec=[i for i,(sid,t,_,_) in enumerate(SEC,1) if f'id="shot-{k:02d}"' in SECHTML.get(sid,'')]
        rows.append([f'{k:02d}',E(cap),f'<a href="#shot-{k:02d}">Section {sec[0]}</a>' if sec else '',f'<code>{f}</code>'])
    return rows
def sec23_html():
    return ('<p>This guide uses real screenshots from the portfolio-building process where they provide useful visual guidance. When a real interface screenshot is unavailable, the instructions remain fully usable without one.</p>'
    +table(['#','Screenshot','Used in','Filename'],sec23()))
FL=[('1','Collect','CV + projects + certificates + links'),('2','Extract','ChatGPT organizes the facts'),('3','Gap-check','ChatGPT identifies missing information'),('4','Brief','ChatGPT creates the Claude build prompt'),('5','Build','Claude creates/edits the website'),('6','Review','You inspect the first version'),('7','QA','Claude audits recruiter + technical quality'),('8','Test','You verify links, files and mobile'),('9','Publish','GitHub repository + GitHub Pages'),('10','Verify','Open the live site and test again'),('11','Maintain','Make small evidence-based updates')]
B[23]='@@'
B[24]=('<p>This is the entire process compressed into one repeatable sequence.</p>'+table(['#','Stage','What happens'],[list(r) for r in FL])
+call('good','GOOD','The simplest version','If the reader remembers only one thing: give ChatGPT the truth, give Claude the plan, give GitHub the files, and give yourself the final approval.')
+LAUNCH+'<h3>Reference links</h3><ul><li><a href="https://docs.github.com/en/pages/quickstart" rel="noopener">GitHub Pages Quickstart</a></li><li>Publishing source documentation: GitHub Docs: Configuring a publishing source</li></ul><p class="small">Source note: portfolio-specific details in the GLEEBOI example were derived from the supplied portfolio prompt material.</p><p><strong>END OF GUIDE</strong></p>')

N=len(SEC)
out=[]
SECHTML={}
for i,(sid,title,short,step) in enumerate(SEC,1):
    pv=SEC[i-2] if i>1 else None; nx=SEC[i] if i<N else None
    nav='<nav class="pn" aria-label="Section navigation">'+(f'<a class="prev" href="#{pv[0]}">← {E(pv[1])}</a>' if pv else '<span></span>')+(f'<a class="next" href="#{nx[0]}">{E(nx[1])} →</a>' if nx else '<span></span>')+'</nav>'
    body=CDC.get(i,'')+DD.get(i,'')+B[i]
    if i==23: body=sec23_html()
    SECHTML[sid]=body
    out.append(f'<section id="{sid}" class="guide-section" data-title="{E(title)}"><p class="eyebrow">SECTION {i:02d} OF {N}· {CATS[i-1]}{" · "+step.upper() if step else ""}</p><h2>{i}. {E(title)}</h2>{body}{nav}</section>')
toc=''.join(f'<li><a href="#{s[0]}"><span class="n">{i:02d}</span>{E(s[2])}</a></li>' for i,s in enumerate(SEC,1))
page=f'''<!DOCTYPE html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Build &amp; Deploy Your Professional Portfolio Website</title>
<meta name="description" content="A beginner-friendly workflow for going from a CV to a live portfolio website using ChatGPT, Claude, GitHub and GitHub Pages.">
<link rel="stylesheet" href="css/style.css"><link rel="stylesheet" href="css/responsive.css"><link rel="stylesheet" href="css/print.css" media="print">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress-bar" id="progress-bar" role="progressbar" aria-label="Reading progress" aria-valuemin="0" aria-valuemax="100"></div>
<header class="topbar"><button class="btn menu-btn" id="menu-btn" type="button" aria-controls="sidebar" aria-expanded="false">☰ Contents</button><a class="brand" href="#top">Portfolio Guide</a><span class="progress-text" id="progress-text">Reading progress: 0%</span>
<div class="actions"><button class="btn" id="search-btn" type="button" aria-haspopup="dialog">Search</button><a class="btn" href="assets/pdf/GLEEBOI_Portfolio_Build_and_Deploy_Guide.pdf" download>Download PDF</a><button class="btn" id="theme-btn" type="button" aria-label="Toggle theme">Theme</button></div></header>
<div class="overlay" id="overlay" hidden></div>
<div class="layout"><aside class="sidebar" id="sidebar" aria-label="Table of contents"><nav aria-label="Table of contents"><p class="side-title">PORTFOLIO GUIDE</p><ol class="toc">{toc}</ol></nav></aside>
<main id="main"><div id="top" class="hero"><p class="eyebrow">BEGINNER-FRIENDLY GUIDE</p><h1>Build &amp; Deploy Your Professional Portfolio Website</h1><p class="sub">A beginner-friendly workflow using ChatGPT, Claude and GitHub Pages</p>
<ol class="journey" aria-label="Your journey from CV to live portfolio"><li><a href="#what-to-prepare">CV</a></li><li><a href="#step-1-give-chatgpt-your-information">ChatGPT</a></li><li><a href="#step-4-prepare-the-claude-workspace">Claude</a></li><li><a href="#step-6-review-the-website">Website</a></li><li><a href="#step-10-create-the-github-repository">GitHub</a></li><li><a href="#step-12-turn-on-github-pages">GitHub Pages</a></li><li><a href="#step-13-open-and-test-the-live-website">Live Portfolio</a></li></ol>
<p><a class="btn primary" href="#{SEC[0][0]}">Start Reading</a> <a class="btn" href="assets/pdf/GLEEBOI_Portfolio_Build_and_Deploy_Guide.pdf" download>Download PDF Guide</a></p><p class="small">Worked example: GLEEBOI · Data Scientist | Machine Learning Engineer</p></div>
{''.join(out)}</main></div>
<dialog id="search-dialog" aria-label="Search the guide"><form method="dialog"><input id="search-input" type="search" placeholder="Search: GitHub Pages, Claude, CV, mobile…" aria-label="Search"><button class="btn" value="close">Close</button></form><ul id="search-results"></ul></dialog>
<button class="btn to-top" id="to-top" type="button" hidden>↑ Back to top</button>
<script src="js/app.js"></script><script src="js/search.js"></script><script src="js/checklist.js"></script></body></html>'''
open(BASE+'/index.html','w').write(page)
print(len(page))
