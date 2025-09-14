from pathlib import Path
import setuptools
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")
setuptools.setup(
    name="streamlit-japanese-date-input",
    version="0.1.0",
    author="Ayumu Yamaguchi",
    author_email="",
    description="Streamlit component for date input with Japanese localization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gussan-me/streamlit_japanese_date_input",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.28.0",
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.48.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    }
)