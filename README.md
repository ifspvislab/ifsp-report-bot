# IFSP Report Bot  VisLab

# How to run

Make sure you have python 3.11 installed:

```bash
python --version
```

Clone the project:
```bash
git clone https://github.com/ifspvislab/ifsp-report-bot.git
```

After project clone, run `pip install` to install project dependencies:

```bash
pip install -r requirements.txt
```

Before run, set the environment variable `DISCORD_BOT_TOKEN` with the value of the token available in the Discord Developer Portal.

Run the project

```bash
python src/main.py
```

# Dev tasks

## black
Black is a Python code formatter for consistent and readable code.

Check the problems:

```bash
python -m black src --check
```


A line-by-line comparison of the proposed formatting changes without actually applying them.
```bash
python -m black src --diff
```

Formats Python code in the "src" directory using Black.
```bash
python -m pylint src
```

## isort
isort a Python library and command-line tool used to sort imports in Python code.

A line-by-line comparison of the proposed formatting changes without actually applying them.
```bash
python -m isort src --diff --check-only --profile black
```

Format the Python code in the "src" directory using the black profile. This applies the import sorting and formatting changes. 
```bash
python -m isort src --profile black
```



## PyLint
PyLint is a Python Linter for consistent and readable code.

Check the problems:

```bash
python -m pylint src
```

### Messages
See messages: https://pylint.readthedocs.io/en/latest/user_guide/messages/index.html
  

Disable rules on specific parts of code:

```python
# pylint: disable-next=missing-function-docstring
def main():
    print("main function")
```


Disable rules for the entire project in `.pylintrc` file.
```
[MESSAGES CONTROL]
...

disable=raw-checker-failed,
        bad-inline-option,
        locally-disabled,
        file-ignored,
        suppressed-message,
        useless-suppression,
        deprecated-pragma,
        use-symbolic-message-instead,
        missing-function-docstring
```