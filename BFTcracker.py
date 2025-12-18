import subprocess
import re
import sys

if len(sys.argv) != 2:
    print('Argument missing. Use:')
    print('    python BFTcracker.py [filename.json]')
    exit(1)

json_file = sys.argv[1]
with open(json_file, 'r') as file:
    content = file.read()

fixed_content = re.sub('(?<=\\[)(0x[0-9A-Fa-f]+(?:,0x[0-9A-Fa-f]+)*)(?=\\])', lambda m: ','.join((f'"{x}"' for x in m.group(0).split(','))), content)
data = eval(fixed_content)

for key, values in data.items():
    inputs = ','.join(values[0:3])
    command = f'docker run -it  --init --gpus=all cudakeeloq:local --mode=5 --learning-type=4 --start 0x4C6D4D7A55644F76 --inputs {inputs}'
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)

        seed_input = input("\nWrite the founded seed (or Enter to exit): ").strip()
        if seed_input:
            try:
                if seed_input.startswith('0x'):
                    seed = int(seed_input, 16)
                else:
                    seed = int(seed_input)
                print(f"Hexadecimal Seed: 0x{seed:08X}")
            except ValueError:
                print("Not a valid seed")

    except subprocess.CalledProcessError as e:
        print('Command failed')