"""Predefined Multi-Agent Workflow Templates."""

from ..workflows.models import (
    WorkflowDefinition,
    WorkflowStep,
    WorkflowType,
    WORKFLOW_REGISTRY,
)

# Lead Generation Workflow
LEAD_GENERATION_WORKFLOW = WorkflowDefinition(
    id="lead-generation-v1",
    name="Lead Generation Pipeline",
    description="Multi-agent workflow for comprehensive lead generation and qualification",
    type=WorkflowType.PIPELINE,
    steps=[
        WorkflowStep(
            id="search",
            name="Initial Search",
            description="Search for potential leads using multiple criteria",
            agent_type="search_agent",
            task="search_leads",
            parameters={
                "sources": ["linkedin", "company_websites", "news", "social_media"],
                "criteria": ["job_title", "company_size", "industry", "location"]
            },
        ),
        WorkflowStep(
            id="enrich",
            name="Data Enrichment",
            description="Enrich lead data with additional information",
            agent_type="enrichment_agent",
            task="enrich_profiles",
            dependencies=["search"],
            parameters={
                "fields": ["company_size", "industry", "social_profiles", "contact_info"],
                "validation": True
            },
        ),
        WorkflowStep(
            id="score",
            name="Lead Scoring",
            description="Score leads based on engagement and fit criteria",
            agent_type="analysis_agent",
            task="score_leads",
            dependencies=["enrich"],
            parameters={
                "criteria": ["job_title_match", "company_size", "engagement", "social_presence"],
                "weights": {"job_title_match": 0.4, "company_size": 0.3, "engagement": 0.2, "social_presence": 0.1}
            },
        ),
        WorkflowStep(
            id="validate",
            name="Contact Validation",
            description="Validate contact information and reachability",
            agent_type="validation_agent",
            task="validate_contacts",
            dependencies=["score"],
            parameters={
                "validation_types": ["email", "phone", "social", "website"],
                "timeout": 30
            },
        ),
        WorkflowStep(
            id="segment",
            name="Lead Segmentation",
            description="Segment leads into categories for targeted outreach",
            agent_type="segmentation_agent",
            task="segment_leads",
            dependencies=["validate"],
            parameters={
                "segments": ["hot_leads", "warm_leads", "cold_leads", "qualified", "unqualified"]
            },
        ),
    ],
)

# Content Generation Workflow
CONTENT_GENERATION_WORKFLOW = WorkflowDefinition(
    id="content-generation-v1",
    name="Content Generation Pipeline",
    description="Multi-agent workflow for content creation, editing, and optimization",
    type=WorkflowType.SEQUENTIAL,
    steps=[
        WorkflowStep(
            id="research",
            name="Topic Research",
            description="Research trending topics and audience interests",
            agent_type="research_agent",
            task="research_topic",
            parameters={"depth": "comprehensive", "sources": ["trends", "social", "news"]},
        ),
        WorkflowStep(
            id="outline",
            name="Content Outline",
            description="Create detailed content outline and structure",
            agent_type="planning_agent",
            task="create_outline",
            dependencies=["research"],
            parameters={"structure": "standard", "sections": 5},
        ),
        WorkflowStep(
            id="write",
            name="Content Writing",
            description="Write the main content based on outline",
            agent_type="writing_agent",
            task="write_content",
            dependencies=["outline"],
            parameters={"tone": "professional", "length": "medium", "style": "engaging"},
        ),
        WorkflowStep(
            id="edit",
            name="Content Editing",
            description="Edit and polish the written content",
            agent_type="editing_agent",
            task="edit_content",
            dependencies=["write"],
            parameters={"focus": ["grammar", "clarity", "flow", "engagement"]},
        ),
        WorkflowStep(
            id="optimize",
            name="SEO Optimization",
            description="Optimize content for search engines",
            agent_type="seo_agent",
            task="optimize_seo",
            dependencies=["edit"],
            parameters={"keywords": "auto", "readability": "high", "meta_tags": True},
        ),
        WorkflowStep(
            id="review",
            name="Final Review",
            description="Final quality review and approval",
            agent_type="review_agent",
            task="final_review",
            dependencies=["optimize"],
            parameters={"criteria": ["accuracy", "engagement", "seo", "brand_alignment"]},
        ),
    ],
)

# Data Analysis Workflow
DATA_ANALYSIS_WORKFLOW = WorkflowDefinition(
    id="data-analysis-v1",
    name="Data Analysis Pipeline",
    description="Multi-agent workflow for comprehensive data analysis and insights",
    type=WorkflowType.PIPELINE,
    steps=[
        WorkflowStep(
            id="collect",
            name="Data Collection",
            description="Collect and aggregate data from multiple sources",
            agent_type="data_agent",
            task="collect_data",
            parameters={"sources": ["database", "api", "files"], "format": "standardized"},
        ),
        WorkflowStep(
            id="clean",
            name="Data Cleaning",
            description="Clean and preprocess the collected data",
            agent_type="cleaning_agent",
            task="clean_data",
            dependencies=["collect"],
            parameters={"methods": ["remove_duplicates", "handle_missing", "normalize", "validate"]},
        ),
        WorkflowStep(
            id="analyze",
            name="Statistical Analysis",
            description="Perform statistical analysis on cleaned data",
            agent_type="analysis_agent",
            task="statistical_analysis",
            dependencies=["clean"],
            parameters={"methods": ["descriptive", "correlation", "regression", "clustering"]},
        ),
        WorkflowStep(
            id="visualize",
            name="Data Visualization",
            description="Create visualizations and charts",
            agent_type="visualization_agent",
            task="create_visualizations",
            dependencies=["analyze"],
            parameters={"types": ["charts", "graphs", "dashboards"], "format": "interactive"},
        ),
        WorkflowStep(
            id="insights",
            name="Generate Insights",
            description="Extract key insights and recommendations",
            agent_type="insights_agent",
            task="generate_insights",
            dependencies=["analyze"],
            parameters={"focus": ["trends", "anomalies", "opportunities", "recommendations"]},
        ),
    ],
)

