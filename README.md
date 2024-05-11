# File Renamer

This is a small utility to rename files to help organize content in TV shows.

We assume the directory is organized as follows:

```
Show Name
  - Season x
    - ep 1
    - ep 2
    ...
  - Season y
    - ep 1
            ...

  ...
```

The episodes will be renamed in the format - 'Show Name SxxExx.extension'

## Usage instructions.

  - Clone this repository.
  - Install requirements.txt
  - Run the following to create an executable.

```
pyinstaller -F main.py
```
  - Executable is generated as './dist/main'
  - Run and select your folder.
