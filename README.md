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
  -demography DEMOGRAPHY
                        yaml file with demography (default: None)
  -samples SAMPLES      json file with samples (default: None)
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
iteration	haplotype	pop	        start	    end	    length	admix_event	            admixtime	  snps	shared
0	        0	        NonAfrican	777814	  785510	7696	  Distant_DEN>NonAfrican	1551.7	    3	    3
0	        0	        NonAfrican	790841	  879408	88567	  Distant_DEN>NonAfrican	1551.7	    21	  12
0	        0	        NonAfrican	896724	  914466	17742	  Distant_DEN>NonAfrican	1551.7	    3	    0
0	        0	        NonAfrican	1178743	  1294745	116002	Close_DEN>NonAfrican	  1517.2	    8	    5
0	        0	        NonAfrican	1382003	  1409748	27745	  Close_DEN>NonAfrican	  1517.2	    3	    2
0	        0	        NonAfrican	2916905	  2945237	28332	  Distant_DEN>NonAfrican	1551.7	    4  	  3
0	        0	        NonAfrican	4145150	  4184740	39590	  Distant_DEN>NonAfrican	1551.7	    4	    0
0	        0	        NonAfrican	4405672	  4462512	56840	  Close_DEN>NonAfrican	  1517.2	    11	  4
0	        0	        NonAfrican	5281450	  5373417	91967	  Distant_DEN>NonAfrican	1551.7	    32	  14
0	        0	        NonAfrican	5485190	  5570239	85049	  Distant_DEN>NonAfrican	1551.7	    12	  8
0	        0	        NonAfrican	5570239	  5589862	19623	  Close_DEN>NonAfrican	  1517.2	    4	    3

```
Note please feel free to play around with the parameters in the yaml file and use this for your own simulations.
