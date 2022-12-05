#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import chumpy as ch
import scipy.sparse as sp

from chumpy.utils import col


class sp_dot(ch.Ch):
    terms = 'a',
    dterms = 'b',

    def on_changed(self, which):
        if 'a' in which:
            a_csr = sp.csr_matrix(self.a)
            # To stay consistent with numpy, we must upgrade 1D arrays to 2D
            self.ar = sp.csr_matrix((a_csr.data, a_csr.indices, a_csr.indptr),
                                    shape=(max(np.sum(a_csr.shape[:-1]), 1), a_csr.shape[-1]))

        if 'b' in which:
            self.br = col(self.b.r) if len(self.b.r.shape) < 2 else self.b.r.reshape((self.b.r.shape[0], -1))

        if 'a' in which or 'b' in which:
            self.k = sp.kron(self.ar, sp.eye(self.br.shape[1], self.br.shape[1]))

    def compute_r(self):
        return self.a.dot(self.b.r)

    def compute(self):
        if self.br.ndim <= 1:
            return self.ar
        elif self.br.ndim <= 2:
            return self.k
        else:
            raise NotImplementedError

    def compute_dr_wrt(self, wrt):
        if wrt is self.b:
            return self.compute()
