# Trails <!-- omit in toc -->

A web app for easily organizing your mountain adventures.

## 1. Table of contents

- [1. Table of contents](#1-table-of-contents)
- [2. Development environment setup](#2-development-environment-setup)
  - [2.1. Miniconda](#21-miniconda)
  - [2.2. Install trails CLI](#22-install-trails-cli)
  - [2.3. Developing with a dockerized Postgresql database](#23-developing-with-a-dockerized-postgresql-database)
- [3. Additional installations before contributing](#3-additional-installations-before-contributing)
  - [3.1. Pre-commit hooks](#31-pre-commit-hooks)
  - [3.2. Commitizen](#32-commitizen)
- [4. Release strategy from `development` to `main` branch](#4-release-strategy-from-development-to-main-branch)

## 2. Development environment setup

The following steps will guide you through the installation procedure.

### 2.1. Miniconda

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

### 2.2. Install trails CLI

The CLI is distributed with setuptools instead of using Unix shebangs.  
It is a very simple utility to initialize and delete the app database. There are different use cases:

- Create/delete an _sqlite_ database for local debug
- Initialize/drop tables inside a contanerized _Postgresql_ database
- Initialize/drop tables Heroku's _Postgresql_ add-on

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

Test that everything is working correctly with the following commands.

```
trails --version
trails --help
```

> **Note:**  
> To create the _sqlite_ database and run the app locally, use the flag `--sqlite-test-db` when calling db commands.  
> In addition an environment variable named `FLASK_TEST_DB`shall exist for _Flask_ to work correctly with _sqlite_.
>
> Create the local _sqlite_ database with:
>
> ```
> export FLASK_TEST_DB=true && trails --sqlite-test-db db init
> ```
>
> And then launch the app:
>
> ```
> python -m trails_app flask=sqlite server=sqlite
> ```
>
> Delete the local _sqlite_ database with:
>
> ```
> export FLASK_TEST_DB=true && trails --sqlite-test-db db delete && unset FLASK_TEST_DB
> ```

### 2.3. Developing with a dockerized Postgresql database

Since this app is hosted on _Heroku_ (by using a _Docker_ container) the _Postgresql Addon_ is used.  
After an initial development phase supported by an _sqlite_ database, I moved to a dockerized _Postgresql_ database.

Look inside the `makefile` to see the configuration options I selected for this scope.

To run a container with a _Postgresql_ database for your development environment, you have to install [Docker](https://docs.docker.com/get-docker/) and download the official _Postgresql_ image.

My suggestion is to build the two images from the `docker-compose.yaml` and then run only the database instance to have a containerized _Postgresql_ database accessible from your local environment.

First build the two images, one for each container:

- `web` for the app
- `db` for the postgresql database

From the project directory call the following `make` commands.

```
make up-build
```

The two images are built and the two containers are started.  
Since you need only the database for development pourposes you can turn them down.

```
make down
```

Then start the only the database container.

```
make run-db
```

Do not forget to initialize the database or the app will complain because tables are not there.

```
trails db init
```

This set up (with only the database running inside a container) will allow you to see changes on _html_ and _Python_ files without rebuilding _Docker_ images.  
All you have to do is start the web server locally with _Python_.

```
python -m trails_app
```

The app will be available at `localhost:5000`.

> **Note:**  
> You can also use `make up` to access the app from the container system build by _Docker compose_. However, in this case you have to rebuild the images (with `make up-build`) every time you edit the codebase to see changes in place.

## 3. Additional installations before contributing

Before contributing please create the `pre-commit` and `commitizen` environments.

```
cd requirements
conda env create -f pre-commit.yml
conda env create -f commitizen.yml
```

### 3.1. Pre-commit hooks

Then install the precommit hooks.

```
conda activate pre-commit
pre-commit install
pre-commit autoupdate
```

Optionally run hooks on all files.

```
pre-commit run --all-files
```

### 3.2. Commitizen

The _Commitizen_ hook checks that rules for _conventional commits_ are respected in commits messages.
Use the following command to enjoy _Commitizen's_ interactive prompt.

```
conda activate commitizen
cz commit
```

`cz c` is a shorther alias for `cz commit`.

## 4. Release strategy from `development` to `main` branch

In order to take advantage of _Commitizen_ `bump` command follow this guideline.

First check that you are on the correct branch.

```
git checkout main
```

Then start the merge process forcing it to stop before commit (`--no-commit`) and without using the _fast forward_ strategy (`--no-ff`).

```
git merge development --no-commit --no-ff
```

Check that results match your expectations then commit (you can leave the default message).

```
git commit
```

Now _Commitizen_ `bump` command will add an additional commit with updated versions to every file listed inside `pyproject.toml`.

```
cz bump --no-verify
```

You can now merge results of the release process back to the `development` branch.

```
git checkout development
git merge main --no-ff
```

Use _"update files from last release"_ as commit message.
