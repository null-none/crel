# crel

## Overview
fast, templateless html generation

### Install

```bash
pip install crel
```


### Example

```python

from crel import div, h1, render, p

node = div({}, 
            h1({"id": "hello"}, "Hello World!"), 
            p({}, "hooray!")
        )

print(render(node))

```


