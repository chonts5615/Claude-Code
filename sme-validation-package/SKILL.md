---
name: sme-validation-package
description: "Generate a Cargill-branded SME Validation Package for structured 60-minute focus groups that validate technical competencies against job-relevant essential functions. Use this skill whenever the user asks to create an SME package, validation pack, focus group package, review package, competency validation doc, or anything related to preparing materials for SME reviewers. Also triggers on: 'send to reviewers,' 'SME review,' 'prepare for SMEs,' 'build the review package,' 'validation materials,' 'content validity package,' 'reviewer packet,' 'focus group materials,' 'competency review document,' or any request to package technical competencies (with L1-L4 behavioral indicators) for subject matter expert evaluation. This skill is purpose-built for the Cargill Legal & Compliance job family's 13+ specialization variants but generalizes to any Cargill job family running structured SME validation. Even if the user just names a specialization (e.g., 'Employment Law,' 'Trade Compliance,' 'Litigation') in the context of competency validation, use this skill."
---

# SME Validation Package Generator

Generate audit-ready, Cargill-branded Word documents that package technical competencies for structured Subject Matter Expert (SME) focus group validation. Each package presents competencies with behavioral indicators at four proficiency levels (L1-L4), maps them against essential functions for the target bands (typically Manager II and Advisor), and provides structured rating instruments for SMEs to evaluate relevance, clarity, and level differentiation.

## Why This Skill Exists

The Technical Competency Builder (TCB) initiative produces competency content across 15 job families. Before competencies advance from draft to deployment, they require formal content validation by SMEs who perform the work. This validation step is both a psychometric requirement (Lawshe CVR, SIOP Principles content validity standards) and an organizational governance gate. The SME Validation Package is the primary deliverable that enables this gate.

Without this skill, each specialization's package would be built ad hoc, introducing inconsistency in rating scales, instructions, and methodology across the 13+ Legal & Compliance specializations (and eventually all 15 job families). The skill enforces a consistent, branded, psychometrically defensible template while allowing the variable content — competency names, behavioral indicators, essential functions — to swap cleanly per specialization.

## Required Inputs

Before generating a package, collect these from the user. If any are missing, ask for them explicitly.

| Input | Description | Example |
|---|---|---|
| **Specialization Name** | The Legal & Compliance specialization (or other job family specialization) | "Employment Law," "Trade Compliance," "IP & Innovation" |
| **Technical Competency Set** | Competency names with definitions and L1-L4 behavioral indicators | 4-6 competencies, each with 3 indicators per level |
| **Essential Functions** | Band-specific essential functions for the target roles | Manager II and Advisor band EFs from the JD |
| **Job Description Appendix** | The relevant JD sections for SME reference | Full or excerpted JD content |
| **SME Panel Info** (optional) | Names, titles, years of experience for the reviewers | Used for the cover page and sign-in roster |
| **Session Date/Time** (optional) | Scheduled focus group date | Used for cover page and calendar reference |

If the user provides a specialization name alone, prompt for the remaining inputs. If competency content is available in project knowledge or uploaded files, extract it automatically and confirm before proceeding.

## Output Specification

The skill produces two deliverables:

1. **SME Validation Package (.docx)** — The primary document. Cargill-branded, print-ready, structured for a 60-minute focus group session.
2. **SME Feedback Capture Form (.docx)** — Optional companion. A structured rating matrix that SMEs complete during or after the session, designed for quantitative aggregation (Lawshe CVR computation).

### File Naming Convention

```
SME_Validation_Package_{Specialization}_{YYYYMMDD}.docx
SME_Feedback_Form_{Specialization}_{YYYYMMDD}.docx
```

Replace spaces in specialization names with underscores. Example: `SME_Validation_Package_Employment_Law_20260425.docx`

## Document Generation Process

### Step 1: Read Required References

Before generating any document, read these files in order:

1. **Read the cargill-branding skill** at `/mnt/.claude/skills/user/cargill-branding/SKILL.md` and its `references/colors.md` and `references/typography.md` — these govern all visual styling decisions.
2. **Read `references/stable-content.md`** in this skill's directory — contains all boilerplate sections that are identical across specializations.
3. **Read `references/document-structure.md`** in this skill's directory — contains the exact section order, heading hierarchy, and content placement rules.
4. **Read `references/feedback-form-spec.md`** if the user requests the feedback form — contains the rating matrix specification.

### Step 2: Validate Inputs

Before generating, verify:

