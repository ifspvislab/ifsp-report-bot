# IFSP Report Bot

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


# Dev tasks

## black
Black is a Python code formatter for consistent and readable code.

Check the problems:

```bash
python -m black --check src
```


A line-by-line comparison of the proposed formatting changes without actually applying them.
```bash
python -m black --diff src
```

Formats Python code in the "src" directory using Black.
```bash
python -m black src
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