from setuptools import setup, find_packages

setup(
    name="egypt-real-estate-dashboard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.24.0",
        "pandas==1.5.3",
        "numpy==1.24.3",
        "matplotlib==3.7.1",
        "seaborn==0.12.2"
    ],
    python_requires=">=3.10",
)