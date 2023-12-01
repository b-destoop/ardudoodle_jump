# ardudoodle_jump
Doodle jump with haptic feedback controller

# arduino code
todo:
- implement mass-spring-dampener system (last lab)
- send position of mass to computer
- read wind from computer
- implement wind as constant force in one direction on hapkit

# pygame code
- read mass position from serial
- write wind to serial
- generate obstacles
- render obstacles
- render main character
- make main character jump

# windows funky shizzle (linux 4ever tho)

## venv
to activate the virtual environment for python in Windows:
- run `Set-ExecutionPolicy Unrestricted -Scope Process` to be able to activate the virtual environment 
(https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows)
- activate the virtual environment by running `./Scripts/activate`
- install all the requirements by running `pip install -r .\requirements.txt`