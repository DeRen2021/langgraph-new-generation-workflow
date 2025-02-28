from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#') and not line.startswith('-e')]

setup(
    name="news_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    description="An automated news generation system using AI",
    author="de ren",
    author_email="dr3702@nyu.edu",
    url="https://github.com/DeRen2021/langgraph-new-generation-workflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)