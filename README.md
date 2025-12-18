# AKAI

## Cracking KeeLoq Seeds

### Instalation (linux)

To install the is necessary to have a NVIDIA graphics card

Required packages:

- [Docker](https://docs.docker.com/engine/install/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- CudaKeeLoq
- BFTcracker python script

#### CudaKeeLoq

Download:

```bash
git clone https://github.com/X-Stuff/CudaKeeloq.git
cd CudaKeeloq
git submodule update --init --recursive
```

Depending on the NVIDIA card, edit with `vim`, `nano` or similar editor the `makefile` accordingly to your graphics architecture.

In my machine I have to change the line:

```txt
NVCC_FLAGS=--gpu-architecture=compute_80 --gpu-code=sm_80 --std=c++17 
```

To:

```txt
NVCC_FLAGS=--gpu-architecture=compute_75 --gpu-code=sm_75 --std=c++17
```

Instalation:

```bash
./build.sh
```

Check everything works:

```bash
docker run --rm -it --init --gpus=all cudakeeloq:local  --help
```

Should give an output somehow similar to this:

```bash


  _______  _____  ___     __ __        __
 / ___/ / / / _ \/ _ |   / //_/__ ___ / /  ___  ___ _
/ /__/ /_/ / // / __ |  / ,< / -_) -_) /__/ _ \/ _ `/
\___/\____/____/_/ |_| /_/|_|\__/\__/____/\___/\_, /
                                                /_/
   ___           __      ___
  / _ )______ __/ /____ / _/__  ___________ ____
 / _  / __/ // / __/ -_) _/ _ \/ __/ __/ -_) __/
/____/_/  \_,_/\__/\__/_/ \___/_/  \__/\__/_/


