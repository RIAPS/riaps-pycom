# RIAPS Code Generation Tool

This tool (**riaps_gen**) generates skeleton code for RIAPS components of an application based on information from a user-defined RIAPS application model file (**.riaps**). The tool uses a **json** representatio of the model that can be produced from the **riaps** file using the **riaps_lang** tool. 

The component's implementation language is specified in the model file using the clauses **in C++** or **in Python** in the component definition. If no specification is provided, Python is the target language.  

>Note: Python components are written using Python 3.6, while C++ components use STL C++17.

```
Arguments:
  -m,   --model        : Full path of the model.json
  -o,   --output       : Output directory
  -w,   --overwrite    : Overwrite existing code (no sync)
```

The default output directory is a **generated** directory located with the model file folder.  Use ```-o .``` to place the files in the same directory as the model file.

Communication of messages between C++ components and also between Python and C++ components are handled using [Cap'n Proto](https://capnproto.org/).  The skeleton **.capnp** file will be made available for definition of the message structures.  Python only applications do not utilize this file, so this file can be ignore.

The code created will include code *protection markers* to allow preservation of user-provided code if the generator is executed again.  Below is an example that shows how the markers look like. User code is inserted between the **riaps:....:begin** and **riaps:....:end** markers of the appropriate code sections.

````
# riaps:keep_import:begin
from riaps.run.comp import Component
import logging
import capnp
import weathermonitor_capnp

# riaps:keep_import:end

class TempSensor(Component):

# riaps:keep_constr:begin
    def __init__(self):
        super(TempSensor, self).__init__()
# riaps:keep_constr:end

# riaps:keep_clock:begin
    def on_clock(self):
        pass
# riaps:keep_clock:end

# riaps:keep_impl:begin

# riaps:keep_impl:end
````

During application and component development, the user may determine that an additional component, port, message or actor is desired for the application.  Existing user defined code within the code protection markers of components and ports that do not change in the model file will be preserved and the new elements will be added. If a component name is changed, the old component code will remain and a new skeleton component will be created.  The user can then manually transfer any user defined code to the new component and remove the old component. If a port name changes, the previous port will be removed from the component and the new port added.  

>Note: It is highly recommended to backup your code base prior to running this tool after component development has started. If you forget, the tool created a ```<project name>_bak``` directory with the previous code which can be used to find removed code for the port.
