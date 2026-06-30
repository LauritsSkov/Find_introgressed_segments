# Find_introgressed_segments
Find introgressed segments from an msprime simulation.

```note
python Keeptrack_of_introgressed.py -demography=Demography1.yaml 
```

First look at the Demography1.yaml. There are multiple introgression events Denisovans. This script will keep track of them. 
Note that you need a sequenced denisova population and the name has to start with "Seq_".

Run the script to produce the following output of introgressed segments:

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
