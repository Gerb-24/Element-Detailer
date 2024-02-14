![githubtitle](https://user-images.githubusercontent.com/61150608/164681591-5dac7223-fb4e-4342-ae0d-3e1bd81bfd41.png)
A small application to detail jump elements by using a prototype vmf. This is build using [PyVMF](https://github.com/GorangeNinja/PyVMF) by GorangeNinja.

## Downloads
Latest Release:
[Element Detailer](https://github.com/Gerb-24/Element-Detailer/releases/latest)


## Usage
![ed-example](https://github.com/Gerb-24/Element-Detailer/assets/61150608/1e700434-c882-4397-b745-4768b8dc1298)
The Application consists of two main sections: The detailing queue and the texture variables

### Detailing Queue
On the right side we can open a .ed file, which gives a queue of detailing operations. A detailing operation consists of the following parts:
1. A prototype vmf: this is the vmf that we vertex manipulate into the position of our jump element.
2. the type of element/prototype. Currently, this can be Top, Side, Corner or Bigside.
3. The texture variable/texture name. If the input does not correspond to a texture variable, then we its taken to be a texture name.
4. A button to remove the operation.

Using "save queue", you can save your detailing queue as a .ed file.
We can then detail the our chosen vmf in "Open vmf to detail" and click "Compile". This will create a new vmf file in the same folder as your selected vmf is located. This file will be called (your_selected_vmf)_detailed.vmf. **Note that:** Currently the code looks for an enitity made out of solids in the prototype vmf. So these should be a func_detail/func_illusionary etc.


### Texture Variables
When we want to share our .ed files, we would not like to have to change the dev texture names of the other mapper, to what we use for creating the alpha versions of our map. With texture variables we can give our prefered textures standardized (shorter) names, and use these in the .ed file. A texture variable consists of the following parts:
1. The variable name.
2. The texture name.

We can then save our texture variables to a .tv file. This way we can work with the dev preferences of other, by using their .tv before doing the compile.

## Licenses
The GUI part of this project, i.e. gui.py, filemanagement.py etc use the GPLv3 License as they use PyQt6
The actual python code, i.e. main.py etc use the MIT License as they use PyVMF
