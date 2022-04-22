![githubtitle](https://user-images.githubusercontent.com/61150608/164681591-5dac7223-fb4e-4342-ae0d-3e1bd81bfd41.png)
A small application to detail jump elements by using a prototype vmf. This is build using [PyVMF](https://github.com/GorangeNinja/PyVMF) by GorangeNinja.

## Downloads
Latest Release:
[Element Detailer](https://github.com/Gerb-24/Element-Detailer/releases/latest)

## Usage
![progress_shot2](https://user-images.githubusercontent.com/61150608/164649282-32b6be87-004f-445e-8e22-ed0132935f0e.png)
The Application consists of four parts:
1. In the top part you can open the .vmf file you want to be detailed
2. The second part is a form, where you can open the detailing prototype, select if this meant to be on the side or on top, and what texture it has to look out for. **Note that:** the buttons "jurf", "ramp" and "Create New Prototype" currently dont do anything. Texture variables will be explained in a section below.
3. In the third part you can view the settings that you added to the queue and you are able to remove them. To be able to load the settings automatically when restarting the application, you can save the settings with the "Save Settings" button.
4. The fourth part is the compile button. This will create a new vmf file in the same folder as your selected vmf is located. This file will be called (your_selected_vmf)_detailed.vmf. **Note that:** Currently the code looks for an enitity made out of solids in the prototype vmf. So these should be a func_detail/func_illusionary etc.

#### Texture Variables
In part 2 we saw the "Load Texture Variables" button. With this we can open a texture variables file, which lets you write a short name to use instead of the longer actual texture name. To get a texture variable file, and to get the associated application to change them, see [Texture Variables](https://github.com/Gerb-24/Texture-Variables)


## Licenses
The GUI part of this project, i.e. gui.py, filemanagement.py etc use the GPLv3 License as they use PyQt6
The actual python code, i.e. main.py etc use the MIT License as they use PyVMF
