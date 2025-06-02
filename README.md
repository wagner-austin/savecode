# Python Code Saver

Python Code Saver is a command-line utility that gathers Python code from specified directories and individual files, then consolidates them into one output file. This tool is especially useful for creating a single aggregated file from multiple Python scripts for documentation, analysis, or archiving purposes.

---

## Features

- **Recursive File Gathering:** Scans directories recursively for all `.py` files.
- **Customizable Directory Skipping:** Easily exclude specific subdirectories (default: `node_modules`, `dist`, `build`, `.git`).
- **Git Integration:** Collect only files tracked by Git with options for staged or unstaged changes.
- **File Filtering:** Automatically skips the script itself to avoid self-inclusion.
- **Flexible Input Options:** Combine files from multiple root directories and individual file paths.
- **Multiple File Types:** Support for various file extensions beyond Python (e.g., js, toml, html, css).
- **Output Customization:** Specify the output file location (defaults to `temp.txt` in the script's directory).
- **Progress Indicator:** Shows a progress bar during file processing for better visibility.
- **Enhanced Output Display:** After saving, the tool prints a colored list of all the files that were processed.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/python-code-saver.git
   cd python-code-saver

2. Ensure Python 3 is Installed:

Verify that you have Python 3 installed on your system:

python3 --version

If not, download and install it from python.org.




---

Usage

Run the script from the command line using Python. Below are the available options:

python cli.py [OPTIONS]

### Options

**-r or --roots**

Specify one or more root directories to search for files.

```bash
python -m savecode -r ./src ./lib
```

**-f or --files**

Provide one or more individual file paths to include.

```bash
python -m savecode -f script1.py script2.py
```

**-o or --output**

Define the output file path. If not provided, defaults to temp.txt in the current directory.

```bash
python -m savecode -o combined_output.txt
```

**--skip**

List subdirectory names to skip during the search (default: `node_modules`, `dist`, `build`, `.git`).

```bash
python -m savecode --skip tests docs
```

**--ext or --extensions**

Specify file extensions to collect (without leading period). If not provided, defaults to 'py'.

```bash
python -m savecode --ext py js html css
```

**--git**

Collect files listed by Git status instead of walking the filesystem.

```bash
python -m savecode --git
```

**--staged**

With --git: only include staged changes.

```bash
python -m savecode --git --staged
```

**--unstaged**

With --git: only include unstaged changes.

```bash
python -m savecode --git --unstaged
```


### Example Commands

**Basic Usage:**

Combine files from the current directory with specific extensions:

```bash
python -m savecode --ext py js html css
```

**Multiple Directories:**

Combine files from multiple directories, exclude certain subdirectories, and specify an output file:

```bash
python -m savecode -r ./project/src ./project/utils -o all_code.txt --skip __pycache__ migrations
```

**Git Integration:**

Collect only files tracked by Git with changes (staged or unstaged):

```bash
python -m savecode --git
```

Collect only files with staged changes in Git:

```bash
python -m savecode --git --staged
```

**Using the Makefile:**

The included Makefile provides convenient shortcuts:

```bash
# Run on current directory with default extensions
make run

# Run with Git integration
make git

# Run with custom arguments
make run ARGS="--ext js html css"
```


---

How It Works

1. File Discovery: The script recursively walks through the provided root directories, collecting paths of all .py files while ignoring directories specified by the --skip option and excluding itself (cli.py).


2. File Aggregation: Each discovered Python file is opened, and its content is read and written into the output file. A header indicating the file path is inserted before each file's content to provide clear separation.


3. Output Confirmation: Once the aggregation is complete, the script prints a summary that includes the number of files processed and a list of file paths, with colored formatting for improved readability.




---

Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

1. Fork the repository.


2. Create your feature branch: git checkout -b feature/my-new-feature


3. Commit your changes: git commit -am 'Add some feature'


4. Push to the branch: git push origin feature/my-new-feature


5. Open a pull request.




---

License

Open Source


---

Acknowledgments

Inspired by the need for a simple yet effective tool to consolidate Python code for documentation and analysis.


---

Happy coding!