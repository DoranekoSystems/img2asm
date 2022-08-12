# img2asm
Generate assembly code from image.

# Usage

Install python library.

```
pip install opencv-python
```

Generate assembly code.
```
python img2asm.py cat.png
```

Then ```Native.asm``` is generated.
The asm file can be built by incorporating it into a ```Visual Studio, x64``` project.  
Optionally, ```/LARGEADDRESSAWARE:NO``` is required.  

<img width="405" alt="img" src="https://user-images.githubusercontent.com/96031346/184444755-0aeccf3d-9b6f-4234-ae45-1f17ab73f677.png">
The graph view in ida is shown above.
