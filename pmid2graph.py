import numpy
import argparse

def pmid2graph(values_in, seed, gtype):
#def pmid2graph(table_in):
    # The packages: pandas, numpy, and networkx are required
    #
    # Takes as input the requisite table in .csv format
    # named 'seed.gtype.csv' with header
    #
    # In every case, the output is a .csv file with three (gtype=1) or
    # four (gtype=2,3) columns and a header:
    # seed, pmid_2, edgelength, edgelengthweighted
    # named 'seed.gtype.g.csv'
    #
    # gtype = 1) non-exhaustive list of neighbors...next-next-neighbors
    #    in forward (citation) and reverse (bibliography) from
    #    seed. E.g. an article citing an article citing the
    #    seed is connected with edgelength 2 to the seed.
    #
    #    Input table has two rows including header, variable columns:
    #    cite_1, bib_1,...cite_N,bib_N with contents of the second row:
    #    "pmid_1,...,pmid_M" in every column.
    #
    # gtype = 2) refscore. Seed is connected to all papers with which
    #    it shares at least one reference. edgelength is defined as the
    #    number of references in the union of the bibliographies
    #    divided by the number in the intersection. edgelengthweighted is the
    #    same ratio where each reference is weighted by the inverse of
    #    the size of its citeography.
    #
    #    Input table has variable rows, three columns:
    #    pmid, bibliography, citeography
    #
    # gtype = 3) citescore. Seed is connected to all papers with which
    #    it shares at least one citing article. edgelength is defined as the
    #    number of citing articles in the union of the citeographies
    #    divided by the number in the intersection. edgelengthweighted is the
    #    same ratio where each citing article is weighted by the inverse of
    #    the size of its bibliography.
    #
    #    Input table has variable rows, three columns:
    #    pmid, bibliography, citeography

    # Proceed depending on gtype
    if gtype == 1:
        allpmid = []  # numerically sorted list of pmids beginning with the seed
        for i in range(len(values_in)):
            for j in range(len(values_in[0])):
                if type(values_in[i][j]) == int:
                    allpmid = allpmid + [values_in[i][j]]
                else:
                    allpmid = allpmid + list(map(int, str.split(values_in[i][j], ',')))
        allpmid = sorted(list(set(allpmid)))
        if seed in allpmid:
            allpmid.remove(seed)
        allpmid = [seed] + allpmid

        array_out = numpy.zeros((len(allpmid)-1, 3))+len(values_in[0])+numpy.inf
        array_out[:, 0] = seed
        array_out[:, 1] = allpmid[1:len(allpmid)]
        for i in range(0, len(values_in[0]), 2):  # even columns are citations with positive distance
            valu = list(map(int, str.split(values_in[0][i], ',')))
            indi = numpy.where(numpy.in1d(allpmid[1:len(allpmid)], valu) == 1)
            iles = numpy.less(i/2+1, abs(array_out[indi, 2]))
            array_out[indi[0][iles[0]], 2] = i/2+1
        for i in range(1, len(values_in[0]), 2):  # odd columns are references with negative distance
            valu = list(map(int, str.split(values_in[0][i], ',')))
            indi = numpy.where(numpy.in1d(allpmid[1:len(allpmid)], valu) == 1)
            iles = numpy.less((i-1)/2+1, abs(array_out[indi, 2]))
            array_out[indi[0][iles[0]], 2] = -((i-1)/2+1)

            # #numpy.savetxt(str(seed) + '.' + str(gtype) + '.' + 'g' + '.csv', array_out,
            #               header='seed,pmid_2,edgelength', fmt='%i\t%i\t%f', comments='')

    # elif gtype == 2:
    #     ncite = numpy.zeros((len(values_in), 1))  # size of citeography for each pmid
    #     for i in range(len(values_in)):
    #         ncite[i] = len(str.split(values_in[i, 2], ','))
    #     seedindi = numpy.where(numpy.in1d(values_in[:, 0], seed) == 1)
    #     seedindi = seedindi[0][0]
    #     seedbib = list(map(int, str.split(values_in[seedindi, 1], ',')))
    #     isect = numpy.zeros((len(values_in), 2))  # unweighted/weighted intersection of bibliographies
    #     union = numpy.zeros((len(values_in), 2))  # .. union of bibliographies.
    #     # Note: because bibliographies and citeographies are not returned for all pmids,
    #     # the union between the seed and pmids with an empty intersection is not correct.
    #     # Edges are only, and always, drawn between the seed and pmids with nonzero intersections.
    #     for i in range(len(values_in)):
    #         ibib = list(map(int, str.split(values_in[i, 1], ',')))
    #         ubib = list(set(seedbib + ibib))
    #         indi = numpy.in1d(ibib, seedbib)
    #         isect[i, 0] = numpy.sum(indi == 1)
    #         union[i, 0] = len(ubib)
    #         if isect[i, 0] > 0:
    #             inc = ncite[numpy.in1d(values_in[:, 0], numpy.array(ibib)[indi])]
    #             isect[i, 1] = sum(1/inc)
    #             union[i, 1] = sum(1 / ncite[numpy.in1d(values_in[:, 0], ubib)])
    #     kval = isect[:, 0] > 0
    #     kval[seedindi] = 0
    #     array_out = numpy.zeros((sum(kval), 4))
    #     array_out[:, 0] = seed
    #     array_out[:, 1] = values_in[kval, 0]
    #     array_out[:, 2] = union[kval, 0]/isect[kval, 0]
    #     array_out[:, 3] = union[kval, 1]/isect[kval, 1]
    #     array_out = array_out[array_out[:, 1].argsort()]  # sort pmids numerically
    #     # numpy.savetxt(str(seed) + '.' + str(gtype) + '.' + 'g' + '.csv', array_out,
    #     #               header='seed,pmid_2,edgelength,edgelengthweighted', fmt='%i\t%i\t%f\t%f', comments='')
    #
    # elif gtype == 3:
    #     nbib = numpy.zeros((len(values_in), 1))  # size of bibliography for each pmid
    #     for i in range(len(values_in)):
    #         nbib[i] = len(str.split(values_in[i, 1], ','))
    #     seedindi = numpy.where(numpy.in1d(values_in[:, 0], seed) == 1)
    #     seedindi = seedindi[0][0]
    #     seedcite = list(map(int, str.split(values_in[seedindi, 2], ',')))
    #     isect = numpy.zeros((len(values_in), 2))  # unweighted/weighted intersection of citeographies
    #     union = numpy.zeros((len(values_in), 2))  # .. union of citeographies.
    #     # Note: because bibliographies and citeographies are not returned for all pmids,
    #     # the union between the seed and pmids with an empty intersection is not correct.
    #     # Edges are only, and always, drawn between the seed and pmids with nonzero intersections.
    #     for i in range(len(values_in)):
    #         icite = list(map(int, str.split(values_in[i, 2], ',')))
    #         ubib = list(set(seedcite + icite))
    #         indi = numpy.in1d(icite, seedcite)
    #         isect[i, 0] = numpy.sum(indi == 1)
    #         union[i, 0] = len(ubib)
    #         if isect[i, 0] > 0:
    #             inr = nbib[numpy.in1d(values_in[:, 0], numpy.array(icite)[indi])]
    #             isect[i, 1] = sum(1/inr)
    #             union[i, 1] = sum(1 / nbib[numpy.in1d(values_in[:, 0], ubib)])
    #     kval = isect[:, 0] > 0
    #     kval[seedindi] = 0
    #     array_out = numpy.zeros((sum(kval), 4))
    #     array_out[:, 0] = seed
    #     array_out[:, 1] = values_in[kval, 0]
    #     array_out[:, 2] = union[kval, 0]/isect[kval, 0]
    #     array_out[:, 3] = union[kval, 1]/isect[kval, 1]
    #     array_out = array_out[array_out[:, 1].argsort()]  # sort pmids numerically
    #     # numpy.savetxt(str(seed) + '.' + str(gtype) + '.' + 'g' + '.csv', array_out,
    #     #               header='seed,pmid_2,edgelength,edgelengthweighted', fmt='%i\t%i\t%f\t%f', comments='')

    return array_out

