# Re-implement the AinQ Scheme
In this work, I try to implement the AinQ scheme, a certificateless group key distribution protocol.
In addition, I replicate the experiment results which are shown in the academic paper
_**Arrows in a Quiver: A Secure Certificateless Group Key Distribution Protocol for Drones**_
, publicly available at [this link](https://eprint.iacr.org/2021/1372.pdf)

## How to run the protocol
After you cloned the repository, please run the following commands
```
cd python
python driver.py -e <number_of_existing_edge_drones> -n <number_of_new_drones> [-v]
```

For example, you want to run the protocol with 10 initial edge drones and then 100 new
drones will join the existing group. The script runs in a silent mode without the flag `-v`
```
python driver.py -e 10 -n 100
```

Run the below command for more detail argument description.
```
$ python driver.py -h
usage: driver.py [-h] -e EXISTING_DRONE -n NEW_DRONE [-v]

optional arguments:
  -h, --help            show this help message and exit
  -e EXISTING_DRONE, --existing-drone EXISTING_DRONE
                        Number of existing edge drones
  -n NEW_DRONE, --new-drone NEW_DRONE
                        Number of new drones
  -v, --verbose         Verbose mode of the script
```

## Report of experiment results
To build the full PDF report, please run the following commands
```
cd report
make
```

Try to install required packages if any messages about missing packages would be raised.

## Live demo of the protocol