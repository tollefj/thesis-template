# Required Images

Add three images before building:

1. **`part1-placeholder.jpg`** (1200×800px) - Part 1 divider page
2. **`part2-placeholder.jpg`** (1200×800px) - Part 2 divider page
3. **`signature.jpg`** (800×200px) - Signature for preface

## Quick Create (ImageMagick)

```bash
convert -size 1200x800 xc:lightblue part1-placeholder.jpg
convert -size 1200x800 xc:lightgray part2-placeholder.jpg
convert -size 800x200 xc:white signature.jpg
```

## Quick Create (Python)

```python
from PIL import Image
Image.new('RGB', (1200, 800), 'lightblue').save('part1-placeholder.jpg')
Image.new('RGB', (1200, 800), 'lightgray').save('part2-placeholder.jpg')
Image.new('RGB', (800, 200), 'white').save('signature.jpg')
```

## Additional Images

Add your figures here and reference:

```markdown
![Caption](images/myfigure.pdf){width=70%}
```
