"""Variable (specialization-specific) content for the HR Round 2 SME Review Packets.

This module holds the data that swaps per specialization — competency content,
essential functions, and the competency-to-essential-function crosswalk. The
rendering engine and all stable boilerplate live in ``packet_builder.py``.

Three Human Resources job-family specializations are covered:
  - Total Rewards
  - Benefits & Leave
  - L&D Strategy & Training

Each competency carries a one-sentence definition and exactly three behavioral
indicators at each of four proficiency levels (L1-L4), per the TCB standard.
"""

from __future__ import annotations

# The HR job family is the parent for all three specializations in this packet
# set (the upstream sme-validation-package template was authored for Legal &
# Compliance; here it is reused for Human Resources).
JOB_FAMILY = "Cargill Human Resources"

# Bands under review (used for the essential-functions section and crosswalk).
BANDS = ["Manager II", "Advisor"]

# Which band's essential functions form the crosswalk matrix columns.
CROSSWALK_BAND = "Manager II"


def _levels(l1: list[str], l2: list[str], l3: list[str], l4: list[str]) -> dict[str, list[str]]:
    """Assemble a proficiency-level dict, asserting three indicators per level."""
    levels = {"L1": l1, "L2": l2, "L3": l3, "L4": l4}
    for key, indicators in levels.items():
        if len(indicators) != 3:
            raise ValueError(f"Level {key} must have exactly 3 indicators, got {len(indicators)}")
    return levels


# --------------------------------------------------------------------------- #
# Total Rewards
# --------------------------------------------------------------------------- #

