# Convert PyPi packages to Yocto recipes

Queries the PyPi to get get information about a specific python packages and generate the corresponding Yocto recipes. The recipes follow the template set by the [meta-python]([https://layers.openembedded.org/layerindex/branch/master/layer/meta-python/](https://layers.openembedded.org/layerindex/branch/master/layer/meta-python/)) layer.

## Installation

```shell
git clone https://github.com/kkrizka/pypi2bb.git
pip install pypi2bb
```

## Example Usage

To generate the recipe for [Dash]([https://dash.plotly.com/](https://dash.plotly.com/)), run the following command:

```shell
pypi2bb.py dash
```

This creates the following two files: `python-dash.inc` and `python3-dash_1.14.0.bb`.

## Missing Features
- Recursively generate recipes for dependencies 
- Support non-PyPi hosted packages