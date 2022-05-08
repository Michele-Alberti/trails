# Trails

A simple app for designing mountain trails!

## Development environment setup

The following steps will guide you through the installation procedure.

### Miniconda

[<img style="position: relative; bottom: 3px;" src="https://docs.conda.io/en/latest/_images/conda_logo.svg" alt="Conda" width="80"/>](https://docs.conda.io/en/latest/) is required for creating the development environment (it is suggested to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)).

From terminal navigate to the repository base directory.\
Use the following command in your terminal to create an environment named `trails-app`.

```
conda env create -f environment.yml
```

Activate the new _Conda_ environment with the following command.

```
conda activate trails-app
```

### Install trails CLI

The CLI distributed with setuptools instead of using Unix shebangs.  
It is a very simple utility to initialize and delete an _sqlite_ debug database: use it local tests.

Use the following command for generating the CLI executable from the `setup.py` file, it will install your package locally.

```
pip install .
```

If you want to make some changes to the source code it is suggested to use the following option.

```
pip install --editable .
```

It will just link the package to the original location, basically meaning any changes to the original package would reflect directly in your environment.

Now you can activate the _Conda_ environment and access the _CLI_ commands directly from the terminal (without using annoying _shebangs_ or prepending `python` to run your _CLI_ calls).

Test that everything is working fine with the following commands.

```
trails --version
trails --help
```

## Additional installations before contributing

Before contributing please create the `pre-commit` and `commitizen` environments.

```
cd requirements
conda env create -f pre-commit.yml
conda env create -f commitizen.yml
```

### Pre-commit hooks

Then install the precommit hooks.

```
conda activate pre-commit
pre-commit install
pre-commit autoupdate
```

Optionally run hooks an all files.

```
pre-commit run --all-files
```

### Commitizen

The _Commitizen_ hook checks that rules for _conventional commits_ are respected in commits messages.
Use the following command to enjoy _Commitizen's_ interactive prompt.

```
conda activate commitizen
cz commit
```

`cz c` is a shorther alias for `cz commit`.

### Merge strategy to main branch

In order to take advantage of _Commitizen_ `bump` command follow this guideline.
**TO DO**
