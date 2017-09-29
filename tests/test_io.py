import pytest

try:
    import parasail
except ImportError:
    import sys, os
    myPath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, myPath + '/../')
    import parasail

def create_input_file(filename):
    with open(filename, 'w') as fp:
        fp.write('''>AF0017_1 COG1250 # Protein_GI_number: 11497638 # Func_class: I Lipid transport and metabolism  # Function: 3-hydroxyacyl-CoA dehydrogenase # Organism: Archaeoglobus fulgidus
MMVLEIRNVAVIGAGSMGHAIAEVVAIHGFNVKLMDVSEDQLKRAMEKIEEGLRKSYERGYISEDPEKVLKRIEATADLIEVAKDADLVIEAIPEIFDLKKKVFSEIEQYCPDHTIFATNTSSLSITKLAEATKRPEKFIGMHFFNPPKILKLLEIVWGEKTSEETIRIVEDFARKIDRIIIHVRKDVPGFIVNRIFVTMSNEASWAVEMGEGTIEEIDSAVKYRLGLPMGLFELHDVLGGGSVDVSYHVLEYYRQTLGESYRPSPLFERLFKAGHYGKKTGKGFYDWSEGKTNEVPLRAGANFDLLRLVAPAVNEAAWLIEKGVASAEEIDLAVLHGLNYPRGLLRMADDFGIDSIVKKLNELYEKYNGEERYKVNPVLQKMVEEGKLGRTTGEGFYKYGD
>AF0017_2_COG1024_#_Protein_GI_number: 11497638 # Func_class: I Lipid transport and metabolism  # Function: Enoyl-CoA hydratase/carnithine racemase # Organism: Archaeoglobus fulgidus
GNYEFVKVEKEGKVGVLKLNRPRRANALNPTFLKEVEDALDLLERDEEVRAIVIAGEGKNFCAGADIAMFASGRPEMVTEFSQLGHKVFRKIEMLSKPVIAAIHGAAVGGGFELAMACDLRVMSERAFLGLPELNLGIIPGWGGTQRLAYYVGVSKLKEVIMLKRNIKPEEAKNLGLVAEVFPQERFWDEVMKLAREVAELPPLAVKYLKKVIALGTMPALETGNLAESEAGAVIALTDDVAEGIQAFNYRRKPNFRGR
''')

def work(filename):
    sequences = parasail.sequences_from_file(filename)
    print(len(sequences))
    print(len(sequences[0]))
    print(sequences[0])
    print(len(sequences[-1]))
    print(sequences[-1])
    print(sequences[0][0])
    with pytest.raises(TypeError):
        print(sequences['asdf'])
    with pytest.raises(TypeError):
        print(sequences[0]['asdf'])
    with pytest.raises(IndexError):
        print(sequences[1000000])
    with pytest.raises(IndexError):
        print(sequences[-1000000])
    with pytest.raises(IndexError):
        print(sequences[0][1000000])
    with pytest.raises(IndexError):
        print(sequences[0][-1000000])
    print("name:    '{}'".format(sequences[0].name))
    print("comment: '{}'".format(sequences[0].comment))
    print("seq:     '{}'".format(sequences[0].seq))
    print("qual:    '{}'".format(sequences[0].qual))
    print("characters: {}".format(sequences.characters))
    print("shortest:   {}".format(sequences.shortest))
    print("longest:    {}".format(sequences.longest))
    print("mean:       {}".format(sequences.mean))
    print("stddev:     {}".format(sequences.stddev))

def test1(tmpdir):
    filename = 'input.txt'
    file = tmpdir.join(filename)
    create_input_file(file.strpath)
    work(file.strpath)

if __name__ == '__main__':
    import sys
    work(sys.argv[1])