TOTAL_REWARDS = {
    "name": "Total Rewards",
    "file_slug": "Total_Rewards",
    "description": (
        "The Total Rewards specialization designs, governs, and delivers Cargill's "
        "compensation, incentive, and recognition programs. Professionals in this "
        "specialization ensure that pay is internally equitable, externally competitive, "
        "compliant, and clearly understood — directly enabling Cargill's ability to "
        "attract, motivate, and retain talent across 15 job families and multiple "
        "geographies."
    ),
    "competencies": [
        {
            "name": "Compensation Structure Design",
            "definition": (
                "Designs and maintains base pay structures, salary ranges, and job "
                "architecture that align internal equity with external competitiveness."
            ),
            "levels": _levels(
                l1=[
                    "Applies existing salary ranges and grade structures to individual job placements under guidance.",
                    "Gathers the job documentation and organizational data needed for structure maintenance.",
                    "Explains the components of a pay structure (grades, ranges, midpoints) to managers when asked.",
                ],
                l2=[
                    "Independently builds and updates salary ranges using approved methodology and market data.",
                    "Resolves placement and slotting questions for standard roles within established policy.",
                    "Recommends grade assignments for new or revised jobs based on job evaluation results.",
                ],
                l3=[
                    "Designs grade and range structures for a business unit, balancing competitiveness, cost, and internal equity.",
                    "Diagnoses structural issues such as compression, range overlap, and drift, and proposes corrective frameworks.",
                    "Advises HR and business leaders on the structure implications of reorganizations and acquisitions.",
                ],
                l4=[
                    "Defines the enterprise job architecture and compensation philosophy across regions and businesses.",
                    "Sets the standards and governance for how pay structures are built, maintained, and audited company-wide.",
                    "Influences executive decisions on pay-positioning strategy relative to evolving labor markets.",
                ],
            ),
        },
        {
            "name": "Market Pricing & Benchmarking",
            "definition": (
                "Matches Cargill roles to external survey data and analyzes market "
                "competitiveness to inform pay decisions."
            ),
            "levels": _levels(
                l1=[
                    "Matches standard jobs to survey benchmarks using established matching guidelines.",
                    "Extracts and organizes survey data into the pricing template accurately.",
                    "Flags obvious match discrepancies to a senior analyst for review.",
                ],
                l2=[
                    "Independently prices the full range of standard roles across multiple survey sources.",
                    "Reconciles conflicting survey data and selects appropriate market references with rationale.",
                    "Produces competitiveness analyses (compa-ratio, market index) for a function or location.",
                ],
                l3=[
                    "Designs the survey-participation and benchmarking strategy for a business or region.",
                    "Evaluates survey methodology quality and recommends which sources to weight or retire.",
                    "Translates market analysis into actionable pay-positioning recommendations for leaders.",
                ],
                l4=[
                    "Sets enterprise standards for market-pricing methodology, survey vendors, and data governance.",
                    "Anticipates labor-market shifts and advises executives on strategic repositioning.",
                    "Represents Cargill in compensation survey consortia and shapes industry benchmarking practice.",
                ],
            ),
        },
        {
            "name": "Incentive & Variable Pay Design",
            "definition": (
                "Designs short- and long-term incentive plans that motivate performance "
                "and align with business and shareholder outcomes."
            ),
            "levels": _levels(
                l1=[
                    "Applies existing incentive-plan rules to calculate individual awards accurately.",
                    "Prepares incentive-plan documentation and participant communications from templates.",
                    "Answers routine participant questions about plan mechanics and timing.",
                ],
                l2=[
                    "Models incentive payout scenarios and costs for standard plans under varying performance.",
                    "Recommends target and threshold settings for existing plans based on data.",
                    "Identifies design issues that create unintended behavior or excessive cost.",
                ],
                l3=[
                    "Designs incentive plans for a business unit, linking metrics to strategy and risk appetite.",
                    "Advises leaders on plan trade-offs (leverage, metrics, payout curves) with quantified impact.",
                    "Leads annual incentive-design reviews and governance approvals for a function.",
                ],
                l4=[
                    "Defines the enterprise incentive philosophy and the framework governing all variable pay programs.",
                    "Designs executive and long-term incentive structures in partnership with the Compensation Committee.",
                    "Shapes the link between pay, performance, and shareholder value at the enterprise level.",
                ],
            ),
        },
        {
            "name": "Pay Equity Analysis",
            "definition": (
                "Analyzes pay data to identify, explain, and remediate inequitable pay "
                "differences across protected groups and roles."
            ),
            "levels": _levels(
                l1=[
                    "Compiles and validates the demographic and pay data required for equity analysis.",
                    "Runs standard equity reports using established templates and tools.",
                    "Documents data anomalies and escalates potential issues to senior analysts.",
                ],
                l2=[
                    "Conducts statistical pay-equity analyses for a population and interprets standard results.",
                    "Identifies legitimate explanatory factors and isolates unexplained pay gaps.",
                    "Recommends individual remediation actions consistent with policy and budget.",
                ],
                l3=[
                    "Designs the pay-equity review approach and methodology for a region or business.",
                    "Advises leaders and legal partners on findings, risk exposure, and remediation strategy.",
                    "Builds controls that prevent inequities from re-emerging through pay decisions.",
                ],
                l4=[
                    "Sets enterprise pay-equity strategy, methodology, and governance across jurisdictions.",
                    "Advises executives and the Board on systemic equity risk and disclosure positioning.",
                    "Influences external standards and regulatory engagement on pay transparency and equity.",
                ],
            ),
        },
        {
            "name": "Total Rewards Communication",
            "definition": (
                "Translates complex rewards programs into clear, persuasive communications "
                "that help employees understand and value their total rewards."
            ),
            "levels": _levels(
                l1=[
                    "Drafts routine rewards communications from approved templates and talking points.",
                    "Answers common employee questions about pay and rewards accurately.",
                    "Maintains FAQ and self-service content under guidance.",
                ],
                l2=[
                    "Develops communication materials for a rewards program or cycle independently.",
                    "Tailors messaging for different audiences (managers, employees, regions).",
                    "Gathers and incorporates employee feedback to improve clarity.",
                ],
                l3=[
                    "Designs the total rewards communication strategy for a program launch or annual cycle.",
                    "Advises leaders on framing sensitive rewards changes to sustain trust and engagement.",
                    "Measures communication effectiveness and adjusts approach based on data.",
                ],
                l4=[
                    "Defines the enterprise total rewards communication and employee value proposition strategy.",
                    "Shapes how Cargill positions total rewards in the talent market and to the workforce.",
                    "Sets standards and capability for rewards communication across all businesses and regions.",
                ],
            ),
        },
    ],
    "essential_functions": {
        "Manager II": [
            "Lead the design and governance of compensation structures and total rewards programs for assigned businesses.",
            "Direct market benchmarking and competitiveness analysis to inform pay positioning.",
            "Oversee incentive and variable pay plan design and annual administration.",
            "Ensure pay equity and compliance with pay-related regulations across the portfolio.",
            "Advise senior business and HR leaders on total rewards strategy and trade-offs.",
            "Manage total rewards communication and change for major program launches.",
        ],
        "Advisor": [
            "Serve as deep technical expert on compensation design and market-pricing methodology.",
            "Conduct complex competitiveness, costing, and equity analyses for the enterprise.",
            "Design incentive and recognition solutions for complex or executive populations.",
            "Provide authoritative guidance on pay regulations and equity risk.",
            "Develop tools, standards, and capability for the total rewards community.",
            "Partner with leaders to translate rewards strategy into actionable plans.",
        ],
    },
    # Crosswalk: competency name -> 1-based essential-function numbers (Manager II band).
    "crosswalk": {
        "Compensation Structure Design": [1, 5],
        "Market Pricing & Benchmarking": [1, 2],
        "Incentive & Variable Pay Design": [3, 5],
        "Pay Equity Analysis": [4],
        "Total Rewards Communication": [5, 6],
    },
}


