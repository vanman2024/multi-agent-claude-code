#!/usr/bin/env python3
"""
Setup script for SignalHire Agent

This setup.py provides backward compatibility for pip install -e .
The main configuration is in pyproject.toml following modern Python packaging standards.
"""

from setuptools import setup, find_packages
import sys
import os
from pathlib import Path

# Ensure Python 3.11+
if sys.version_info < (3, 11):
    sys.exit("Error: SignalHire Agent requires Python 3.11 or higher")

# Read long description from README
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "AI-powered lead generation automation for SignalHire with multi-platform expansion capabilities"

# Read version from pyproject.toml or default
version = "0.1.0"
try:
    import tomllib
    pyproject_path = Path(__file__).parent / "pyproject.toml"
    if pyproject_path.exists():
        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)
            version = pyproject.get("project", {}).get("version", version)
except ImportError:
    # tomllib not available in Python < 3.11
    pass

# Read requirements from requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)

# Development requirements
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0", 
    "pytest-mock>=3.10.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "pre-commit>=3.0.0",
]

# Optional dependencies for enhanced functionality
extras_require = {
    "dev": dev_requirements,
    "excel": ["openpyxl>=3.1.0"],
    "browser": [],  # browser automation removed
    "testing": ["pytest>=7.0.0", "pytest-asyncio>=0.21.0", "pytest-mock>=3.10.0"],
    "docs": ["sphinx>=7.0.0", "sphinx-rtd-theme>=1.3.0"],
}

# All optional dependencies
extras_require["all"] = [
    req for extra_deps in extras_require.values() 
    for req in extra_deps if isinstance(req, str)
]

setup(
    name="signalhire-agent",
    version=version,
    author="SignalHire Agent Team",
    author_email="team@signalhire-agent.com",
    description="AI-powered lead generation automation for SignalHire with multi-platform expansion capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/signalhire/signalhire-agent",
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    
    # Requirements
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require=extras_require,
    
    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "signalhire-agent=signalhire_agent.cli.main:main",
            "signalhire=signalhire_agent.cli.main:main",  # Short alias
        ],
    },
    
    # Classification
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Typing :: Typed",
    ],
    
    # Keywords for discovery
    keywords=[
        "signalhire", "lead-generation", "automation", "sales", "prospecting",
        "contacts", "crm", "b2b", "sales-automation", "lead-qualification"
    ],
    
    # Project URLs
    project_urls={
        "Homepage": "https://github.com/signalhire/signalhire-agent",
        "Documentation": "https://signalhire-agent.readthedocs.io/",
        "Repository": "https://github.com/signalhire/signalhire-agent.git",
        "Bug Tracker": "https://github.com/signalhire/signalhire-agent/issues",
        "Changelog": "https://github.com/signalhire/signalhire-agent/blob/main/CHANGELOG.md",
    },
    
    # Package metadata
    license="MIT",
    platforms=["any"],
    zip_safe=False,
)

# Post-installation checks and messages
def post_install():
    """Run post-installation checks and display helpful information."""
    print("\n" + "="*60)
    print("🎉 SignalHire Agent installed successfully!")
    print("="*60)
    print()
    print("📋 Next steps:")
    print("  1. Set up your SignalHire credentials:")
    print("     export SIGNALHIRE_EMAIL='your@email.com'")
    print("     export SIGNALHIRE_PASSWORD='your-password'")
    print()
    print("  2. Test the installation:")
    print("     signalhire-agent --help")
    print("     signalhire-agent doctor  # Run system diagnostics")
    print()
    print("  3. Run your first search:")
    print("     signalhire-agent search --title 'Software Engineer' --location 'New York'")
    print()
    print("📚 Documentation: https://signalhire-agent.readthedocs.io/")
    print("🐛 Issues: https://github.com/signalhire/signalhire-agent/issues")
    print()

if __name__ == "__main__":
    # This is run when the script is executed directly
    import subprocess
    
    print("Installing SignalHire Agent...")
    result = subprocess.run([sys.executable, "setup.py", "install"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        post_install()
    else:
        print(f"Installation failed: {result.stderr}")
        sys.exit(1)
