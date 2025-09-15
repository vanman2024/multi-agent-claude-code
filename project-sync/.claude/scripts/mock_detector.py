#!/usr/bin/env python3
"""
Production Readiness Mock Detection Script
Extends Claude Code's capabilities for comprehensive mock detection and API validation
"""

import os
import re
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class MockIssue:
    """Represents a mock implementation that needs attention"""
    file_path: str
    line_number: int
    severity: str  # critical, warning, info
    category: str  # api, database, auth, payment, etc.
    pattern_matched: str
    context: str
    suggestion: str
    estimated_effort: str  # hours/days

@dataclass
class ProductionReport:
    """Complete production readiness report"""
    timestamp: str
    project_name: str
    total_files_scanned: int
    mock_issues: List[MockIssue]
    api_endpoints: Dict[str, str]  # endpoint -> status
    config_issues: List[str]
    security_issues: List[str]
    summary: Dict[str, int]

class MockDetector:
    """Advanced mock detection and production readiness analyzer"""
    
    # Mock detection patterns with severity and categories
    MOCK_PATTERNS = {
        'critical': {
            'payment': [
                r'mock.*payment|fake.*payment|dummy.*payment',
                r'stripe.*test|paypal.*sandbox|fake.*credit.*card',
                r'payment.*mock|billing.*fake'
            ],
            'auth': [
                r'mock.*auth|fake.*auth|dummy.*auth',
                r'jwt.*fake|token.*mock|auth.*placeholder',
                r'login.*mock|session.*fake'
            ],
            'database': [
                r'mock.*db|fake.*db|dummy.*db',
                r'sqlite:///:memory:|mock.*repository',
                r'test.*database|memory.*database'
            ],
            'external_api': [
                r'mock.*api|fake.*api|dummy.*api',
                r'api.*mock|external.*fake|third.*party.*mock',
                r'requests.*mock|http.*fake'
            ]
        },
        'warning': {
            'environment': [
                r'localhost:\d+|127\.0\.0\.1:\d+',
                r'test.*env|dev.*env|local.*env',
                r'debug.*true|development.*mode'
            ],
            'placeholder': [
                r'TODO.*implement|FIXME.*implement|HACK.*implement',
                r'placeholder|temporary|temp.*fix',
                r'NotImplementedError|raise.*NotImplemented'
            ]
        },
        'info': {
            'testing': [
                r'\.mockResolvedValue|\.mockReturnValue',
                r'jest\.mock|sinon\.stub|mocha\.mock',
                r'mock.*server|test.*server'
            ]
        }
    }

    # File patterns to scan
    FILE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', '.php',
        '.rb', '.swift', '.kt', '.cs', '.cpp', '.c', '.h', '.hpp'
    }

    # Configuration files to check
    CONFIG_FILES = [
        '.env', '.env.local', '.env.production', '.env.staging',
        'config.py', 'settings.py', 'next.config.js', 'nuxt.config.js',
        'docker-compose.yml', 'Dockerfile', 'package.json', 'requirements.txt',
        'go.mod', 'Cargo.toml', 'composer.json'
    ]

    def __init__(self, project_path: str = '.'):
        self.project_path = Path(project_path)
        self.mock_issues: List[MockIssue] = []
        self.api_endpoints: Dict[str, str] = {}
        self.config_issues: List[str] = []
        self.security_issues: List[str] = []
        
    def scan_project(self) -> ProductionReport:
        """Main method to scan project for production readiness"""
        print("🔍 Starting production readiness scan...")
        
        # Get all scannable files
        files_to_scan = self._get_files_to_scan()
        print(f"📁 Found {len(files_to_scan)} files to scan")
        
        # Scan for mocks
        for file_path in files_to_scan:
            self._scan_file_for_mocks(file_path)
            
        # Check configuration files
        self._check_configuration_files()
        
        # Scan for API endpoints
        self._scan_api_endpoints(files_to_scan)
        
        # Security scan
        self._security_scan(files_to_scan)
        
        # Generate report
        return self._generate_report(len(files_to_scan))

    def _get_files_to_scan(self) -> List[Path]:
        """Get list of files to scan for mocks"""
        files = []
        for ext in self.FILE_EXTENSIONS:
            files.extend(self.project_path.rglob(f'*{ext}'))
        
        # Filter out common directories to skip
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                    'target', 'build', 'dist', '.next', 'coverage'}
        
        return [f for f in files if not any(skip in str(f) for skip in skip_dirs)]

    def _scan_file_for_mocks(self, file_path: Path) -> None:
        """Scan a single file for mock patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower().strip()
                
                # Check each pattern category
                for severity, categories in self.MOCK_PATTERNS.items():
                    for category, patterns in categories.items():
                        for pattern in patterns:
                            if re.search(pattern, line_lower):
                                issue = MockIssue(
                                    file_path=str(file_path.relative_to(self.project_path)),
                                    line_number=line_num,
                                    severity=severity,
                                    category=category,
                                    pattern_matched=pattern,
                                    context=line.strip(),
                                    suggestion=self._get_suggestion(category, line),
                                    estimated_effort=self._estimate_effort(severity, category)
                                )
                                self.mock_issues.append(issue)
                                
        except Exception as e:
            print(f"⚠️  Error scanning {file_path}: {e}")

    def _check_configuration_files(self) -> None:
        """Check configuration files for production readiness"""
        for config_file in self.CONFIG_FILES:
            config_path = self.project_path / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for common config issues
                    if 'localhost' in content.lower():
                        self.config_issues.append(f"{config_file}: Contains localhost references")
                        
                    if 'debug=true' in content.lower() or 'debug: true' in content.lower():
                        self.config_issues.append(f"{config_file}: Debug mode enabled")
                        
                    if 'test' in content.lower() and 'database' in content.lower():
                        self.config_issues.append(f"{config_file}: May be using test database")
                        
                except Exception as e:
                    self.config_issues.append(f"Error reading {config_file}: {e}")

    def _scan_api_endpoints(self, files: List[Path]) -> None:
        """Scan for API endpoint definitions and their status"""
        endpoint_patterns = [
            r'@app\.route\([\'"]([^\'"]+)[\'"]',  # Flask
            r'router\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]',  # Express/FastAPI
            r'app\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]',  # Express
            r'@(Get|Post|Put|Delete)\([\'"]([^\'"]+)[\'"]',  # Spring/NestJS
        ]
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                for pattern in endpoint_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Extract endpoint path (last group usually)
                        endpoint = match.groups()[-1]
                        
                        # Determine status based on implementation
                        status = "needs_review"
                        if 'mock' in content.lower() or 'fake' in content.lower():
                            status = "mock_implementation"
                        elif 'todo' in content.lower() or 'notimplemented' in content.lower():
                            status = "not_implemented"
                        else:
                            status = "ready"
                            
                        self.api_endpoints[endpoint] = status
                        
            except Exception:
                continue

    def _security_scan(self, files: List[Path]) -> None:
        """Basic security scan for common issues"""
        security_patterns = [
            r'password\s*=\s*[\'"][^\'"]+[\'"]',
            r'secret\s*=\s*[\'"][^\'"]+[\'"]',
            r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
            r'token\s*=\s*[\'"][^\'"]+[\'"]',
        ]
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                for pattern in security_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.security_issues.append(
                            f"Potential hardcoded secret in {file_path.relative_to(self.project_path)}"
                        )
                        
            except Exception:
                continue

    def _get_suggestion(self, category: str, line: str) -> str:
        """Get implementation suggestion based on category"""
        suggestions = {
            'payment': 'Replace with real payment processor integration (Stripe, PayPal, etc.)',
            'auth': 'implement proper JWT authentication with secure token handling',
            'database': 'Configure production database connection with proper credentials',
            'external_api': 'Replace with actual API integration and error handling',
            'environment': 'Update with production environment configuration',
            'placeholder': 'Implement actual functionality as specified in requirements',
            'testing': 'Ensure test mocks don\'t run in production environment'
        }
        return suggestions.get(category, 'Review and implement proper functionality')

    def _estimate_effort(self, severity: str, category: str) -> str:
        """Estimate effort required to fix"""
        effort_map = {
            ('critical', 'payment'): '2-4 days',
            ('critical', 'auth'): '1-2 days',
            ('critical', 'database'): '0.5-1 day',
            ('critical', 'external_api'): '1-3 days',
            ('warning', 'environment'): '2-4 hours',
            ('warning', 'placeholder'): '4-8 hours',
            ('info', 'testing'): '1-2 hours'
        }
        return effort_map.get((severity, category), '4-8 hours')

    def _generate_report(self, total_files: int) -> ProductionReport:
        """Generate final production readiness report"""
        # Calculate summary statistics
        summary = {
            'total_issues': len(self.mock_issues),
            'critical_issues': len([i for i in self.mock_issues if i.severity == 'critical']),
            'warning_issues': len([i for i in self.mock_issues if i.severity == 'warning']),
            'info_issues': len([i for i in self.mock_issues if i.severity == 'info']),
            'api_endpoints_total': len(self.api_endpoints),
            'api_endpoints_ready': len([v for v in self.api_endpoints.values() if v == 'ready']),
            'config_issues': len(self.config_issues),
            'security_issues': len(self.security_issues)
        }
        
        return ProductionReport(
            timestamp=datetime.now().isoformat(),
            project_name=self.project_path.name,
            total_files_scanned=total_files,
            mock_issues=self.mock_issues,
            api_endpoints=self.api_endpoints,
            config_issues=self.config_issues,
            security_issues=self.security_issues,
            summary=summary
        )

    def save_report(self, report: ProductionReport, output_format: str = 'markdown', 
                   filename: Optional[str] = None) -> str:
        """Save report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'production_readiness_report_{timestamp}'
            
        if output_format == 'json':
            filepath = f"{filename}.json"
            with open(filepath, 'w') as f:
                json.dump(asdict(report), f, indent=2)
        else:
            filepath = f"{filename}.md"
            with open(filepath, 'w') as f:
                f.write(self._format_markdown_report(report))
                
        return filepath

    def _format_markdown_report(self, report: ProductionReport) -> str:
        """Format report as markdown"""
        md = f"""# 🚨 Production Readiness Report

**Generated:** {report.timestamp}  
**Project:** {report.project_name}  
**Files Scanned:** {report.total_files_scanned}

## 📊 Executive Summary

- **Total Issues Found:** {report.summary['total_issues']}
- **Critical Issues:** {report.summary['critical_issues']} 🚨
- **Warning Issues:** {report.summary['warning_issues']} ⚠️
- **Info Issues:** {report.summary['info_issues']} ℹ️
- **API Endpoints:** {report.summary['api_endpoints_ready']}/{report.summary['api_endpoints_total']} ready

## 🚨 CRITICAL MOCK IMPLEMENTATIONS

"""
        
        critical_issues = [i for i in report.mock_issues if i.severity == 'critical']
        if critical_issues:
            for issue in critical_issues:
                md += f"""### {issue.category.title()} Mock - {issue.file_path}:{issue.line_number}
**Context:** `{issue.context}`  
**Issue:** {issue.pattern_matched}  
**Suggestion:** {issue.suggestion}  
**Estimated Effort:** {issue.estimated_effort}

"""
        else:
            md += "✅ No critical mock implementations found!\n\n"

        md += "## ⚠️ WARNING ISSUES\n\n"
        warning_issues = [i for i in report.mock_issues if i.severity == 'warning']
        for issue in warning_issues:
            md += f"- **{issue.file_path}:{issue.line_number}** - {issue.suggestion}\n"

        md += "\n## 🌐 API ENDPOINT STATUS\n\n"
        if report.api_endpoints:
            for endpoint, status in report.api_endpoints.items():
                emoji = "✅" if status == "ready" else "🚨" if status == "mock_implementation" else "⚠️"
                md += f"- {emoji} `{endpoint}` - {status.replace('_', ' ').title()}\n"
        else:
            md += "No API endpoints detected.\n"

        md += "\n## ⚙️ CONFIGURATION ISSUES\n\n"
        for issue in report.config_issues:
            md += f"- ⚠️ {issue}\n"

        md += "\n## 🔐 SECURITY ISSUES\n\n"
        for issue in report.security_issues:
            md += f"- 🚨 {issue}\n"

        md += f"""
## 🎯 NEXT STEPS

### Priority 1: Critical Issues ({report.summary['critical_issues']} items)
Fix all critical mock implementations before production deployment.

### Priority 2: Configuration ({len(report.config_issues)} items)  
Update environment configurations for production.

### Priority 3: API Validation ({report.summary['api_endpoints_total'] - report.summary['api_endpoints_ready']} endpoints)
Test and validate all API endpoints work with real data.

### Priority 4: Security Review ({len(report.security_issues)} items)
Address all security concerns before going live.

## 📈 PRODUCTION READINESS SCORE

**{((report.summary['api_endpoints_ready'] / max(report.summary['api_endpoints_total'], 1)) * 100 * 
   (1 - (report.summary['critical_issues'] / max(report.summary['total_issues'], 1)))):.0f}%**

*Score based on API readiness and absence of critical issues*
"""

        return md

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Production Readiness Mock Detection Tool')
    parser.add_argument('--path', default='.', help='Project path to scan')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', 
                       help='Output format')
    parser.add_argument('--output', help='Output filename (without extension)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = MockDetector(args.path)
    
    # Run scan
    report = detector.scan_project()
    
    # Save report
    output_file = detector.save_report(report, args.format, args.output)
    
    print(f"\n✅ Production readiness scan complete!")
    print(f"📊 Found {report.summary['total_issues']} issues ({report.summary['critical_issues']} critical)")
    print(f"📄 Report saved to: {output_file}")
    
    # Print summary to stdout
    if args.verbose or args.format == 'json':
        print(f"\n{json.dumps(report.summary, indent=2)}")

if __name__ == '__main__':
    main()