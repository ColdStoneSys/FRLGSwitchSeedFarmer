from cx_Freeze import setup, Executable

IMPORT_MAP = {
        "pyusb": "usb"
}

def get_requirements():
    frozen_packages = []

    with open("requirements.txt") as f:
        # Filter out comments and empty lines
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            module_name = IMPORT_MAP.get(line, line)
            frozen_packages.append(module_name)

        return frozen_packages

executables = [
    Executable("main.py", target_name="frlg_switch_seed_farmer"),
    Executable("process_seeds.py", target_name="frlg_switch_seed_processor"),
]

setup(
    name="FRLG Switch Seed Farmer",
    version="1.0",
    description="",
    executables=executables,
    options={"build_exe": {"packages": get_requirements(), "build_exe": "dist", "include_files": ["config.json"]}},
)
