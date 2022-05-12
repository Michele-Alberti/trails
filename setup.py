from setuptools import setup

setup(
    name="trails_cli",
    version="0.2.1",
    py_modules=["trails_app"],
    install_requires=[
        "flask==2.0.3",
        "flask-wtf==0.15.1",
        "flask-login==0.5.0",
        "flask-sqlalchemy==2.5.1",
        "hydra-core==1.1.1",
        "omegaconf",
    ],
    entry_points={
        "console_scripts": [
            "trails = trails_app.trails_cli:main",
        ],
    },
)
