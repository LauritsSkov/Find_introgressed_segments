import msprime
from collections import defaultdict
import demes
import demesdraw
import matplotlib.pyplot as plt
import argparse

# -----------------------------------------------------------------------------------------------------
# Parameters for demography (plot with demes)
# -----------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-demography", metavar='',help="File with demography", type=str, required=True)
parser.add_argument("-outfile", metavar='',help="outplot name", type=str, default = 'Demography.pdf')

args = parser.parse_args()




def get_introgressed_segments(ts, admixed_ind_from):
    """
    Optimized version: loops through trees once and processes overlapping migrations.
    """

    pop_to_number = {x.metadata['name']: x.id for x in ts.populations()}
    number_to_pop = {x.id: x.metadata['name'] for x in ts.populations()}

    excluded_times = []
    for event in demography.events:
        if type(event) == msprime.demography.PopulationSplit:
            excluded_times.append(event.time)


    Testpopulation = set(ts.get_samples(pop_to_number[admixed_ind_from]))
    introgressed_seg = defaultdict(list)

    # ---- 1. collect relevant migrations ----
    mig_events = []

    for mr in ts.migrations():
        if mr.time not in excluded_times:
            mig_events.append(mr)

    # sort by left coordinate
    mig_events.sort(key=lambda m: m.left)

    mig_idx = 0
    active_migs = []

    # ---- 2. single pass through trees ----
    for tree in ts.trees(leaf_lists=True):
        tree_left, tree_right = map(int, tree.interval)

        # add migrations that start before this tree ends
        while mig_idx < len(mig_events) and mig_events[mig_idx].left < tree_right:
            active_migs.append(mig_events[mig_idx])
            mig_idx += 1

        # remove migrations that end before this tree starts
        active_migs = [
            mr for mr in active_migs if mr.right > tree_left
        ]

        if not active_migs:
            continue

        # ---- 3. process overlapping migrations ----
        for mr in active_migs:
            from_pop = number_to_pop[mr.dest]
            into_pop = number_to_pop[mr.source]
            time = round(mr.time,1)
            admixinfo = f'{from_pop}|{into_pop}|{time}'

            # descendant leaves of the migrant node
            leaves = [x for x in tree.leaves(mr.node)]

            for l in leaves:
                if l in Testpopulation:
                    introgressed_seg[l, admixinfo].append([tree_left, tree_right])

    
    def merge_overlapping(temp_tuple):
        temp_tuple.sort(key=lambda interval: interval[0])
        merged = [temp_tuple[0]]

        for current in temp_tuple:
            previous = merged[-1]
            if current[0] <= previous[1]:
                previous[1] = max(previous[1], current[1])
            else:
                merged.append(current)

        return merged
    

    merged_introgressed_segs = []
    for (haplotype, admix_event), segments in introgressed_seg.items():
        from_pop, to_pop, admixtime = admix_event.split('|')
        for start, end in merge_overlapping(segments):
            merged_introgressed_segs.append((haplotype, start, end, f'{from_pop}>{to_pop}', admixtime))

    return sorted(merged_introgressed_segs)











# -----------------------------------------------------------------------------------------------------
# Parameters for demography (plot with demes)
# -----------------------------------------------------------------------------------------------------

graph = demes.load(f"Demography1.yaml")
demography = msprime.Demography.from_demes(graph)

CHROM_SIZE = 1_000_000
gen_time = 29.0 
rec_rate = 1.45e-8
mutation_rate = 1.45e-8


# Plot demography
fig, ax = plt.subplots()  
demesdraw.tubes(graph, ax=ax, seed=1, log_time=True)
plt.tight_layout()
plt.savefig(args.outfile)

# Simulate
ts = msprime.sim_ancestry(
    samples={"NonAfrican": 2}, 
    demography=demography,
    sequence_length=CHROM_SIZE,
    recombination_rate=rec_rate,
    record_migrations=True,
    random_seed=123)


introgressed_segments = get_introgressed_segments(ts, admixed_ind_from = 'NonAfrican')


row = "{:<10} {:<10} {:<10} {:<30} {:<10}"
print(row.format('haplotype', 'start', 'end',  'admix_event', 'admixtime') )
for (haplotype, start, end,  admix_event, admixtime) in introgressed_segments:
    print(row.format(haplotype, start, end,  admix_event, admixtime))