# --------------------------------------------------------------------------- #
# Benefits & Leave
# --------------------------------------------------------------------------- #

BENEFITS_LEAVE = {
    "name": "Benefits & Leave",
    "file_slug": "Benefits_Leave",
    "description": (
        "The Benefits & Leave specialization designs and administers Cargill's health, "
        "welfare, retirement, and leave programs. Professionals in this specialization "
        "protect the financial security and wellbeing of the workforce while ensuring "
        "fiduciary integrity, regulatory compliance, cost effectiveness, and a "
        "high-quality employee experience across jurisdictions."
    ),
    "competencies": [
        {
            "name": "Health & Welfare Plan Management",
            "definition": (
                "Manages the design, administration, and performance of medical, dental, "
                "and other health and welfare benefit plans."
            ),
            "levels": _levels(
                l1=[
                    "Processes standard enrollment, eligibility, and life-event transactions accurately.",
                    "Responds to routine employee benefit inquiries using plan documents.",
                    "Maintains plan documentation and audit files under guidance.",
                ],
                l2=[
                    "Administers the full range of health and welfare plans independently across a population.",
                    "Resolves complex eligibility, coverage, and claims escalations within policy.",
                    "Analyzes plan utilization and cost data to support renewal recommendations.",
                ],
                l3=[
                    "Designs and recommends health and welfare plan changes for a business or region.",
                    "Manages annual renewal strategy, balancing cost, competitiveness, and employee impact.",
                    "Advises leaders on plan-design trade-offs with quantified cost and risk analysis.",
                ],
                l4=[
                    "Defines the enterprise health and welfare benefits strategy and philosophy.",
                    "Sets governance and standards for plan design, funding, and vendor performance globally.",
                    "Influences executive decisions on benefits investment and workforce health strategy.",
                ],
            ),
        },
        {
            "name": "Retirement & Savings Plan Administration",
            "definition": (
                "Administers and governs defined-contribution, pension, and savings plans "
                "in compliance with fiduciary and regulatory requirements."
            ),
            "levels": _levels(
                l1=[
                    "Processes contributions, deferrals, and standard retirement transactions accurately.",
                    "Responds to routine participant questions about plan features and timing.",
                    "Maintains plan records and supports audit data requests under guidance.",
                ],
                l2=[
                    "Administers retirement and savings plans independently, including complex transactions.",
                    "Reconciles plan data with recordkeepers and resolves discrepancies.",
                    "Supports compliance testing and required filings with accurate data.",
                ],
                l3=[
                    "Manages plan governance, fiduciary processes, and recordkeeper performance for a region.",
                    "Advises committees on plan design, investment menu, and participant outcomes.",
                    "Leads remediation of compliance or operational findings.",
                ],
                l4=[
                    "Defines enterprise retirement and savings strategy and the fiduciary governance framework.",
                    "Advises executives and plan fiduciary committees on strategy and risk.",
                    "Shapes the long-term financial-security strategy for the global workforce.",
                ],
            ),
        },
        {
            "name": "Leave & Absence Management",
            "definition": (
                "Administers leave programs and absence policies in compliance with "
                "statutory requirements while supporting employees and managers."
            ),
            "levels": _levels(
                l1=[
                    "Processes standard leave requests and tracks absence per policy and statute.",
                    "Provides employees and managers routine guidance on leave types and eligibility.",
                    "Maintains accurate leave records and documentation under guidance.",
                ],
                l2=[
                    "Administers complex and concurrent leaves (FMLA, disability, statutory) independently.",
                    "Coordinates leave with pay, benefits, and accommodation processes.",
                    "Resolves escalated leave issues within policy and legal requirements.",
                ],
                l3=[
                    "Designs leave and absence policy and process for a region, ensuring compliance and consistency.",
                    "Advises managers and HR on complex, high-risk, or precedent-setting cases.",
                    "Analyzes absence trends and recommends program and policy improvements.",
                ],
                l4=[
                    "Defines enterprise leave and absence strategy across jurisdictions.",
                    "Sets governance, vendor standards, and the compliance framework for all leave programs.",
                    "Influences executive and policy decisions on workforce flexibility and wellbeing.",
                ],
            ),
        },
        {
            "name": "Benefits Compliance & Governance",
            "definition": (
                "Ensures benefit programs comply with applicable laws and regulations "
                "through governance, documentation, and controls."
            ),
            "levels": _levels(
                l1=[
                    "Gathers documentation and data required for compliance filings and audits.",
                    "Applies established compliance checklists to routine benefit processes.",
                    "Flags potential compliance gaps to senior staff.",
                ],
                l2=[
                    "Manages required filings, notices, and nondiscrimination testing for assigned plans.",
                    "Interprets standard regulatory requirements and applies them to administration.",
                    "Documents controls and supports internal and external audits independently.",
                ],
                l3=[
                    "Designs the compliance and governance framework for benefit programs in a region.",
                    "Advises leaders and legal partners on regulatory change and risk exposure.",
                    "Leads remediation and control improvements following findings or law changes.",
                ],
                l4=[
                    "Sets enterprise benefits compliance strategy and governance across jurisdictions.",
                    "Advises executives and the Board on systemic benefits-compliance risk.",
                    "Influences external regulatory engagement and industry compliance practice.",
                ],
            ),
        },
        {
            "name": "Vendor & Carrier Management",
            "definition": (
                "Selects and manages benefit vendors and carriers to ensure service "
                "quality, cost effectiveness, and contractual performance."
            ),
            "levels": _levels(
                l1=[
                    "Tracks vendor service requests and routine performance data accurately.",
                    "Coordinates standard vendor transactions and escalations under guidance.",
                    "Maintains vendor contact and contract documentation.",
                ],
                l2=[
                    "Manages day-to-day vendor relationships and service levels for assigned plans.",
                    "Analyzes vendor performance against service standards and identifies issues.",
                    "Supports renewals and RFPs with accurate data and evaluation input.",
                ],
                l3=[
                    "Leads vendor selection, RFPs, and contract negotiation for a business or region.",
                    "Manages strategic vendor relationships and holds carriers to performance commitments.",
                    "Advises leaders on vendor strategy, consolidation, and cost trade-offs.",
                ],
                l4=[
                    "Defines enterprise benefits vendor and sourcing strategy.",
                    "Sets standards and governance for vendor selection, performance, and risk globally.",
                    "Influences market and carrier practices through Cargill's scale and partnership.",
                ],
            ),
        },
    ],
    "essential_functions": {
        "Manager II": [
            "Lead design, funding, and governance of health, welfare, and retirement programs.",
            "Direct leave and absence program strategy and compliance across the portfolio.",
            "Ensure benefits compliance with applicable laws and fiduciary requirements.",
            "Manage vendor and carrier strategy, selection, and performance.",
            "Advise senior leaders on benefits strategy, cost, and workforce impact.",
            "Oversee benefits administration quality and the employee experience.",
        ],
        "Advisor": [
            "Serve as deep technical expert on health, welfare, and retirement plan design.",
            "Provide authoritative guidance on benefits and leave compliance and fiduciary matters.",
            "Lead complex plan analyses, renewals, and remediation.",
            "Manage strategic vendor relationships and contract performance.",
            "Develop standards, tools, and capability for the benefits community.",
            "Partner with leaders and legal on high-risk and precedent-setting cases.",
        ],
    },
    "crosswalk": {
        "Health & Welfare Plan Management": [1, 5, 6],
        "Retirement & Savings Plan Administration": [1, 3],
        "Leave & Absence Management": [2, 6],
        "Benefits Compliance & Governance": [3],
        "Vendor & Carrier Management": [4],
    },
}


