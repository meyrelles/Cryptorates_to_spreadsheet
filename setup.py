from cx_Freeze import setup, Executable

base = None


executables = [Executable("cryptorates.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "cryptorates",
    options = options,
    version = "0.1.0",
    description = 'Download cryptocurrency rates',
    executables = executables
)