# Customer Support Workflow
CUSTOMER_SUPPORT_WORKFLOW = WorkflowDefinition(
    id="customer-support-v1",
    name="Customer Support Automation",
    description="Multi-agent workflow for automated customer support and issue resolution",
    type=WorkflowType.CONDITIONAL,
    steps=[
        WorkflowStep(
            id="classify",
            name="Issue Classification",
            description="Classify and categorize customer issues",
            agent_type="classification_agent",
            task="classify_issue",
            parameters={"categories": ["technical", "billing", "account", "general"]},
        ),
        WorkflowStep(
            id="route",
            name="Issue Routing",
            description="Route issues to appropriate support channels",
            agent_type="routing_agent",
            task="route_issue",
            dependencies=["classify"],
            parameters={"escalation_rules": "auto", "priority_matrix": "standard"},
        ),
        WorkflowStep(
            id="diagnose",
            name="Problem Diagnosis",
            description="Diagnose technical or service issues",
            agent_type="diagnostic_agent",
            task="diagnose_problem",
            dependencies=["route"],
            parameters={"diagnostic_tools": ["logs", "system_check", "user_history"]},
        ),
        WorkflowStep(
            id="resolve",
            name="Issue Resolution",
            description="Provide solutions and resolve issues",
            agent_type="resolution_agent",
            task="resolve_issue",
            dependencies=["diagnose"],
            parameters={"resolution_types": ["automated", "guided", "escalated"]},
        ),
        WorkflowStep(
            id="followup",
            name="Follow-up",
            description="Follow up with customer to ensure satisfaction",
            agent_type="followup_agent",
            task="customer_followup",
            dependencies=["resolve"],
            parameters={"timing": "24h", "survey": True},
        ),
    ],
)

# Research and Development Workflow
RESEARCH_WORKFLOW = WorkflowDefinition(
    id="research-development-v1",
    name="Research and Development Pipeline",
    description="Multi-agent workflow for research, experimentation, and development",
    type=WorkflowType.SEQUENTIAL,
    steps=[
        WorkflowStep(
            id="hypothesis",
            name="Hypothesis Generation",
            description="Generate research hypotheses and questions",
            agent_type="research_agent",
            task="generate_hypothesis",
            parameters={"domain": "specified", "creativity": "high"},
        ),
        WorkflowStep(
            id="literature",
            name="Literature Review",
            description="Review existing literature and research",
            agent_type="literature_agent",
            task="literature_review",
            dependencies=["hypothesis"],
            parameters={"sources": ["academic", "industry", "patents"], "depth": "comprehensive"},
        ),
        WorkflowStep(
            id="design",
            name="Experiment Design",
            description="Design experiments and methodologies",
            agent_type="design_agent",
            task="design_experiment",
            dependencies=["literature"],
            parameters={"methodology": "scientific", "controls": "standard"},
        ),
        WorkflowStep(
            id="execute",
            name="Experiment Execution",
            description="Execute designed experiments",
            agent_type="execution_agent",
            task="execute_experiment",
            dependencies=["design"],
            parameters={"monitoring": "real-time", "data_collection": "automated"},
        ),
        WorkflowStep(
            id="analyze_results",
            name="Results Analysis",
            description="Analyze experiment results and findings",
            agent_type="analysis_agent",
            task="analyze_results",
            dependencies=["execute"],
            parameters={"methods": ["statistical", "qualitative", "comparative"]},
        ),
        WorkflowStep(
            id="conclusion",
            name="Draw Conclusions",
            description="Draw conclusions and formulate recommendations",
            agent_type="conclusion_agent",
            task="draw_conclusions",
            dependencies=["analyze_results"],
            parameters={"confidence_level": "high", "actionable": True},
        ),
    ],
)

# Register all workflows
WORKFLOW_REGISTRY.update({
    "lead-generation": LEAD_GENERATION_WORKFLOW,
    "content-generation": CONTENT_GENERATION_WORKFLOW,
    "data-analysis": DATA_ANALYSIS_WORKFLOW,
    "customer-support": CUSTOMER_SUPPORT_WORKFLOW,
    "research-development": RESEARCH_WORKFLOW,
})

# Workflow categories for organization
WORKFLOW_CATEGORIES = {
    "Business": ["lead-generation", "customer-support"],
    "Content": ["content-generation"],
    "Data": ["data-analysis"],
    "Research": ["research-development"],
}
