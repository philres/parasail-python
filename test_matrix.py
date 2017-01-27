import parasail

matrix = parasail.blosum62
matrix[3,4] = 100

matrix = parasail.blosum62.copy()
matrix[3,4] = 100
print matrix.matrix

matrix = parasail.matrix_create("ACGT", 10, 1)
matrix[2] = 200
matrix[1:3, 1:3] = 300
matrix.set_value(0,4,400)
print matrix.matrix
