# Find_introgressed_segments
Find introgressed segments from an msprime simulation.

```note
python Keeptrack_of_introgressed.py -demography=Demography1.yaml 
```

First look at the Demography1.yaml. There are multiple introgression events from Neanderthals and Denisovans. This script will keep track of them.

Run the script to produce the following output of introgressed segments:

```note
haplotype  start      end        admix_event                    admixtime 
0          938695     1000000    Intro_NEA>NonAfrican           612.4     
1          335085     641415     Intro_DEN>NonAfrican           689.7     
1          654131     666516     Intro_NEA>NonAfrican           1551.7    
1          779643     789331     Intro_DEN>NonAfrican           689.7     
2          709870     788552     Intro_DEN>NonAfrican           689.7     
2          927098     939317     Intro_NEA>NonAfrican           435.3     
3          449311     481743     Intro_NEA>NonAfrican           1551.7
```
Note please feel free to play around with the parameters in the yaml file and use this for your own simulations.
