# jovian-papermill

`jovian-papermill` is an I/O Handler for [papermill](https://github.com/nteract/papermill). 

## Installation

```bash
pip install git+https://github.com/JovianML/jovian-papermill.git
```

## How it works
Once installed, a `jovian://` URL must be supplied to papermill as input/output path.

Below is the format of a Jovian URL, or we could call it - Jovian Gist Locator (JGL)

```jovian:///{gist_slug}?gist_version={version}```

Papermill recognizes the protocol to be `jovian://` and delegates the I/O Handler to `jovian-papermill`.

## Usage
 
### via `jovian-papermill` Python API
```python
from jovian_papermill.execute import execute
execute("rohit/city", parameters=dict(city="Mumbai"))
```

### via CLI
```bash
papermill -p city 'Mumbai' \                         # parameters
                  jovian:///rohit/city \             # input gist
                  jovian:///rohit/city \             # output gist
                  --no-request-save-on-cell-execute  # save after execution terminates
 ```

