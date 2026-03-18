from cx_Freeze import setup, Executable

def get_requirements():
    with open("requirements.txt") as f:
        # Filter out comments and empty lines
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

executables = [
    Executable("main.py", target_name="frlg_switch_seed_farmer"),
    Executable("process_seeds.py", target_name="frlg_switch_seed_processor"),
]

setup(
    name="FRLG Switch Seed Farmer",
    version="1.0",
    description="",
    executables=executables,
    options={"build_exe": {"packages": ["usb"], "build_exe": "dist", "include_files": ["config.json"]}},
)
