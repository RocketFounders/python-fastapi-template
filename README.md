# FastAPI Basic Template

FastAPI basic template with PostgreSQL

## Requirements

* Python >= 3.11.4
* Poetry
* Docker

## How to install

### Install Python 3.11.4

For example using `pyenv` on MacOS

```shell
brew install pyenv
pyenv install 3.11.4
# Optional. Select 3.11.4 as global python version
pyenv global 3.11.4
# Or set local version in project directory
pyenv local 3.11.4
```

### Install Poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -

# for zsh
poetry completions zsh > ~/.zfunc/_poetry
# and add to .zshrc
fpath+=~/.zfunc
autoload -Uz compinit && compinit

# for bash
poetry completions bash >> ~/.bash_completion

# for Oh My Zsh
mkdir $ZSH_CUSTOM/plugins/poetry
poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry
# You must then add poetry to your plugins array in ~/.zshrc:
plugins(
  poetry
  ...
)
```

---

### Install dependencies

```shell
poetry init
```

### Run Application

1. Copy .env.example to .env file

```shell
cp .env.example .env
```
2. Change data in .env file
> **DATABASE_URL** – your postgreSQL DSN
>
> **SECRET_KEY** – special secret key. You can generate it with openssl:
> ```openssl rand -hex 32```
>
> **ACCESS_TOKEN_EXPIRE_DAYS** – JWT token expire timedelta. By default, set 1 day
>
> **CELERY_BROKER_DSN** - your redis DSN
>
> **CELERY_BACKEND_DSN** - your postgreSQL DSN


3. Run the application with `make`
```shell
make uvicorn_start
```

4. Run Celery worker with `make`
```shell
make start_celery
```

---

### Configure the pre-commit hooks

```shell
pre-commit install
```

### Install the migrate tool

```shell
brew install golang-migrate
```

### Migrations

```shell
make new_migration
make migrate
```
