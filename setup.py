from setuptools import setup, find_packages

setup(
    name="cirtusai-sdk",
    version="0.1.0",
    description="CirtusAI Python SDK for agent and wallet management",
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
