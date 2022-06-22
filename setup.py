from setuptools import setup, find_packages

setup(name="custom-NER",
      version="0.1.0",
      description="Recipe Ingredient Parser",
      author="Vishwa Pardeshi",
      packages=find_packages("src"),
      package_dir={"": "src"},
      author_email="pardeshi.vishwa25@gmail.com",
      install_requires=["jupyter==1.0.0",
                        "numpy==1.22.0",
                        "pandas",
                        "bs4",
                        "requests==2.24.0",
                        "requests",
                        "spacy",
                        "pytest==5.2.2",
                        "pytest-mpl==0.10",
                        "pytest-mock==1.11.2"
                        ],
      )
