from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cirtusai-sdk",
    version="0.1.1",
    description="A Python SDK for the CirtusAI backend: agent, wallet, and credential management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CirtusAI Team",
    packages=find_packages(include=["cirtusai", "cirtusai.*"]),
    install_requires=[
        "requests>=2.0.0",
        "httpx>=0.24.0",
        "click>=8.0.0"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'cirtusai=cirtusai.cli:main'
        ]
    },
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.20.0',
            'responses>=0.10.0',
            'respx>=0.20.0'
        ]
    },
)
