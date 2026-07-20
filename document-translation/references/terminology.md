# Terminology and Glossary Management

The glossary is what makes eleven translations behave like one document set. It is built **once per project** (before any translation begins), applied mechanically in Phase 3, and enforced by the Phase 5 consistency scan. When a document family gets retranslated or extended later, the existing glossary is the starting point — consistency with what SMEs and employees have already seen outranks a marginally better new rendering.

## Glossary Structure

One table, maintained as a simple Markdown or Excel artifact delivered alongside the translations so future projects can reuse it:

| Column | Content |
|---|---|
| Term (EN) | The exact English term as it appears in the source |
| Category | `DNT` / `LOCKED` / `PREFERRED` (see below) |
| zh-CN … es-419 | One column per target language: the approved rendering, or `=EN` for keep-in-English |
| Notes | Context restrictions, part-of-speech, first-use gloss text |

**Categories:**

- **DNT (do not translate).** Stays in English in every language, every occurrence. Company and product names (Cargill, named systems/tools), trademarked assessment names (Hogan, KFALP), legal entity names, email addresses, URLs, file paths, acronyms used as codes (L1–L4, R1/R2, EF numbers).
- **LOCKED.** Translated, but only ever as the glossary rendering — no synonyms, no stylistic variation. Everything readers must recognize as *the same thing* across pages and files: competency titles, proficiency level names, rating anchors, section headings that recur across a document set, form field labels, defined terms.
- **PREFERRED.** Default rendering, but the translator may inflect or adapt for grammar (case, number, gender). Most domain vocabulary lands here.

## Decisions to Settle at Intake (once, not per file)

Put each answer in the glossary notes so the decision is auditable:

1. **Competency titles** — three viable policies: (a) translate fully; (b) keep English with translation in parentheses at first use; (c) keep English everywhere. Recommend (a) for employee/candidate-facing material and (b) when the organization runs global calibration sessions in English. Whichever is chosen applies to *every* language.
2. **Rating-scale anchors** ("Below Expectations" … "Exceptional") — translate as a set; the ordinal ordering must be unmistakable in each language; the identical rendering must appear in every file of the set.
3. **Proficiency level labels** (L1–L4 and their names) — level codes are DNT; level names are LOCKED.
4. **English HR loanwords** — each target language has terms its professionals use in English (Dutch "assessment", German "Feedback", Russian "ассессмент"). Decide per term per language, guided by the language profiles; the test is "what would an HR professional in that country write," not "what is the purest native word."
5. **Company voice** — formal vs. informal address per language (profiles give defaults; the user's company culture may override).

## HR/Talent Core Vocabulary — Starting Points

Seed renderings for terms this repository's document families use constantly. These are defensible defaults to *propose*, not to impose — confirm against any existing translated material the organization already uses.

| EN | zh-CN | fr-FR / fr-CA | de-DE | es-ES / es-419 | pt-BR | Notes |
|---|---|---|---|---|---|---|
| competency | 胜任力 | compétence | Kompetenz | competencia | competência | zh: 能力 only in generic ability contexts |
| behavioral indicator | 行为指标 | indicateur comportemental | Verhaltensindikator / Verhaltensanker | indicador conductual (es-419: also "de comportamiento") | indicador comportamental | |
| proficiency level | 熟练程度等级 | niveau de maîtrise | Kompetenzstufe | nivel de dominio | nível de proficiência | |
| interview guide | 面试指南 | guide d'entretien (fr-CA: guide d'entrevue) | Interviewleitfaden | guía de entrevista | roteiro de entrevista | fr-FR "entretien" vs fr-CA "entrevue" |
| rating scale | 评分量表 | échelle d'évaluation | Bewertungsskala | escala de valoración / calificación | escala de avaliação | es-419 prefers "calificación" |
| candidate | 候选人 | candidat(e) | Kandidat:in / Bewerber:in | candidato/a | candidato/a | apply the language's inclusive-form policy |
| essential function | 基本职能 | fonction essentielle | wesentliche Funktion | función esencial | função essencial | |
| stakeholder | 利益相关者 | partie prenante | Stakeholder | parte interesada | parte interessada | de: loanword standard |

(Dutch, Indonesian, Polish, Russian columns follow the same pattern — build them out at project time; the table above illustrates the artifact, it is not exhaustive.)

## Enforcement

- **Phase 3:** the translator applies LOCKED renderings by exact substitution (inflected correctly where grammar demands — Polish/Russian case endings count as the same rendering).
- **Phase 5 consistency scan:** for each LOCKED/DNT term, search every output file for (a) the approved rendering — must appear wherever the English term appeared; (b) known rival renderings — must appear zero times; (c) the raw English term in translated text — must appear only for DNT/`=EN` entries. For inflected languages match on stems, not exact strings.
- **Drift rule:** if mid-project a better rendering is discovered, the glossary is updated **first** and every already-translated file is re-scanned — a rendering change is a project-wide event, never a local fix.