# --------------------------------------------------------------------------- #
# L&D Strategy & Training
# --------------------------------------------------------------------------- #

LD_STRATEGY_TRAINING = {
    "name": "L&D Strategy & Training",
    "file_slug": "LD_Strategy_Training",
    "description": (
        "The Learning & Development Strategy and Training specialization builds "
        "organizational capability through the diagnosis of needs and the design, "
        "delivery, and measurement of learning. Professionals in this specialization "
        "connect business strategy to workforce capability, deploying learning solutions "
        "and technologies that demonstrably improve performance across Cargill."
    ),
    "competencies": [
        {
            "name": "Learning Needs Analysis",
            "definition": (
                "Diagnoses performance and capability gaps to determine whether and what "
                "learning solutions are required."
            ),
            "levels": _levels(
                l1=[
                    "Collects needs data (surveys, interviews, performance data) using provided tools.",
                    "Summarizes findings into standard needs-analysis templates.",
                    "Distinguishes learning needs from non-learning issues with guidance.",
                ],
                l2=[
                    "Conducts end-to-end needs analyses for a function or program independently.",
                    "Recommends whether learning, process, or other interventions best address a gap.",
                    "Links identified needs to measurable performance outcomes.",
                ],
                l3=[
                    "Designs the needs-analysis approach for a business or capability area.",
                    "Advises leaders on capability priorities based on strategy and workforce data.",
                    "Synthesizes enterprise data to identify systemic capability gaps.",
                ],
                l4=[
                    "Defines the enterprise approach to capability diagnosis and skills intelligence.",
                    "Shapes how learning investment is prioritized against business strategy.",
                    "Influences executive workforce-capability and skills strategy decisions.",
                ],
            ),
        },
        {
            "name": "Instructional Design",
            "definition": (
                "Designs learning experiences grounded in adult-learning principles that "
                "achieve defined performance objectives."
            ),
            "levels": _levels(
                l1=[
                    "Develops learning content from approved designs and storyboards.",
                    "Applies standard templates and design patterns under guidance.",
                    "Writes clear learning objectives for routine modules.",
                ],
                l2=[
                    "Designs complete learning solutions (objectives, content, assessment) independently.",
                    "Selects appropriate modalities and methods for the audience and objectives.",
                    "Builds assessments that validly measure stated objectives.",
                ],
                l3=[
                    "Designs blended and curriculum-level solutions for a capability area.",
                    "Advises on design strategy, modality mix, and learning-experience architecture.",
                    "Coaches designers and sets quality standards for a portfolio.",
                ],
                l4=[
                    "Defines enterprise learning-design standards and methodology.",
                    "Shapes the organization's learning-experience and design capability.",
                    "Influences industry practice in learning design and adult learning.",
                ],
            ),
        },
        {
            "name": "Learning Program Delivery",
            "definition": (
                "Facilitates and manages the delivery of learning programs that engage "
                "learners and achieve learning transfer."
            ),
            "levels": _levels(
                l1=[
                    "Facilitates standard sessions following an established facilitator guide.",
                    "Manages logistics, materials, and learner communications for a program.",
                    "Gathers learner reaction data using standard instruments.",
                ],
                l2=[
                    "Facilitates complex or sensitive sessions and adapts to learner needs in the moment.",
                    "Manages multi-session program delivery end to end independently.",
                    "Coaches managers to reinforce learning transfer on the job.",
                ],
                l3=[
                    "Designs the delivery and transfer strategy for a program portfolio.",
                    "Builds and develops a facilitator network and quality standards.",
                    "Advises leaders on scaling delivery across regions and modalities.",
                ],
                l4=[
                    "Defines enterprise strategy for learning delivery and transfer at scale.",
                    "Shapes the facilitation capability and delivery model across the company.",
                    "Influences how Cargill builds capability through experiential and social learning.",
                ],
            ),
        },
        {
            "name": "Learning Technology & LMS Management",
            "definition": (
                "Manages learning platforms and technologies to enable effective, "
                "scalable, and measurable learning."
            ),
            "levels": _levels(
                l1=[
                    "Performs standard LMS administration (enrollments, content loads, reporting).",
                    "Resolves routine user and access issues following procedures.",
                    "Maintains content metadata and catalog accuracy under guidance.",
                ],
                l2=[
                    "Configures and manages LMS and learning-tech workflows independently.",
                    "Troubleshoots complex platform and integration issues.",
                    "Builds reports and dashboards that meet stakeholder needs.",
                ],
                l3=[
                    "Designs the learning-technology architecture and roadmap for a business.",
                    "Advises on platform selection, integration, and data strategy.",
                    "Leads implementations and major configuration or migration efforts.",
                ],
                l4=[
                    "Defines the enterprise learning-technology strategy and ecosystem.",
                    "Sets standards and governance for learning data, platforms, and AI-enabled learning.",
                    "Influences the market and vendor roadmap through Cargill's requirements and scale.",
                ],
            ),
        },
        {
            "name": "Learning Impact Measurement",
            "definition": (
                "Measures and evaluates learning outcomes and business impact to "
                "demonstrate value and drive improvement."
            ),
            "levels": _levels(
                l1=[
                    "Collects evaluation data (reaction, learning) using standard instruments.",
                    "Produces standard evaluation reports from templates.",
                    "Maintains accurate evaluation records under guidance.",
                ],
                l2=[
                    "Designs and runs evaluations through behavior and results levels for a program.",
                    "Analyzes data to identify what is and is not driving outcomes.",
                    "Recommends program improvements based on evaluation evidence.",
                ],
                l3=[
                    "Designs the measurement strategy and framework for a portfolio or business.",
                    "Advises leaders on learning ROI, leading indicators, and impact narratives.",
                    "Builds analytics that connect learning to performance and business metrics.",
                ],
                l4=[
                    "Defines the enterprise learning-measurement strategy and standards.",
                    "Shapes how learning value is quantified and communicated to executives.",
                    "Influences industry practice in learning analytics and impact evaluation.",
                ],
            ),
        },
    ],
    "essential_functions": {
        "Manager II": [
            "Lead learning strategy and capability planning for assigned businesses.",
            "Direct design and delivery of learning programs aligned to business priorities.",
            "Manage learning-technology strategy and platform performance.",
            "Ensure measurement and demonstration of learning impact and ROI.",
            "Advise senior leaders on capability building and workforce development.",
            "Lead the learning team and develop learning-professional capability.",
        ],
        "Advisor": [
            "Serve as deep technical expert on instructional design and adult learning.",
            "Lead complex needs analyses and capability diagnostics for the enterprise.",
            "Design enterprise curricula and blended learning architectures.",
            "Provide authoritative guidance on learning measurement and analytics.",
            "Develop standards, tools, and capability for the learning community.",
            "Partner with leaders to translate capability strategy into learning solutions.",
        ],
    },
    "crosswalk": {
        "Learning Needs Analysis": [1, 5],
        "Instructional Design": [2],
        "Learning Program Delivery": [2, 6],
        "Learning Technology & LMS Management": [3],
        "Learning Impact Measurement": [4],
    },
}


SPECIALIZATIONS = {
    "total_rewards": TOTAL_REWARDS,
    "benefits_leave": BENEFITS_LEAVE,
    "ld_strategy_training": LD_STRATEGY_TRAINING,
}
