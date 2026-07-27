# Find_introgressed_segments
Find introgressed segments from an msprime simulation. Here are two examples you can run:

```note
usage: Keeptrack_of_introgressed.py [-h] -demography DEMOGRAPHY -samples
                                    SAMPLES [-outfile] [-printdemography]
                                    [-seed] [-iterations] [-genomesize]
                                    [-mutation_rate] [-recombination_rate]
                                    [-extrainfo] [-keepevents]

optional arguments:
  -h, --help            show this help message and exit
  -demography           yaml file with demography (default: None) < REQUIRED
  -samples              json file with samples (default: None)    < REQUIRED
  -outfile              outplot name (default: /dev/stdout)
  -printdemography      print demography and save to pdf (default: )
  -seed                 set seed (default: 1234)
  -iterations           number of independent iterations (default: 1)
  -genomesize           size of genome (default: 10000000)
  -mutation_rate        genome wide mutation rate (default: 1.45e-08)
  -recombination_rate   genomewide recombination rate (default: 1.45e-08)
  -extrainfo            print snp positions and ages (default: False)
  -keepevents           filter events containing this word (or more words
                        comma separated like Nea,Den) (default: )
```



```note
# try this
python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml

# or this 
python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -keepevents=Den,Nea
```

The program needs two files to run. A Demography file in yaml format and a list of samples in json format. 
The list of samples needs to be in 3 types of classes: Ingroup, Sequenced_Archaics and Outgroup:

```json
{
	"Ingroup":
		[{"num_samples":1, "population": "Ingroup", "time": 0, "ploidy": 2}],
	"Sequenced_Archaics":
		[{"num_samples":1, "population": "Seq_DEN", "time": 0, "ploidy": 2}],
	"Outgroup":
		[{"num_samples":1, "population": "Outgroup", "time": 0, "ploidy": 2}]
}
```

Below is an example output from the first scenario:

```note
iteration  haplotype  pop      start    end       length  admix_event          admixtime  snps  Seq_DEN
0          0          Ingroup  126443   158290    31847   Distant_DEN>Ingroup  1551.7     7     5
0          0          Ingroup  206139   223580    17441   Distant_DEN>Ingroup  1551.7     8     4
0          0          Ingroup  1006542  1007305   763     Distant_DEN>Ingroup  1551.7     0     0
0          0          Ingroup  1180240  1290919   110679  Distant_DEN>Ingroup  1551.7     27    13
0          0          Ingroup  1342407  1344305   1898    Distant_DEN>Ingroup  1551.7     2     0
0          0          Ingroup  1458530  1459883   1353    Distant_DEN>Ingroup  1551.7     0     0
0          0          Ingroup  1823533  1897035   73502   Distant_DEN>Ingroup  1551.7     23    16
0          0          Ingroup  2100370  2230879   130509  Close_DEN>Ingroup    1517.2     31    24
0          0          Ingroup  2533876  2713571   179695  Distant_DEN>Ingroup  1551.7     51    29
0          0          Ingroup  2744458  2797000   52542   Distant_DEN>Ingroup  1551.7     14    11
0          0          Ingroup  3378226  3392709   14483   Distant_DEN>Ingroup  1551.7     6     2
0          0          Ingroup  3420729  3556243   135514  Distant_DEN>Ingroup  1551.7     35    16
0          0          Ingroup  3568935  3688536   119601  Distant_DEN>Ingroup  1551.7     39    21
0          0          Ingroup  3719236  3752493   33257   Distant_DEN>Ingroup  1551.7     10    4
0          0          Ingroup  4002786  4017326   14540   Distant_DEN>Ingroup  1551.7     5     2
0          0          Ingroup  4120728  4289263   168535  Distant_DEN>Ingroup  1551.7     47    22
```
Note please feel free to play around with the parameters in the yaml file and use this for your own simulations.