def correct_info(InfoFileName):
    CorrectedInfo = []
    for Line in open(InfoFileName):
        InfoFields = Line[:-1].split("\t")
        InfoFields[0] = InfoFields[1]
        InfoFields[2] = InfoFields[3]
        InfoFields[4] = InfoFields[5]
        CorrectedInfo.extend(InfoFields)

    return numpy.asarray([CorrectedInfo])



ap = argparse.ArgumentParser(description = "For given list of PMIDs builds graph distance")
ap.add_argument("-f", help = "File with PMIDs", required = True)
ap.add_argument("-d", help = "Directory where pubmed data is stored", required = True)
ap.add_argument("-g", help = "Graph type", required = True)
opts = ap.parse_args()

PMIDsFileName = opts.f
DataFolder = opts.d
GraphType = int(opts.g)

for Line in open(PMIDsFileName):
    PMId = Line[:-1]

    ## fix for pmid2grpaph function
    CorrectedPMIdInfo = correct_info(DataFolder + PMId + ".tab")
    if CorrectedPMIdInfo[0][1] == "": ## empty file
        continue

    for Edge in pmid2graph(CorrectedPMIdInfo, PMId, GraphType).tolist():
        print(str(int(Edge[0])) + "\t" + str(int(Edge[1])) + "\t" + "\t".join([str(x) for x in Edge[2:]]))