Usage:
  CudaKeeloq [OPTION...]

  -h, --help                    Prints this help
      --inputs [k1, k1, k3]     Comma separated uint64 values (it's better to have 3)
      --cuda-blocks <num>       How many thread blocks to launch. (default: 32)
      --cuda-threads <num>      How many threads will be launched in a block (if 0 - will use value from device). (default: 0)
      --mode [m1,m2..]          Bruteforce modes (comma separated):
                                	0: - Dictionary.
                                	1: - Simple +1.
                                	2: - Simple +1 with filters.
                                	3: - Alphabet. Bruteforce +1 using only specified bytes.
                                	4: - Pattern. Bruteforce with bytes selected by specified pattern.
                                	5: - Seed. Bruteforce only seed with provided manufacturer key (applied only to algorithms with seed).
      --learning-type <type>    Specific learning type (if you know your target well). Increases approximately x16 times (since doesn't calculate other types)
                                	V+1 means with reverse key (There are also more types. see source code):
                                	0: - Simple
                                	2: - Normal
                                	4: - Secure
                                	6: - Xor
                                ALL (default: 16)
      --word-dict [f1,w1,...]   Word dictionary file(s) or word(s) - contains hexadecimal strings which will be used as keys. e.g: 0xaabb1122 FFbb9800121212
      --bin-dict [b1,b2,...]    Binary dictionary file(s) - each 8 bytes of the file will be used as key (do not check duplicates or zeros)
      --bin-dict-mode <mode>    Byte order mode for binary dictionary. 0 - as is. 1 - reverse, 2 - add both (default: 0)
      --start <value>           The first key value which will be used for selected mode(s) (default: 0)
      --seed <value>            The seed which is used for bruteforce. If you specify it, most probably you need to check seed-only learning types (SECURE, FAAC) (default: 0)
      --count <value>           How many keys selected mode(s) should check. (default: 0xFFFFFFFFFFFFFFFF)
      --alphabet [f1,a1,...]    Alphabet binary file(s) or alphabet hex string(s) (like: AA:61:62:bb)
      --pattern [f1,p1,...]     Pattern file (or pattern itself) - contains comma separated patterns like: AL1:0A:0x10-0x32:*:33|44|FA:FF
                                Pattern is in big endian. That means first byte in patter is highest byte (e.g. 01:.... equals key 0x01......)
                                Each byte in pattern separated by `:`, pattern types:
                                	AL[0-N]   - alphabet N (index in alphabet )
                                	0A        - constant. might be any byte as hex string
                                	0x10-0x32 - range. bytes from first to second (including)
                                	*         - any byte
                                	33|44|FA  - exact 3 bytes
      --exclude-filter <value>  Exclude filter: key matching this filters will not be used in bruteforce. (default: 0)
      --include-filter <value>  Include filter: only keys matching this filters will be used in bruteforce. (WARNING: may be EXTREMELY heavy to compute) (default: 0xFFFFFFFFFFFFFFFF)
      --first-match             Boolean. Stop bruteforce on first match. If inputs are 3+ probably should set to true (default: true)
      --test                    Boolean. Run application tests. You'd better use them in debug.
      --benchmark               Boolean. Run application benchmarks. You can specify learning and num loops type from command line also.


Example:
	./CudaKeeloq --inputs xxx,yy,zzz --mode=1 --start=0x9876543210 --count=1000000

	This will launch simple bruteforce (+1) attack with 1 million checks from 0x9876543210. Will be checked ALL 16 (12 if no seed specified) keeloq learning types
Example:
	./CudaKeeloq --inputs xxx,yy,zzz --mode=3 --learning-type=0 --alphabet=examples/alphabet.bin,10:20:30:AA:BB:CC:DD:EE:FF:02:33

	This will launch 2 alphabets attacks for all possible combinations for SIMPLE learning Keeloq type. First alphabet will be taken from file, second - parsed from inputs.
Example:
	./CudaKeeloq --inputs xxx,yy,zzz --mode=4 --learning-type=2 --alphabet=examples/alphabet.bin --pattern=AL0:11:AB|BC:*:00-44:AL0:AA-FF:01

	This will launch pattern attacks with NORMAL keeloq learning type.
	Pattern applied 'as is' - big endian. The highest byte (0xXX.......) will be taken from 1st alphabet.
	Next byte (0x..XX....) will be exact `0x11`.
	Next byte (0x....XX..) will be `0xAB` or `0xBC`.

Example:
	./CudaKeeloq --inputs xxx,yy,zzz --mode=5 --start=0xAABBCCDDEEFF

	This will launch seed bruteforce attack for all seed learning types. 
	Specifying '--learning-type=a,b,c' will narrow learning types to provided ones.

Not enough arguments for bruteforce  
```


#### BFTcracker

Download the [python script](./BFTcracker.py) in this repository

With the json file from AKAI in the same folder as the script, run:

```bash
python3 BFTcracker.py  carckFile-[xxxxxxxx].json
```

It will use CudaKeeLoq container to brute force the key. If it cracks the seed successfully, will print it in decimal format, you have to write or copy/paste his value to calculate his hexadecimal value.  

Example output:

```bash
Running...    
Setup:
	CUDA: Blocks:32 Threads:1024 Iterations:1
	Encrypted data size:3
	Learning type:KEELOQ_LEARNING_SECURE
	Results per batch:98304
	Decryptors per batch:32768
	Config: Type: Seed. Manufacturer key: 0x4C6D4D7A55644F76 Start Seed:0

[|][106544/131072]    0(ms)/batch Speed: 0 KKeys/s   Last key:0x4C6D4D7A55644F76 (3491160015)             
[=================================================================>--------------]81%  00:00:47   ETA:00:00:10    
Matches count: 3
Results (Input: 0xF307F8A4F480004 - Man key: 0x4C6D4D7A55644F76 - Seed: 3491189009 )

[KEELOQ_LEARNING_SECURE                  ] Btn:0x2	Serial:0x2F2 (0x12F2)	Counter:0x9A	(MATCH)

Results (Input: 0xDFBC85AB4F480004 - Man key: 0x4C6D4D7A55644F76 - Seed: 3491189009 )

[KEELOQ_LEARNING_SECURE                  ] Btn:0x2	Serial:0x2F2 (0x12F2)	Counter:0x9B	(MATCH)

Results (Input: 0xDE39D7884F480004 - Man key: 0x4C6D4D7A55644F76 - Seed: 3491189009 )

[KEELOQ_LEARNING_SECURE                  ] Btn:0x2	Serial:0x2F2 (0x12F2)	Counter:0x9C	(MATCH)





Write the founded seed (or Enter to exit): 3491189009
Hexadecimal Seed: 0xD0175111
``` 

#### AKAI

Now, with the hexadecimal value, copy/paste it inside __AKAI Garage__ configuration page, in the __Custom keys__ section, by selecting __Keyloq Seed__ (or __FAAC Seed__) as the type, and press __ADD__.  

After this, go back to __Remotes__, after a new press of the remote, the previous frames and the newly captured one will be decripted. The __remote__ can now be cloned and used.

