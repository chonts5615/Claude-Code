# Step 4: Competency Customization Prompt Template

## User Prompt Format

```
Customize the mapped competencies for this specific role:
- Job Title: [Title from Step 1]
- Job Level: [Level from Step 1]
- Key Tools/Technologies: [From Step 1 requirements]

For each competency:
1. Tailor the definition to the role context (50-150 words)
2. Select 3-7 most relevant behavioral indicators
3. Customize the applied scope with role-specific tools and outputs
```

## GPT Response Template

```yaml
# STEP 4: COMPETENCY CUSTOMIZATION
# ============================================================================

customization_context:
  job_title: "[Title]"
  job_level: "[Level]"
  job_family: "[Family]"
  key_technologies: ["Tech1", "Tech2", "Tech3"]
  domain_context: "[Brief description of work domain]"

customized_competencies:

  # -------------------------------------------------------------------------
  # COMPETENCY 1
  # -------------------------------------------------------------------------
  - competency_id: "CORE_001"
    original_name: "[Name from Model]"
    customized_name: "[Domain: Specific Skill]"

    # Definition Customization
    definition:
      original_text: |
        [Original definition from the Job Family Competency Model]

      customized_text: |
        [50-150 word customized definition that:
        - Is specific to this role's context
        - References tools/technologies from the JD
        - Describes how the competency is applied in this role
        - Uses industry-appropriate language
        - Avoids generic statements

        Example: "The ability to design, develop, and maintain scalable
        software solutions using Python and Java within an agile development
        environment. This includes writing clean, efficient code that follows
        established coding standards, implementing RESTful APIs for system
        integration, and applying object-oriented design principles to create
        maintainable architectures. Practitioners at this level independently
        handle complex technical challenges, optimize application performance,
        and ensure code quality through comprehensive testing and peer reviews."]

      word_count: [N]
      customization_notes: "[What was changed and why]"

    # Why It Matters
    why_it_matters: |
      [2-3 sentences explaining the business impact of this competency
      for this specific role. Connect to organizational outcomes.

      Example: "Strong programming capabilities directly impact product
      delivery timelines and system reliability. Engineers who excel in
      this competency produce fewer defects, enabling faster release
      cycles and reducing maintenance costs by an estimated 30%."]

    # Behavioral Indicators Selection
    behavioral_indicators:
      selection_rationale: |
        [Brief explanation of why these indicators were selected
        from the model's full list]

      selected_indicators:
        - indicator: "[Verb + Object + Context/Standard]"
          level_applicability: ["Mid", "Senior", "Lead"]
          observable_in_role: true
          example_evidence: "[How this would be demonstrated in this role]"

        - indicator: "[Verb + Object + Context/Standard]"
          level_applicability: ["Senior", "Lead", "Principal"]
          observable_in_role: true
          example_evidence: "[Evidence example]"

        - indicator: "[Verb + Object + Context/Standard]"
          level_applicability: ["Entry", "Mid", "Senior"]
          observable_in_role: true
          example_evidence: "[Evidence example]"

        # 3-7 indicators total

      indicator_count: [N]

    # Applied Scope Customization
    applied_scope:
      tools_methods_technologies:
        from_jd: ["Tool1 from JD", "Tool2 from JD"]
        from_model: ["Tool from model that fits context"]
        final_list:
          - "[Tool/Technology 1]"
          - "[Tool/Technology 2]"
          - "[Tool/Technology 3]"

      standards_frameworks:
        - "[Relevant standard for this role/industry]"
        - "[Framework mentioned in JD or implied by context]"

      typical_outputs:
        - "[Deliverable this role produces using this competency]"
        - "[Work product from mapped responsibilities]"
        - "[Artifact that demonstrates competency application]"

    # Proficiency Target
    proficiency_target: "[FOUNDATIONAL | WORKING | ADVANCED | EXPERT]"
    proficiency_rationale: "[Why this level is appropriate for this role]"

    # Responsibility Trace (from Step 3)
    responsibility_trace:
      - responsibility_id: "R1"
        responsibility_summary: "[Brief summary]"
        contribution: "PRIMARY"
        justification: |
          [Explain how this competency enables this specific responsibility
          in the context of this role]

      - responsibility_id: "R3"
        responsibility_summary: "[Brief summary]"
        contribution: "SECONDARY"
        justification: "[Justification]"

  # -------------------------------------------------------------------------
  # COMPETENCY 2
  # -------------------------------------------------------------------------
  - competency_id: "CORE_002"
    original_name: "[Name]"
    customized_name: "[Domain: Specific Skill]"

    definition:
      original_text: "[Original]"
      customized_text: |
        [Customized 50-150 word definition]
      word_count: [N]
      customization_notes: "[Notes]"

    why_it_matters: |
      [Business impact statement]

    behavioral_indicators:
      selection_rationale: "[Rationale]"
      selected_indicators:
        - indicator: "[Indicator 1]"
          level_applicability: ["Levels"]
          observable_in_role: true
          example_evidence: "[Evidence]"
        # Continue...
      indicator_count: [N]

    applied_scope:
      tools_methods_technologies:
        from_jd: ["Tools"]
        from_model: ["Tools"]
        final_list: ["Final tools"]
      standards_frameworks: ["Standards"]
      typical_outputs: ["Outputs"]

    proficiency_target: "[Level]"
    proficiency_rationale: "[Rationale]"

    responsibility_trace:
      - responsibility_id: "R2"
        responsibility_summary: "[Summary]"
        contribution: "[Contribution]"
        justification: "[Justification]"

  # Continue for all competencies...

# Customization Summary
customization_summary:
  total_competencies_customized: [N]
  average_definition_word_count: [N]
  average_indicator_count: [N]

  customization_highlights:
    - "[Key customization decision 1]"
    - "[Key customization decision 2]"

  technologies_incorporated:
    - "[Tech 1]"
    - "[Tech 2]"

  standards_referenced:
    - "[Standard 1]"
    - "[Standard 2]"

# Ready to proceed to Step 5: Quality Validation
```

