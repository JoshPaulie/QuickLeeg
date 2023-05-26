from setuptools import setup

setup(
    name="QuickLeeg",
    version="1.0.0",
    author="JoshPaulie",
    description="Crude cli to quickly get champion stats for League, from 'League of Graphs' ❤️",
    py_modules=["leeg"],
    install_requires=[
        "requests",
        "thefuzz",
        "python-Levenshtein",  # speed up 'the fuzz'
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "leeg=leeg:main",
        ],
    },
)
