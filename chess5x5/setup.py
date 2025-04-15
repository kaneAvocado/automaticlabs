from setuptools import setup, find_packages

setup(
    name="chess5x5",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.2",
        "numpy>=1.26.4",
        "pytest>=8.0.2",
        "python-dotenv>=1.0.1",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Система для проведения турнира по шахматам на доске 5x5",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chess5x5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
