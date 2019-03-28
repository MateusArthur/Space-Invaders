import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win64":
    base = "Win64GUI"

executables = [
        Executable("jg.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = [],
        include_files = [],
        excludes = []
)




setup(
    name = "Space Invader",
    version = "1.0",
    description = "Batalha de naves espaciais",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
