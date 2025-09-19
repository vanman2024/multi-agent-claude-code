"""Predefined Multi-Agent Workflow Templates."""

from ..workflows.models import (
    WorkflowDefinition,
    WorkflowStep,
    WorkflowType,
    WORKFLOW_REGISTRY,
)

# Codebase Analysis Workflow
CODEBASE_ANALYSIS_WORKFLOW = WorkflowDefinition(
    id="codebase-analysis-v1",
    name="Codebase Analysis Pipeline",
    description="Multi-agent workflow for comprehensive codebase analysis and insights",
    type=WorkflowType.PIPELINE,
    steps=[
        WorkflowStep(
            id="discover",
            name="Project Discovery",
            description="Scan project structure and identify key components",
            agent_type="claude",
            task="analyze_project_structure",
            parameters={
                "scan_depth": "comprehensive",
                "focus_areas": ["architecture", "dependencies", "configurations", "patterns"]
            },
        ),
        WorkflowStep(
            id="document",
            name="Documentation Analysis",
            description="Analyze existing documentation and identify gaps",
            agent_type="gemini",
            task="analyze_documentation",
            dependencies=["discover"],
            parameters={
                "scope": "full_codebase",
                "context_window": "2M",
                "output_format": "detailed_report"
            },
        ),
        WorkflowStep(
            id="optimize",
            name="Performance Analysis",
            description="Identify performance bottlenecks and optimization opportunities",
            agent_type="qwen",
            task="analyze_performance",
            dependencies=["discover"],
            parameters={
                "analysis_types": ["memory", "cpu", "network", "database"],
                "benchmarking": True,
                "optimization_suggestions": True
            },
        ),
        WorkflowStep(
            id="test",
            name="Testing Analysis",
            description="Review testing coverage and strategies",
            agent_type="codex",
            task="analyze_testing",
            dependencies=["discover"],
            parameters={
                "coverage_types": ["unit", "integration", "e2e"],
                "framework_review": True
            },
        ),
        WorkflowStep(
            id="synthesize",
            name="Synthesis Report",
            description="Combine all agent analyses into comprehensive recommendations",
            agent_type="claude",
            task="synthesize_analysis",
            dependencies=["document", "optimize", "test"],
            parameters={
                "report_format": "executive_summary",
                "include_roadmap": True
            },
        ),
    ],
)

# Security Audit Workflow
SECURITY_AUDIT_WORKFLOW = WorkflowDefinition(
    id="security-audit-v1",
    name="Security Audit Pipeline",
    description="Multi-agent workflow for comprehensive security assessment and compliance",
    type=WorkflowType.PIPELINE,
    steps=[
        WorkflowStep(
            id="scan_vulnerabilities",
            name="Vulnerability Scanning",
            description="Automated security vulnerability detection and analysis",
            agent_type="claude",
            task="security_vulnerability_scan",
            parameters={
                "scan_types": ["dependency", "code", "configuration"],
                "severity_threshold": "medium",
                "compliance_frameworks": ["OWASP", "NIST"]
            },
        ),
        WorkflowStep(
            id="auth_review",
            name="Authentication & Authorization Review",
            description="Review authentication mechanisms and access controls",
            agent_type="gemini",
            task="auth_security_review",
            dependencies=["scan_vulnerabilities"],
            parameters={
                "auth_methods": ["oauth", "jwt", "session"],
                "access_patterns": True,
                "context_window": "2M"
            },
        ),
        WorkflowStep(
            id="data_protection",
            name="Data Protection Analysis",
            description="Analyze data handling, encryption, and privacy practices",
            agent_type="qwen",
            task="data_protection_analysis",
            dependencies=["scan_vulnerabilities"],
            parameters={
                "encryption_standards": ["AES256", "RSA", "TLS"],
                "privacy_compliance": ["GDPR", "CCPA"],
                "data_flow_mapping": True
            },
        ),
        WorkflowStep(
            id="security_report",
            name="Security Assessment Report",
            description="Compile comprehensive security findings and recommendations",
            agent_type="claude",
            task="compile_security_report",
            dependencies=["auth_review", "data_protection"],
            parameters={
                "report_format": "executive_summary",
                "risk_scoring": True,
                "remediation_timeline": True
            },
        ),
    ],
)

# Production Readiness Workflow
PRODUCTION_READINESS_WORKFLOW = WorkflowDefinition(
    id="production-readiness-v1",
    name="Production Readiness Check",
    description="Multi-agent workflow for comprehensive production deployment validation",
    type=WorkflowType.VALIDATION,
    steps=[
        WorkflowStep(
            id="environment_check",
            name="Environment Configuration",
            description="Validate production environment settings and configurations",
            agent_type="claude",
            task="environment_validation",
            parameters={
                "config_types": ["database", "cache", "external_apis"],
                "secret_management": True,
                "environment_variables": True
            },
        ),
        WorkflowStep(
            id="performance_validation",
            name="Performance Benchmarking",
            description="Run performance tests and validate scalability metrics",
            agent_type="qwen",
            task="performance_benchmarking",
            dependencies=["environment_check"],
            parameters={
                "load_testing": True,
                "stress_testing": True,
                "scalability_targets": {"response_time": "200ms", "throughput": "1000rps"}
            },
        ),
        WorkflowStep(
            id="deployment_verification",
            name="Deployment Verification",
            description="Verify deployment artifacts and rollback procedures",
            agent_type="codex",
            task="deployment_verification",
            dependencies=["performance_validation"],
            parameters={
                "artifact_validation": True,
                "rollback_testing": True,
                "monitoring_setup": True
            },
        ),
    ],
)

# Register all workflows
WORKFLOW_REGISTRY.update({
    "codebase-analysis": CODEBASE_ANALYSIS_WORKFLOW,
    "security-audit": SECURITY_AUDIT_WORKFLOW,
    "production-readiness": PRODUCTION_READINESS_WORKFLOW,
})

# Workflow categories for organization
WORKFLOW_CATEGORIES = {
    "Development": ["codebase-analysis"],
    "Security": ["security-audit"],
    "Operations": ["production-readiness"],
}
