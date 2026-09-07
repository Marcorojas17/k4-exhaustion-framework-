from PIL import Image
import os
for i in range(9):
    p=f"{i}.png"
    if not os.path.exists(p):
        print(f"{p} no encontrado")
        continue
    im=Image.open(p).convert("L")
    w,h=im.size
    cells=[]
    for r in range(4):
        for c in range(4):
            x=int((c+0.5)/4*w); y=int((r+0.5)/4*h)
            cells.append(1 if im.getpixel((x,y))<128 else 0)
    print(f"{i}.png // {cells}")
    for r in range(4):
        print(cells[r*4:(r+1)*4])
    print()
