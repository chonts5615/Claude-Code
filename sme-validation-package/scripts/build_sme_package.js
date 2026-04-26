#!/usr/bin/env node
/**
 * SME Validation Package Generator
 * 
 * Generates a Cargill-branded Word document (.docx) for structured SME focus group
 * validation of technical competencies.
 * 
 * Usage:
 *   node build_sme_package.js --input data.json --output SME_Validation_Package.docx [--feedback]
 * 
 * Input JSON Schema:
 * {
 *   "specialization": "Employment Law",
 *   "sessionDate": "2026-05-15",
 *   "competencies": [
 *     {
 *       "name": "Legal Research & Analysis",
 *       "definition": "The ability to...",
 *       "shared": false,
 *       "indicators": {
 *         "L4": ["indicator 1", "indicator 2", "indicator 3"],
 *         "L3": ["indicator 1", "indicator 2", "indicator 3"],
 *         "L2": ["indicator 1", "indicator 2", "indicator 3"],
 *         "L1": ["indicator 1", "indicator 2", "indicator 3"]
 *       }
 *     }
 *   ],
 *   "essentialFunctions": {
 *     "managerII": ["EF1 text", "EF2 text", ...],
 *     "advisor": ["EF1 text", "EF2 text", ...]
 *   },
 *   "competencyEFMapping": {
 *     "Legal Research & Analysis": [1, 3, 5],
 *     "Regulatory Navigation": [2, 4]
 *   },
 *   "jobDescription": "Full JD text...",
 *   "smePanel": [
 *     { "name": "Jane Doe", "title": "VP Employment Law", "years": 15 }
 *   ]
 * }
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, TabStopType, TabStopPosition
} = require("docx");

// ─── Brand Constants ───────────────────────────────────────────────────────────
const LEAF_GREEN = "00843D";
const WHITE_GREEN = "F5F9ED";
const DARK_GRAY = "333333";
const MED_GRAY = "666666";
const LIGHT_GRAY = "CCCCCC";
const WHITE = "FFFFFF";

// Fonts — fallback to Arial/Georgia if Cargill fonts unavailable
const HEADING_FONT = "Georgia";  // Fallback for Big Caslon for Cargill
const BODY_FONT = "Arial";      // Fallback for Helvetica Now for Cargill

// Page dimensions (DXA: 1440 = 1 inch)
const PAGE_WIDTH = 12240;  // 8.5"
const PAGE_HEIGHT = 15840; // 11"
const MARGIN = 1440;       // 1"
const CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN); // 9360

// ─── Utility Functions ─────────────────────────────────────────────────────────

const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: LIGHT_GRAY };
const borders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorder = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function greenRule() {
  return new Paragraph({
    spacing: { before: 240, after: 240 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LEAF_GREEN, space: 1 } },
    children: []
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 240 },
    children: [new TextRun({ text, font: HEADING_FONT, size: 44, color: LEAF_GREEN, bold: true })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 180 },
    children: [new TextRun({ text, font: BODY_FONT, size: 28, bold: true, color: DARK_GRAY })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text, font: BODY_FONT, size: 24, bold: true, color: DARK_GRAY })]
  });
}

function bodyPara(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({
      text,
      font: BODY_FONT,
      size: 22, // 11pt
      color: DARK_GRAY,
      italics: opts.italic || false,
      bold: opts.bold || false
    })]
  });
}

function bodyParaMultiRun(runs) {
  return new Paragraph({
    spacing: { after: 120 },
    children: runs.map(r => new TextRun({
      text: r.text,
      font: BODY_FONT,
      size: 22,
      color: r.color || DARK_GRAY,
      bold: r.bold || false,
      italics: r.italic || false
    }))
  });
}

function headerCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: LEAF_GREEN, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({ text, font: BODY_FONT, size: 20, bold: true, color: WHITE })]
    })]
  });
}

function bodyCell(text, width, opts = {}) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.shaded ? { fill: WHITE_GREEN, type: ShadingType.CLEAR } : undefined,
    verticalAlign: VerticalAlign.TOP,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({
        text,
        font: BODY_FONT,
        size: 20,
        color: DARK_GRAY,
        bold: opts.bold || false,
        italics: opts.italic || false
      })]
    })]
  });
}

function mergedBodyCell(text, width, rowSpan, opts = {}) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    rowSpan,
    shading: { fill: LEAF_GREEN, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({
        text,
        font: BODY_FONT,
        size: 20,
        color: WHITE,
        bold: true
      })]
    })]
  });
}

// ─── Section Builders ──────────────────────────────────────────────────────────

function buildCoverPage(data) {
  const children = [];
  
  // Leaf Green rule at top
  children.push(greenRule());
  children.push(new Paragraph({ spacing: { before: 720 }, children: [] }));
  
  // Title
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({
      text: "Technical Competency Validation Package",
      font: HEADING_FONT, size: 56, color: LEAF_GREEN, bold: true
    })]
  }));
  
  // Specialization
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({
      text: data.specialization,
      font: BODY_FONT, size: 36, bold: true, color: DARK_GRAY
    })]
  }));
  
  // Function
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 480 },
    children: [new TextRun({
      text: "Cargill Legal & Compliance",
      font: BODY_FONT, size: 28, color: MED_GRAY
    })]
  }));
  
  // Metadata
  const metaLines = [
    "Prepared for: Subject Matter Expert Review Panel",
    "Prepared by: Assessment, Competency & Career Framework Team",
    `Date: ${data.sessionDate || new Date().toISOString().split("T")[0]}`
  ];
  for (const line of metaLines) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [new TextRun({ text: line, font: BODY_FONT, size: 22, color: DARK_GRAY })]
    }));
  }
  
  children.push(new Paragraph({ spacing: { before: 480 }, children: [] }));
  
  // Confidentiality box
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 240, after: 60 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 1, color: LIGHT_GRAY, space: 8 },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: LIGHT_GRAY, space: 8 },
      left: { style: BorderStyle.SINGLE, size: 1, color: LIGHT_GRAY, space: 8 },
      right: { style: BorderStyle.SINGLE, size: 1, color: LIGHT_GRAY, space: 8 }
    },
    children: [new TextRun({
      text: "This document contains proprietary competency architecture materials developed by Cargill's Assessment, Competency & Career Framework team. Distribution is limited to designated Subject Matter Expert reviewers and project stakeholders. Do not forward, copy, or share outside the approved reviewer panel without written authorization from the project owner.",
      font: BODY_FONT, size: 18, italics: true, color: MED_GRAY
    })]
  }));
  
  return children;
}

function buildProjectOverview(data) {
  const spec = data.specialization;
  return [
    heading1("1. Project Overview"),
    bodyPara(`The Technical Competency Builder (TCB) initiative is developing technical competencies across Cargill's 15 job families to support talent decisions spanning selection, development, performance management, and succession planning. These competencies form the third layer of Cargill's three-tier competency architecture:`),
    bodyParaMultiRun([
      { text: "Layer 1 — Values & Behaviors: ", bold: true },
      { text: "Enterprise-wide expectations aligned to Cargill's corporate values and 2030 strategic goals. Apply to all employees." }
    ]),
    bodyParaMultiRun([
      { text: "Layer 2 — Common Competencies: ", bold: true },
      { text: "Cross-functional capabilities expected across multiple job families." }
    ]),
    bodyParaMultiRun([
      { text: "Layer 3 — Technical Competencies: ", bold: true },
      { text: "Specialized knowledge, skills, and behaviors unique to a job family or specialization. This is the layer under review today." }
    ]),
    bodyPara(`Your role as a Subject Matter Expert (SME) is to evaluate whether the draft technical competencies accurately represent the critical knowledge, skills, and behaviors required for effective performance in the ${spec} specialization within Cargill Legal & Compliance.`),
    
    heading2("What We Are Asking You to Do"),
    bodyPara("During this 60-minute structured session, you will:"),
    bodyPara("1. Review each draft technical competency and its behavioral indicators across four proficiency levels (L1 through L4)."),
    bodyPara("2. Rate each competency on three dimensions: Relevance (importance to job performance), Clarity (are indicators unambiguous?), and Level Differentiation (do L1–L4 represent meaningfully different proficiency?)."),
    bodyPara("3. Identify gaps: Are there critical technical capabilities missing from the draft set?"),
    bodyPara(`4. Validate the mapping between competencies and essential job functions for the Manager II and Advisor bands.`),
    bodyPara("Your expert judgment directly shapes the final competency framework. This is not a test — there are no right or wrong answers. We need your candid professional assessment based on your experience performing and supervising this work.")
  ];
}

function buildFocusGroupProtocol() {
  return [
    heading1("2. Focus Group Protocol"),
    heading2("Session Structure"),
    bodyParaMultiRun([{ text: "Minutes 0–5: ", bold: true }, { text: "Welcome, introductions, and overview of session purpose and ground rules." }]),
    bodyParaMultiRun([{ text: "Minutes 5–15: ", bold: true }, { text: "Walkthrough of the competency architecture (three-layer model) and explanation of the rating scales. Questions and clarifications." }]),
    bodyParaMultiRun([{ text: "Minutes 15–50: ", bold: true }, { text: "Competency-by-competency review. For each competency: read the name and definition, allow silent individual review of L1–L4 indicators, facilitate group discussion, capture wording suggestions, and record individual ratings." }]),
    bodyParaMultiRun([{ text: "Minutes 50–55: ", bold: true }, { text: "Gap analysis — open discussion on whether any critical technical capabilities are missing from the draft set." }]),
    bodyParaMultiRun([{ text: "Minutes 55–60: ", bold: true }, { text: "Wrap-up, next steps, and timeline for incorporating feedback." }]),
    
    heading2("Ground Rules"),
    bodyPara("Every perspective is valuable. Disagreement among SMEs is expected and informative."),
    bodyPara("Focus on the work, not the person. We are evaluating whether behaviors are accurately described, not whether individuals possess them."),
    bodyPara("Specificity helps. “This indicator is vague” is less actionable than “This indicator should specify whether we mean internal investigations or regulatory investigations.”"),
    bodyPara("Silence is data. If a competency or indicator generates no discussion, that signals clarity and consensus."),
    bodyPara("We will capture all feedback. If time runs short on a competency, we will collect written feedback via the companion form.")
  ];
}

function buildRatingScaleTable(title, rows) {
  const colWidths = [1200, 2160, 6000];
  const headerRow = new TableRow({
    children: [
      headerCell("Rating", colWidths[0]),
      headerCell("Label", colWidths[1]),
      headerCell("Definition", colWidths[2])
    ]
  });
  const bodyRows = rows.map((r, i) => new TableRow({
    children: [
      bodyCell(r[0], colWidths[0], { shaded: i % 2 === 1 }),
      bodyCell(r[1], colWidths[1], { shaded: i % 2 === 1, bold: true }),
      bodyCell(r[2], colWidths[2], { shaded: i % 2 === 1 })
    ]
  }));
  
  return [
    heading2(title),
    new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: colWidths,
      rows: [headerRow, ...bodyRows]
    })
  ];
}

function buildRatingScales(data) {
  const spec = data.specialization;
  return [
    heading1("3. Rating Scales"),
    ...buildRatingScaleTable(`Relevance: How important is this competency to effective performance in ${spec}?`, [
      ["5", "Essential", "This competency is critical. Deficiency would result in unacceptable job performance."],
      ["4", "Important", "This competency significantly contributes to effective performance. Most incumbents need it."],
      ["3", "Useful", "This competency is helpful but not critical. Some incumbents may perform adequately without strong proficiency."],
      ["2", "Minor", "This competency has limited applicability to this specialization."],
      ["1", "Not Relevant", "This competency does not apply to this specialization."]
    ]),
    new Paragraph({ spacing: { before: 240 }, children: [] }),
    ...buildRatingScaleTable("Clarity: Are the behavioral indicators clearly written?", [
      ["3", "Clear", "The indicators are specific, observable, and would be interpreted consistently by different raters."],
      ["2", "Partially Clear", "The general intent is understandable, but some indicators are vague or could be interpreted differently. Suggest specific rewording."],
      ["1", "Unclear", "The indicators are too abstract, jargon-heavy, or ambiguous to be useful. Significant rewriting needed."]
    ]),
    new Paragraph({ spacing: { before: 240 }, children: [] }),
    ...buildRatingScaleTable("Level Differentiation: Do L1–L4 indicators represent different proficiency levels?", [
      ["3", "Well Differentiated", "Each level describes qualitatively different behavior. A trained observer could reliably distinguish levels."],
      ["2", "Partially Differentiated", "Some levels are distinct, but others overlap or differ only in degree. Suggest where the gaps are."],
      ["1", "Not Differentiated", "The levels read as minor variations of the same behavior. Fundamental restructuring needed."]
    ])
  ];
}

function buildArchitectureReference(data) {
  const levelColWidths = [2000, 7360];
  const levelRows = [
    ["L1 — Foundational", "Applies core technical knowledge under guidance. Handles routine matters within established frameworks. Seeks direction on novel or complex situations."],
    ["L2 — Practitioner", "Independently executes standard technical work. Identifies and resolves moderately complex issues. Begins to advise others. Exercises judgment within established precedent."],
    ["L3 — Advanced Practitioner", "Handles complex, ambiguous, or high-stakes matters with minimal oversight. Shapes technical strategy. Mentors less experienced professionals. Recognized go-to expert."],
    ["L4 — Expert / Thought Leader", "Defines and drives technical strategy across the enterprise. Navigates unprecedented, multi-jurisdictional matters. Shapes organizational capability and external reputation."]
  ];
  
  return [
    heading1("4. Competency Architecture Reference"),
    heading2("Three-Layer Model"),
    bodyPara("Cargill's competency architecture operates on three integrated layers. Layer 1 (Values & Behaviors) is enterprise-wide. Layer 2 (Common Competencies) spans multiple job families. Layer 3 (Technical Competencies) is specialization-specific. Today's review focuses exclusively on Layer 3 content."),
    
    heading2("Proficiency Level Definitions"),
    new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: levelColWidths,
      rows: [
        new TableRow({ children: [headerCell("Level", levelColWidths[0]), headerCell("Description", levelColWidths[1])] }),
        ...levelRows.map((r, i) => new TableRow({
          children: [
            bodyCell(r[0], levelColWidths[0], { bold: true, shaded: i % 2 === 1 }),
            bodyCell(r[1], levelColWidths[1], { shaded: i % 2 === 1 })
          ]
        }))
      ]
    }),
    
    heading2("Band Mapping Reference"),
    bodyPara("The two primary bands under review today are Manager II (JL4 equivalent, expected L3–L4 proficiency) and Advisor (senior individual contributor, expected L3–L4 with deep technical depth). Essential functions for each band are provided in Section 6.")
  ];
}

function buildCompetencyBlock(comp, index, total, data) {
  const children = [];
  const levelWidth = 2160;
  const indicatorWidth = CONTENT_WIDTH - levelWidth;
  
  // Green rule separator
  children.push(greenRule());
  children.push(heading2(`Competency ${index + 1} of ${total}: ${comp.name}`));
  children.push(bodyPara(`Definition: ${comp.definition}`, { italic: true }));
  
  if (comp.shared) {
    children.push(bodyPara("Note: This competency is shared across multiple specializations. Your feedback will be considered alongside input from other specialization SME panels.", { italic: true }));
  }
  
  // Build indicator table — L4 first (descending)
  const levels = ["L4", "L3", "L2", "L1"];
  const levelLabels = {
    "L4": "L4 — Expert / Thought Leader",
    "L3": "L3 — Advanced Practitioner",
    "L2": "L2 — Practitioner",
    "L1": "L1 — Foundational"
  };
  
  const tableRows = [
    new TableRow({
      children: [headerCell("Level", levelWidth), headerCell("Behavioral Indicators", indicatorWidth)]
    })
  ];
  
  for (const level of levels) {
    const indicators = (comp.indicators && comp.indicators[level]) || [];
    if (indicators.length === 0) {
      // Empty level — show placeholder
      tableRows.push(new TableRow({
        children: [
          mergedBodyCell(levelLabels[level], levelWidth, 1),
          bodyCell("[No indicators provided — SMEs: Are behaviors at this level relevant for this specialization?]", indicatorWidth, { italic: true })
        ]
      }));
    } else if (indicators.length === 1) {
      tableRows.push(new TableRow({
        children: [
          mergedBodyCell(levelLabels[level], levelWidth, 1),
          bodyCell(indicators[0], indicatorWidth)
        ]
      }));
    } else {
      // First indicator row with merged level cell
      tableRows.push(new TableRow({
        children: [
          mergedBodyCell(levelLabels[level], levelWidth, indicators.length),
          bodyCell(indicators[0], indicatorWidth)
        ]
      }));
      // Subsequent indicator rows
      for (let j = 1; j < indicators.length; j++) {
        tableRows.push(new TableRow({
          children: [
            bodyCell(indicators[j], indicatorWidth, { shaded: j % 2 === 1 })
          ]
        }));
      }
    }
  }
  
  children.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [levelWidth, indicatorWidth],
    rows: tableRows
  }));
  
  // Rating box
  children.push(new Paragraph({ spacing: { before: 240 }, children: [] }));
  
  const ratingColWidths = [3120, 3120, 3120];
  children.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: ratingColWidths,
    rows: [
      new TableRow({
        children: [
          headerCell("Relevance (1–5)", ratingColWidths[0]),
          headerCell("Clarity (1–3)", ratingColWidths[1]),
          headerCell("Level Differentiation (1–3)", ratingColWidths[2])
        ]
      }),
      new TableRow({
        children: ratingColWidths.map(w => bodyCell("Rating: ___", w))
      })
    ]
  }));
  
  children.push(new Paragraph({ spacing: { before: 120 }, children: [] }));
  children.push(bodyParaMultiRun([
    { text: "Comments: ", bold: true },
    { text: "_______________________________________________________________" }
  ]));
  
  return children;
}

function buildCompetenciesSection(data) {
  const children = [heading1("5. Technical Competencies Under Review")];
  const total = data.competencies.length;
  
  if (total > 6) {
    children.push(bodyPara(`Note: This review includes ${total} competencies, which exceeds the standard six-competency-per-JD maximum. As part of your review, please also consider whether the set should be consolidated or whether any competencies are redundant.`, { italic: true }));
  }
  
  for (let i = 0; i < total; i++) {
    if (i > 0) {
      children.push(new Paragraph({ children: [new PageBreak()] }));
    }
    children.push(...buildCompetencyBlock(data.competencies[i], i, total, data));
  }
  
  return children;
}

function buildEFCrosswalk(data) {
  const children = [heading1("6. Essential Functions Crosswalk")];
  
  // Manager II EFs
  if (data.essentialFunctions && data.essentialFunctions.managerII) {
    children.push(heading2("Manager II Essential Functions"));
    data.essentialFunctions.managerII.forEach((ef, i) => {
      children.push(bodyPara(`${i + 1}. ${ef}`));
    });
  }
  
  // Advisor EFs
  if (data.essentialFunctions && data.essentialFunctions.advisor) {
    children.push(heading2("Advisor Essential Functions"));
    data.essentialFunctions.advisor.forEach((ef, i) => {
      children.push(bodyPara(`${i + 1}. ${ef}`));
    });
  }
  
  // Crosswalk table
  if (data.competencyEFMapping && data.essentialFunctions) {
    children.push(heading2("Competency-to-Essential-Function Mapping"));
    
    const efCount = Math.max(
      (data.essentialFunctions.managerII || []).length,
      (data.essentialFunctions.advisor || []).length
    );
    
    // Calculate column widths
    const compColWidth = 2500;
    const efColWidth = Math.floor((CONTENT_WIDTH - compColWidth) / efCount);
    const colWidths = [compColWidth, ...Array(efCount).fill(efColWidth)];
    
    // Header row
    const headerCells = [headerCell("Competency", compColWidth)];
    for (let i = 0; i < efCount; i++) {
      headerCells.push(headerCell(`EF ${i + 1}`, efColWidth));
    }
    
    const rows = [new TableRow({ children: headerCells })];
    
    // Body rows
    data.competencies.forEach((comp, ci) => {
      const mapping = data.competencyEFMapping[comp.name] || [];
      const cells = [bodyCell(comp.name, compColWidth, { bold: true, shaded: ci % 2 === 1 })];
      for (let i = 0; i < efCount; i++) {
        cells.push(bodyCell(
          mapping.includes(i + 1) ? "X" : "",
          efColWidth,
          { shaded: ci % 2 === 1 }
        ));
      }
      rows.push(new TableRow({ children: cells }));
    });
    
    children.push(new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: colWidths,
      rows
    }));
    
    children.push(new Paragraph({ spacing: { before: 240 }, children: [] }));
    children.push(bodyPara("Review the mapping above. For each competency: Is the mapping accurate? Are there essential functions that should be linked (or unlinked)? Are there essential functions not covered by any competency?", { italic: true }));
  }
  
  return children;
}

function buildMethodologyNote() {
  return [
    heading1("7. Validation Methodology Note"),
    bodyPara("The validation approach used in this project follows established content validity methodology as specified by the Society for Industrial and Organizational Psychology (SIOP) Principles for the Validation and Use of Personnel Selection Procedures and the American Psychological Association (APA) Standards for Educational and Psychological Testing."),
    bodyPara("Content validity evidence is established when qualified Subject Matter Experts confirm that the competency content is representative of the critical requirements of the job. Your individual ratings will be aggregated to compute a Content Validity Ratio (CVR) for each competency, following Lawshe's (1975) methodology. Competencies meeting the CVR threshold for your panel size will be retained; those falling below will be revised or removed."),
    bodyPara("This process ensures that the final competency framework is legally defensible, psychometrically grounded, and practically meaningful for talent decisions.")
  ];
}

function buildConfidentiality(data) {
  return [
    heading1("8. Confidentiality and Data Handling"),
    bodyPara("All materials in this package are Cargill Confidential. Your individual ratings and comments will be aggregated with other SME responses. Individual responses will not be attributed by name in any reporting unless you provide explicit written consent."),
    bodyPara("The aggregated validation data will be used to finalize the technical competency framework, compute content validity statistics for psychometric documentation, inform revisions to behavioral indicators, and support the TCB initiative's audit and governance requirements."),
    bodyPara("Please return all physical copies of this document at the end of the session or destroy them per Cargill's information handling policy.")
  ];
}

function buildContact() {
  return [
    heading1("9. Contact Information"),
    bodyParaMultiRun([{ text: "Project Owner:", bold: true }]),
    bodyPara("Christopher Honts, Ph.D."),
    bodyPara("Manager, Assessment, Competency & Career Framework"),
    bodyPara("Cargill — Human Resources"),
    bodyPara("Wayzata, Minnesota"),
    new Paragraph({ spacing: { before: 120 }, children: [] }),
    bodyPara("For questions about this validation package, the focus group session, or the TCB initiative, please contact the project owner directly.")
  ];
}

function buildJDAppendix(data) {
  if (!data.jobDescription) return [];
  return [
    new Paragraph({ children: [new PageBreak()] }),
    greenRule(),
    heading1(`Appendix A: Job Description — ${data.specialization}`),
    bodyPara(data.jobDescription)
  ];
}

function buildGlossary() {
  const terms = [
    ["Behavioral Indicator", "A specific, observable action or behavior that demonstrates proficiency in a competency at a given level."],
    ["Competency", "A cluster of related knowledge, skills, and behaviors that differentiate levels of job performance."],
    ["Content Validity", "Evidence that a framework adequately represents the critical requirements of the job, as judged by subject matter experts."],
    ["Content Validity Ratio (CVR)", "A statistical index (Lawshe, 1975) quantifying SME agreement that a competency is essential. Ranges from -1 to +1."],
    ["Essential Function", "A fundamental duty or responsibility of a job, as defined in the job description."],
    ["Job Level (JL)", "Cargill's career band designation (JL1 through JL4) reflecting scope, complexity, and organizational impact."],
    ["OMD Criteria", "Observable-Measurable-Discriminant: quality criteria for behavioral indicators."],
    ["Proficiency Level (L1–L4)", "A qualitative tier of capability, from Foundational (L1) to Expert/Thought Leader (L4)."],
    ["SME", "Subject Matter Expert: an individual with deep professional expertise in the specialization under review."],
    ["Technical Competency", "A Layer 3 competency capturing specialized knowledge, skills, and behaviors unique to a specialization."]
  ];
  
  const colWidths = [2800, 6560];
  const rows = [
    new TableRow({ children: [headerCell("Term", colWidths[0]), headerCell("Definition", colWidths[1])] }),
    ...terms.map((t, i) => new TableRow({
      children: [
        bodyCell(t[0], colWidths[0], { bold: true, shaded: i % 2 === 1 }),
        bodyCell(t[1], colWidths[1], { shaded: i % 2 === 1 })
      ]
    }))
  ];
  
  return [
    new Paragraph({ children: [new PageBreak()] }),
    greenRule(),
    heading1("Appendix B: Glossary of Terms"),
    new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: colWidths, rows })
  ];
}

function buildSMERoster(data) {
  if (!data.smePanel || data.smePanel.length === 0) return [];
  
  const colWidths = [2500, 3000, 2000, 1860];
  const rows = [
    new TableRow({
      children: [
        headerCell("Name", colWidths[0]),
        headerCell("Title", colWidths[1]),
        headerCell("Specialization", colWidths[2]),
        headerCell("Years Experience", colWidths[3])
      ]
    }),
    ...data.smePanel.map((sme, i) => new TableRow({
      children: [
        bodyCell(sme.name || "", colWidths[0], { shaded: i % 2 === 1 }),
        bodyCell(sme.title || "", colWidths[1], { shaded: i % 2 === 1 }),
        bodyCell(data.specialization, colWidths[2], { shaded: i % 2 === 1 }),
        bodyCell(String(sme.years || ""), colWidths[3], { shaded: i % 2 === 1 })
      ]
    }))
  ];
  
  return [
    new Paragraph({ children: [new PageBreak()] }),
    greenRule(),
    heading1("Appendix C: SME Panel Roster"),
    new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: colWidths, rows })
  ];
}

// ─── Main Document Assembly ────────────────────────────────────────────────────

async function buildDocument(data) {
  const pageProps = {
    page: {
      size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
      margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
    }
  };
  
  // Cover section (no header/footer)
  const coverSection = {
    properties: { ...pageProps },
    children: buildCoverPage(data)
  };
  
  // Body section (with header/footer)
  const bodyChildren = [
    // TOC
    new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
    new Paragraph({ children: [new PageBreak()] }),
    
    // Sections
    ...buildProjectOverview(data),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildFocusGroupProtocol(),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildRatingScales(data),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildArchitectureReference(data),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildCompetenciesSection(data),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildEFCrosswalk(data),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildMethodologyNote(),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildConfidentiality(data),
    new Paragraph({ children: [new PageBreak()] }),
    ...buildContact(),
    
    // Appendices
    ...buildJDAppendix(data),
    ...buildGlossary(),
    ...buildSMERoster(data)
  ];
  
  const bodySection = {
    properties: {
      ...pageProps,
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [
            new TextRun({ text: `SME Validation Package — ${data.specialization}`, font: BODY_FONT, size: 16, color: MED_GRAY }),
          ],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          children: [
            new TextRun({ text: "Cargill Confidential", font: BODY_FONT, size: 16, color: MED_GRAY }),
            new TextRun({ text: "\tPage " }),
            new TextRun({ children: [PageNumber.CURRENT] }),
          ],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }]
        })]
      })
    },
    children: bodyChildren
  };
  
  const doc = new Document({
    styles: {
      default: { document: { run: { font: BODY_FONT, size: 22 } } },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 44, bold: true, font: HEADING_FONT, color: LEAF_GREEN },
          paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 }
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, font: BODY_FONT, color: DARK_GRAY },
          paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 }
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, font: BODY_FONT, color: DARK_GRAY },
          paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 2 }
        }
      ]
    },
    sections: [coverSection, bodySection]
  });
  
  return doc;
}

// ─── CLI Entry Point ───────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  let inputPath = null;
  let outputPath = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--input" && args[i + 1]) inputPath = args[++i];
    else if (args[i] === "--output" && args[i + 1]) outputPath = args[++i];
  }
  
  if (!inputPath) {
    console.error("Usage: node build_sme_package.js --input data.json --output output.docx");
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  
  if (!outputPath) {
    const safeName = data.specialization.replace(/\s+/g, "_");
    const date = new Date().toISOString().split("T")[0].replace(/-/g, "");
    outputPath = `SME_Validation_Package_${safeName}_${date}.docx`;
  }
  
  console.log(`Generating SME Validation Package for: ${data.specialization}`);
  console.log(`Competencies: ${data.competencies.length}`);
  
  const doc = await buildDocument(data);
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  
  console.log(`Package saved to: ${outputPath}`);
  console.log(`File size: ${(buffer.length / 1024).toFixed(1)} KB`);
}

main().catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});
