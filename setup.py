from setuptools import setup, find_packages

setup(
      name="docs2md",
      version="1.0.0",
      description="Convert documentation sites to markdown using Claude AI + Jina Reader",
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=[
                "anthropic>=0.52.0",
                "requests>=2.31.0",
                "click>=8.1.0",
                "rich>=13.0.0",
      ],
      entry_points={
                "console_scripts": [
                              "docs2md=docs2md.cli:main",
                ],
      },
      python_requires=">=3.10",
)
