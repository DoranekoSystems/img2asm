# img2asm

Generate assembly code from image.  
Inspired by REpsych.

# Usage

Install python library.

```
pip install toml
pip install opencv-python
```

Generate assembly code.

```
python img2asm.py cat.png
```

Then `Native.asm` is generated.

1. The Native.asm file can be built by incorporating it into a `Visual Studio, x64` project.
1. Project RightClick->Build Dependencies->Build Customizations->`masm`
1. Project RightClick->Properties->Linker->System->Enable Large Addresses->`No (/LARGEADDRESSAWARE:NO)`
1. Native.asm RightClick->Properties->Item Type->`Microsoft Macro Assembler`
1. Build  
   Have fun!!

<img width="405" alt="img" src="https://user-images.githubusercontent.com/96031346/184444755-0aeccf3d-9b6f-4234-ae45-1f17ab73f677.png">
The graph view in ida is shown above.
