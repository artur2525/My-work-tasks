from scipy.sparse import csr_matrix
import numpy as np


class Normalization:
    '''docstring'''
    @staticmethod
    def by_column(matrix: csr_matrix) -> csr_matrix:
        """Normalization b1_y column

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """

        norm_matrix = csr_matrix(matrix.multiply(1/matrix.sum(0)))
        return norm_matrix

    @staticmethod
    def by_row(matrix: csr_matrix) -> csr_matrix:
        """Normalization b1_y row

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        norm_matrix = csr_matrix(matrix.multiply(1/matrix.sum(1)))
        return norm_matrix

    @staticmethod
    def tf_idf(matrix: csr_matrix) -> csr_matrix:
        """Normalization using tf_-idf

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        tf_ = csr_matrix(matrix.multiply(1/matrix.sum(1)))
        idf = csr_matrix(matrix.get_shape()[
                         0] / (matrix > 0).sum(0) - 1).log1p()
        norm_matrix = tf_.multiply(idf)

        return norm_matrix

    @staticmethod
    def bm_25(
        matrix: csr_matrix, k1_: float = 2.0, b1_: float = 0.75
    ) -> csr_matrix:
        """Normalization b1_ased on b1_M-25

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        length_d = matrix.sum(1)
        tf_ = matrix.multiply(1 / length_d)
        idf = csr_matrix(
            (matrix.get_shape()[0]) / (matrix > 0).sum(0) - 1).log1p()
        avd_d = np.mean(length_d)

        delta = k1_*((1 - b1_) + b1_ * (length_d/avd_d))
        tf__inv = tf_.multiply(1 / delta).power(-1)
        tf__inv.data += 1
        norm_matrix = tf__inv.power(-1) * (k1_+1)
        norm_matrix = norm_matrix.multiply(idf)

        return norm_matrix