- Every competency has exactly 4 proficiency levels (L1-L4) with behavioral indicators
- Each level has at least 2-3 indicators (the three-indicator-per-level standard from TCB v4)
- Essential functions are provided for at least two bands (typically Manager II and Advisor)
- Competency count is between 3 and 8 (flag if outside this range — fewer than 3 suggests incomplete extraction; more than 8 suggests the competency set hasn't been pruned)
- All indicators pass the Observable-Measurable-Discriminant (OMD) test: each indicator describes an observable behavior (not a trait), is measurable (could be rated by a trained observer), and discriminates between proficiency levels (L2 indicator is qualitatively different from L1, not just "more")

If validation fails, surface the specific issues to the user and request corrections before proceeding.

### Step 3: Generate the Document

Use the docx skill's creation approach (`npm install -g docx`, then JavaScript generation). Apply Cargill branding per the cargill-branding skill:

- **Fonts**: Big Caslon for Cargill (headings), Helvetica Now for Cargill (body). Fall back to Georgia (headings) and Arial (body) if Cargill fonts are unavailable in the generation environment.
- **Colors**: Cargill Leaf Green (#00843D) for header accents, horizontal rules, and table header rows. White Green (#F5F9ED) for alternating table rows. Neutral palette for body text.
- **Layout**: US Letter, 1-inch margins, generous whitespace reflecting the Cargill brand personality (optimistic, humble, clean).

Execute the generation script at `scripts/build_sme_package.js` if available. Otherwise, generate the docx inline following the document structure specification.

### Step 4: Post-Generation Verification

After generating the document:

1. Validate the .docx file structure
2. Confirm all competencies from the input appear in the document
3. Confirm all essential functions are mapped in the crosswalk table
4. Confirm page count is reasonable (typically 12-25 pages depending on competency count)
5. Confirm Cargill branding elements are present (Leaf Green headers, correct font declarations)

## Stable vs. Variable Content Architecture

Understanding what changes per specialization and what stays constant is critical for consistency across the 13+ Legal & Compliance variants.

### STABLE Content (identical across all specializations)

These sections use the exact text from `references/stable-content.md`:

- Cover page structure and branding elements
- Project overview and purpose statement
- Focus group protocol (60-minute session structure)
- SME instructions and expectations
- Rating scale definitions (5-point relevance, 3-point clarity, 3-point level-differentiation)
- Competency architecture overview (Values & Behaviors → Common → Technical)
- Validation methodology explanation (content validity, Lawshe CVR)
- Band structure reference (JL1-JL4, University Recruiting, Manager II, Advisor)
- Confidentiality and data handling notice
- Project owner contact block
- Appendix: glossary of terms

### VARIABLE Content (swaps per specialization)

These sections are populated from user inputs:

- Specialization name (appears in title, headers, running footer)
- Specialization functional description (1-2 paragraph overview)
- Technical competency presentation (each competency: name, definition, L1-L4 indicators in a structured table)
- Essential functions crosswalk table (competency × essential function mapping)
- Job description appendix (verbatim JD content for SME reference)
- SME panel roster (names, titles, experience — if provided)
- Session logistics (date, time, location/virtual link — if provided)

## Integration with Other Skills

This skill works alongside:

- **cargill-branding**: Governs all visual identity. Read BEFORE generating any output.
- **competency-architecture**: If the user needs to BUILD competencies before validating them, that skill handles the upstream work. This skill picks up where competency-architecture leaves off.
- **docx**: The underlying document generation capability. This skill adds the domain-specific template and content architecture on top of the docx skill's mechanical generation.
- **review-recommend-enhance-like-an-io-psychologist / multi-lens-review**: After validation data is collected, those skills can evaluate the results through the multi-persona lens.

## Specialization Variants (Legal & Compliance)

The following specializations are known to exist within Cargill Legal & Compliance. When a user references any of these, this skill applies:

| Specialization | Typical Competency Count | Notes |
|---|---|---|
| Employment Law | 5-6 | Heavily regulated; labor relations focus |
| Trade Compliance | 5-6 | Export controls, sanctions, customs |
| Regulatory Affairs | 4-5 | Government agency interface |
| Government Relations | 4-5 | Lobbying, policy advocacy |
| Intellectual Property | 5-6 | Patents, trademarks, trade secrets |
| Litigation | 5-6 | Dispute resolution, trial management |
| Corporate Transactions | 4-5 | M&A, joint ventures, corporate governance |
| Ethics & Compliance | 5-6 | Code of conduct, investigations |
| Environmental Law | 4-5 | EPA, state environmental regs |
| Food Safety & Regulatory | 5-6 | FDA, USDA, global food law |
| Data Privacy | 4-5 | GDPR, CCPA, cross-border data |
| Antitrust & Competition | 4-5 | Cartel enforcement, merger review |
| Commercial Contracting | 5-6 | Procurement, supply agreements |

This list is non-exhaustive. If the user names a specialization not listed here, proceed normally — the template accommodates any specialization.

## Edge Cases and Decision Rules

- **University Recruiting band**: If UR-level essential functions are provided, include them in the crosswalk table as a separate band column. UR competencies may have only L1-L2 indicators; this is acceptable.
- **Shared competencies across specializations**: If a competency appears in multiple specializations (e.g., "Legal Research & Analysis"), note it as a shared competency in the document header for that competency. SME feedback on shared competencies propagates per TCB v4 propagation discipline.
- **More than 6 competencies**: Flag this per the six-competency-per-JD maximum from TCB v4. Include all provided competencies but add a reviewer note that the focus group should also assess whether the set should be pruned.
- **Missing L3 or L4 indicators**: If a competency has indicators only at L1-L2 (common for newer or UR-focused competencies), generate the table with empty cells at L3-L4 and add an explicit SME prompt: "Are L3/L4 behaviors relevant for this specialization? If so, what would they look like?"
