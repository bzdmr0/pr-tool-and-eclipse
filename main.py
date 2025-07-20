import subprocess
import os

# Paths (edit as needed)
source_file = "/home/bzdmr/eclipse-workspace/newProject1/test.c"  # Updated path
output_dir = "/home/bzdmr/eclipse-workspace/newProject1/Debug"
output_binary = os.path.join(output_dir, "test")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Compilation command
compile_cmd = ["gcc", source_file, "-o", output_binary]

try:
    # Run the compilation command
    subprocess.check_call(compile_cmd)
    print(f"Compiled '{source_file}' successfully to '{output_binary}'")
except subprocess.CalledProcessError as e:
    print(f"Compilation failed: {e}")