from setuptools import setup

setup(
    name="trails_cli",
    version="0.1.0",
    py_modules=["trails_app"],
    install_requires=[
        "click",
        "flask",
        "flask-sqlalchemy",
        "hydra",
        "omegaconf",
    ],
    entry_points={
        "console_scripts": [
            "trails = trails_app.trails_cli:main",
        ],
    },
)
