We want to package and distribute my  Python project (`codescribe`) for installation with `pipx`. Please follow the following instruytions:


## Step-by-step Guide
###  **Move CLI entry point into a proper module/package (recommended)**

Python best practice is to wrap it in a package, so instead of having `codescribe-agent.py` in the root, structure it like this:

```
codescribe/
├── codescribe/
│   ├── __init__.py
│   ├── __main__.py    ← contains `main()` entry point
│   └── agent.py  ← contains main body of 
├── pyproject.toml
├── README.md
├── LICENSE
├── uv.lock
```

main() will call the code in agent.py. Apart from the necearry imports and def main(), __main__.py will be empty


### **Update `pyproject.toml`**

Add the right dependencies to pyproject.toml (I woudl imagine setuptool, but do whatever is needed)


Ensure we're using [PEP 621](https://peps.python.org/pep-0621/) (declarative config via `[project]`). 

for example:

[project.scripts]
codescribe = "codescribe.__main__:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