## Definition Writing Guidelines

### Structure Template
```
[Opening - What the competency is]
The ability to [core action/skill] using [methods/approaches]
within [work context/environment].

[Middle - How it's applied]
This includes [specific activities] and [related tasks],
applying [principles/frameworks] to [achieve outcomes].

[Closing - Level expectations]
Practitioners at this level [level-appropriate expectations]
and [quality/outcome measures].
```

### Quality Checklist
- [ ] 50-150 words (strict requirement)
- [ ] Work-context specific (not generic)
- [ ] Includes relevant tools/technologies
- [ ] Describes observable application
- [ ] Free of undefined jargon
- [ ] Action-oriented language
- [ ] Level-appropriate complexity

### Words to Avoid
| Avoid | Use Instead |
|-------|-------------|
| "Knowledge of..." | "Applies...", "Uses...", "Implements..." |
| "Understanding of..." | "Analyzes...", "Evaluates...", "Demonstrates..." |
| "Familiar with..." | "Works with...", "Utilizes...", "Operates..." |
| "Awareness of..." | "Recognizes...", "Identifies...", "Monitors..." |

## Behavioral Indicator Format

### Pattern: Verb + Object + Context/Standard

| Component | Examples |
|-----------|----------|
| Strong Verbs | Designs, Develops, Implements, Analyzes, Validates, Configures, Optimizes, Integrates, Documents, Reviews |
| Clear Objects | APIs, databases, test cases, architectures, specifications, reports, systems, models |
| Context/Standard | Following [framework], Using [tool], Within [timeframe], Meeting [standard], Achieving [metric] |

### Good Examples
- "Designs RESTful APIs following OpenAPI 3.0 specification"
- "Writes unit tests achieving >80% code coverage"
- "Conducts code reviews using established security checklists"
- "Optimizes database queries to achieve <2 second response times"
- "Documents system architecture using UML diagrams"

### Poor Examples (to avoid)
- "Knows how to write code" (too vague)
- "Good at problem solving" (not observable)
- "Understands database concepts" (not action-oriented)
- "Works well with team" (leadership, not technical)

## Applied Scope Categories

### Tools/Methods/Technologies
- Programming languages (Python, Java, JavaScript)
- Frameworks (React, Django, Spring)
- Platforms (AWS, Azure, GCP)
- Tools (Git, Jenkins, Docker)
- Methodologies (Agile, TDD, CI/CD)

### Standards/Frameworks
- Industry standards (ISO 27001, SOC 2, HIPAA)
- Development standards (OpenAPI, WCAG, OWASP)
- Frameworks (ITIL, TOGAF, COBIT)
- Best practices (12-Factor App, Clean Code)

### Typical Outputs
- Documents (specifications, designs, reports)
- Artifacts (code, configurations, models)
- Deliverables (features, releases, integrations)
- Reviews (code reviews, test results, audits)
