from setuptools import setup, find_packages

setup(
    name="agent-ai-personal-financial-advisor",
    version="1.0.0",
    description="Agentic AI Financial Advice Application",
    author="AgenticAI Class",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.28.0",
        "google-generativeai>=0.3.0",
        "mysql-connector-python>=8.2.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.1.0",
        "plotly>=5.17.0",
        "typing-extensions>=4.8.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
