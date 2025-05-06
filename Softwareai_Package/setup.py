from setuptools import setup, find_packages

# Lê os requisitos
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# Lê o Readme
with open("Readme.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="softwareai_engine_library",
    version="1.0.23",
    description="O motor da biblioteca é liberado através do pip para a sincronia do motor em múltiplos agentes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ualerson",
    author_email="mediacutsstudio@gmail.com",
    url="https://github.com/SoftwareAI-Company/SoftwareAI",
    license="Apache-2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
