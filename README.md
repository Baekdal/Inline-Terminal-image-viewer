# terminal-display

A Python function that renders images directly in the terminal — no popup windows, no temp files.

Supports two methods:

- **Sixel** — true pixel rendering, works in WezTerm, Windows Terminal, and most modern terminal emulators
- **Half-block** — uses Unicode block characters and ANSI color codes, works in any terminal with color support

## Requirements

```
pip install Pillow numpy
```

## Usage

```python
# from a file path
display("image.jpg")

# from a PIL Image object
img = Image.open("image.jpg")
display(img)

# options
display("image.jpg", pixel_width=800)             # larger output
display("image.jpg", method="halfblock")          # use half-block instead of sixel
display("image.jpg", method="halfblock", term_width=120)  # set character width
```

### Inline matplotlib graphs

```python
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
# ... build your plot ...

buf = BytesIO()
fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
buf.seek(0)
display(Image.open(buf), pixel_width=int(fig.get_figwidth() * fig.get_dpi()))
plt.close()
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `img` | required | File path (str) or PIL Image object |
| `pixel_width` | 400 | Output width in pixels (sixel only) |
| `method` | `"sixel"` | `"sixel"` or `"halfblock"` |
| `term_width` | 80 | Output width in characters (halfblock only) |

## Terminal support

| Terminal | Sixel | Half-block |
|----------|-------|------------|
| Windows Terminal | ✓ | ✓ |
| WezTerm | ✓ | ✓ |
| iTerm2 (macOS) | ✓ | ✓ |
| Any terminal | — | ✓ |

## Notes

- Sixel quantizes the image to 256 colors using median cut
- Rendering speed scales with `pixel_width` and CPU speed
- When passing a PIL Image, it does not need to be RGB — conversion is handled internally
