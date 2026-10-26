# Snake

Multiple snakes enter from the canvas edges, carry the input characters through orthogonal paths, and deposit them into the final text.

## Quick Start

```python
from effect_snake import Snake

effect = Snake("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```
