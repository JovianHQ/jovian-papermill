# jovian-papermill

`jovian-papermill` is an I/O Handler for [papermill](https://github.com/nteract/papermill). 

## Installation

```bash
pip install jovian-papermill
```

## How it works
Once installed, a `jvn://` URL must be supplied to papermill as input/output path.

This is the format of a Jovian URL, or we could call it - Jovian Gist Locator (JGL)

```jvn:///{gist_slug}?gist_version={version}```

Papermill recognizes the protocol to be `jvn://` and delegates the I/O Handler to `jovian-papermill`.

**Note**: Input and output JGL must point to same gist for normal usage. 

## Usage

### via CLI
```bash
papermill -p city 'Mumbai' \                                # parameters
                  jvn:///cebe687752e844649cdf1e4cfba34c6d \ # input gist
                  jvn:///cebe687752e844649cdf1e4cfba34c6d \ # output gist
                  --no-request-save-on-cell-execute         # save after execution terminates
 ```
 
### via `jovian-papermill` Python API
```python
import papermill
from jovian_papermill import execute

execute("cebe687752e844649cdf1e4cfba34c6d", dict(city="Mumbai"))
```
