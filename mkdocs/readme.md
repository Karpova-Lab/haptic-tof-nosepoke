

## Submodule setup
Add this repository as a submodule by going to the top level of you project of your project and running the following from the command line:

```
git submodule add https://github.com/alustig3/mkdocs.git mkdocs
```

```
git submodule init
```

```
git submodule update
```


## Python libraries installation
install [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#getting-started) if you don't have it yet

create a python virtual environment for your project

```
uv venv
```

activate the virtual environment
```
# On macOS and Linux.
source .venv/bin/activate

# On Windows.
.venv\Scripts\activate
```


install the python libraries by running 

`uv pip install -r mkdocs/mkdocs_requirements.txt`
