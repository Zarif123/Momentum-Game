import cx_Freeze, os

os.environ['TCL_LIBRARY'] = r"C:\Program Files (x86)\Python36-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files (x86)\Python36-32\tcl\tk8.6"

executables = [cx_Freeze.Executable("Momentum_A.py")]

cx_Freeze.setup(
    name="Momentum A",
    options={"build_exe": {"packages":["pygame","sys","math","pygame_textinput"]}},

    executables = executables,
    version="1.0.0"

    )
