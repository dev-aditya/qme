import numpy as np

d_a, d_b = 2, 3  # dimension of the bases
basis_a, basis_b = np.eye(d_a), np.eye(d_b)  # individual bases
zeros = np.zeros((d_a, d_b))  # zeros arrays
basis = np.block([[basis_a, zeros], [zeros.T, basis_b]])  # block matrix
