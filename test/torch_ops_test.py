# Copyright 2020 Bluefog Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import itertools
import unittest
import warnings

import numpy as np
import pytest
import torch
import networkx as nx

import bluefog.torch as bf
from bluefog.common import topology_util


EPSILON = 1e-5
LOOSE_EPSILON = 1e-3
TEST_ON_GPU = torch.cuda.is_available()

class OpsTests(unittest.TestCase):
    """
    Tests for bluefog/torch/mpi_ops.py
    """

    def __init__(self, *args, **kwargs):
        super(OpsTests, self).__init__(*args, **kwargs)
        warnings.simplefilter("module")

    def setUp(self):
        bf.init()

    def convert_cpu_fp16_to_fp32(self, *values):
        # PyTorch doesn't support any CPU ops on FP16 tensors.
        # In case we need to do ops, we will convert tensor to FP32 here.
        result = []
        for value in values:
            if value.dtype in [torch.float16, torch.HalfTensor] and not value.is_cuda:
                result.append(value.float())
            else:
                result.append(value)
        return result

    def cast_and_place(self, tensor, dtype):
        if dtype.is_cuda:
            device_id = bf.local_rank() % torch.cuda.device_count()
            return tensor.cuda(device_id).type(dtype)
        return tensor.type(dtype)

    def test_broadcast(self):
        """Test that the broadcast correctly broadcasts 1D, 2D, 3D tensors."""
        size = bf.size()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.IntTensor, torch.DoubleTensor, torch.LongTensor,
                  torch.ByteTensor, torch.CharTensor, torch.ShortTensor, torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        dims = [1, 2, 3]
        root_ranks = list(range(size))
        for dtype, dim, root_rank in itertools.product(dtypes, dims, root_ranks):
            torch.manual_seed(123456)
            tensor = torch.FloatTensor(*([23] * dim)).random_(-100, 100)
            tensor = self.cast_and_place(tensor, dtype)
            name = "broadcast_tensor_{}_{}".format(dim, dtype)
            if bf.rank() == root_rank:
                bf.broadcast(tensor, root_rank=root_rank, name=name)
            else:
                zero_tensor = torch.zeros_like(tensor)
                output = bf.broadcast(
                    zero_tensor, root_rank=root_rank, name=name
                )
                output, tensor = self.convert_cpu_fp16_to_fp32(output, tensor)
                assert torch.allclose(output, tensor)

    def test_broadcast_inplace(self):
        """Test that the broadcast correctly broadcasts 1D, 2D, 3D tensors."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.IntTensor, torch.DoubleTensor, torch.LongTensor,
                  torch.ByteTensor, torch.CharTensor, torch.ShortTensor, torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        dims = [1, 2, 3]
        root_ranks = list(range(size))
        for dtype, dim, root_rank in itertools.product(dtypes, dims, root_ranks):
            torch.manual_seed(123456)
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            name = "broadcast_inplace_tensor_{}_{}".format(dim, dtype)
            root_tensor = torch.FloatTensor(
                *([23] * dim)).fill_(1).mul_(root_rank)
            tensor = self.cast_and_place(tensor, dtype)
            root_tensor = self.cast_and_place(root_tensor, dtype)

            broadcasted_tensor = bf.broadcast_(tensor, root_rank=root_rank, name=name)

            tensor, broadcasted_tensor, root_tensor = self.convert_cpu_fp16_to_fp32(tensor,
                    broadcasted_tensor, root_tensor)

            assert (
                torch.allclose(tensor, broadcasted_tensor)
            ), "bf.broadcast_ does not modify source tensor"
            assert (
                torch.allclose(broadcasted_tensor, root_tensor)
            ), "bf.broadcast_ produces incorrect broadcasted tensor"

    def test_allreduce_avg(self):
        """Test that the allreduce correctly sums 1D, 2D, 3D tensors."""
        size = bf.size()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.DoubleTensor, torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            torch.manual_seed(123456)
            tensor = torch.FloatTensor(*([23] * dim)).random_(-100, 100)
            name = "allreduce_tensor_{}_{}".format(dim, dtype)
            tensor = self.cast_and_place(tensor, dtype)

            output = bf.allreduce(tensor, average=True, name=name)
            tensor, output = self.convert_cpu_fp16_to_fp32(tensor, output)
            assert (
                torch.allclose(tensor, output)
            ), "bf.allreduce(avg) produces incorrect tensor"

    def test_allreduce_sum(self):
        """Test that the allreduce correctly sums 1D, 2D, 3D tensors."""
        size = bf.size()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.DoubleTensor, torch.IntTensor, torch.DoubleTensor,
                  torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            torch.manual_seed(123456)
            tensor = torch.FloatTensor(*([23] * dim)).random_(-100, 100)
            tensor = self.cast_and_place(tensor, dtype)
            name = "allreduce_tensor_{}_{}".format(dim, dtype)

            output = bf.allreduce(tensor, average=False, name=name)
            tensor, output = self.convert_cpu_fp16_to_fp32(tensor, output)
            assert (
                torch.allclose(output, tensor.mul(size))
            ), "bf.allreduce(sum) produces incorrect tensor"

    def test_allgather(self):
        """Test that the allgather correctly gathers 1D, 2D, 3D tensors."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.IntTensor, torch.DoubleTensor, torch.LongTensor,
                  torch.ByteTensor, torch.CharTensor, torch.ShortTensor, torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([2] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            name = "allgather_tensor_{}_{}".format(dim, dtype)
            gathered = bf.allgather(tensor, name=name)

            tensor, gathered = self.convert_cpu_fp16_to_fp32(tensor, gathered)

            assert list(gathered.shape) == [2 * size] + [2] * (dim - 1)

            for i in range(size):
                rank_tensor = gathered[i * 2: (i + 1) * 2]
                assert (
                    list(rank_tensor.shape) == [2] * dim
                ), "bf.allgather produces incorrect gathered shape"
                assert (
                    rank_tensor.data.min() == i
                ), "bf.allgather produces incorrect gathered tensor"
                assert (
                    rank_tensor.data.max() == i
                ), "bf.allgather produces incorrect gathered tensor"

    @unittest.skipIf(bf.nccl_built(), 'nccl do not support variable size on allgather')
    def test_allgather_variable_size(self):
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.IntTensor, torch.DoubleTensor, torch.LongTensor,
                  torch.ByteTensor, torch.CharTensor, torch.ShortTensor, torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            # Support tests up to MPI Size of 35
            if size > 35:
                break

            tensor_sizes = [17, 32, 81, 12, 15, 23, 22] * 5
            tensor_sizes = tensor_sizes[:size]

            tensor = torch.FloatTensor(
                *([tensor_sizes[rank]] + [17] * (dim - 1))).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            name = "allgather_tensor_{}_{}".format(dim, dtype)
            gathered = bf.allgather(tensor, name=name)

            tensor, gathered = self.convert_cpu_fp16_to_fp32(tensor, gathered)

            expected_size = sum(tensor_sizes)
            assert list(gathered.shape) == [expected_size] + [17] * (dim - 1)

            for i in range(size):
                rank_size = [tensor_sizes[i]] + [17] * (dim - 1)
                rank_tensor = gathered[sum(
                    tensor_sizes[:i]):sum(tensor_sizes[:i + 1])]
                assert list(rank_tensor.shape) == rank_size, \
                    "bf.allgather(var) produces incorrect gathered shape"
                assert rank_tensor.data.min() == i, \
                    "bf.allgather(var) produces incorrect gathered tensor"
                assert rank_tensor.data.max() == i, \
                    "bf.allgather(var) produces incorrect gathered tensor"

    def test_neighbor_allreduce_sum_precision(self):
        """Test that the neighbor all reduce precision (sum) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.DoubleTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        num_indegree = int(np.ceil(np.log2(size)))
        neighbor_ranks = [(rank - 2**i) % size for i in range(num_indegree)]
        sum_value = np.sum(neighbor_ranks) + rank
        sum_value = (len(neighbor_ranks)+1)*(2**-256)

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.DoubleTensor(*([23] * dim)).fill_(1).mul_(2**-256)
            tensor = self.cast_and_place(tensor, dtype)
            name = "neighbor_allreduce_{}_{}".format(dim, dtype)
            nw = {i: 1.0 for i in neighbor_ranks}
            reduced_tensor = bf.neighbor_allreduce(tensor, self_weight=1.0,
                                                   neighbor_weights=nw, name=name)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data - sum_value).abs().max() == 0
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_avg_precision(self):
        """Test that the neighbor all reduce precision (avg) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.DoubleTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        num_indegree = int(np.ceil(np.log2(size)))
        neighbor_ranks = [(rank - 2**i) % size for i in range(num_indegree)]
        sum_value = np.sum(neighbor_ranks) + rank
        sum_value = 2**-256

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.DoubleTensor(*([23] * dim)).fill_(1).mul_(2**-256)
            tensor = self.cast_and_place(tensor, dtype)
            name = "neighbor_allreduce_{}_{}".format(dim, dtype)
            reduced_tensor = bf.neighbor_allreduce(tensor, name=name)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data - sum_value).abs().max() == 0
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"
    @unittest.skip
    def test_neighbor_allreduce_dynamic_topo_check(self):
        """Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        self_weight = 0.0
        neighbor_weights = {(rank-1) % size : 1.0}
        send_ranks = [(rank + 2) % size]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            name = "neighbor_allreduce_{}_{}".format(dim, dtype)
            with pytest.raises(ValueError):
                bf.neighbor_allreduce(tensor, name=name, self_weight=self_weight,
                                      neighbor_weights=neighbor_weights, send_neighbors=send_ranks)

    def test_neighbor_allreduce_dynamic_topo_move(self):
        """Test that the neighbor all reduce (move) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        self_weight = 0.0
        neighbor_weights = {(rank-1) % size : 1.0}
        send_ranks = [(rank + 1) % size]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            name = "neighbor_allreduce_{}_{}".format(dim, dtype)
            reduced_tensor = bf.neighbor_allreduce(
                tensor, name=name, self_weight=self_weight,
                neighbor_weights=neighbor_weights, send_neighbors=send_ranks)
            eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (move) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data - (rank-1) % size).abs().max() < eps
            ), "bf.neighbor_allreduce (move) produces incorrect reduced tensor"

    def test_neighbor_allreduce_dynamic_topo_avg(self):
        """Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        num_indegree = int(np.ceil(np.log2(size)))
        neighbor_ranks = [(rank - 2**i) % size for i in range(num_indegree)]
        sum_value = np.sum(neighbor_ranks) + rank

        self_weight = 1/(num_indegree+1)
        neighbor_weights = {i: self_weight for i in neighbor_ranks}
        send_ranks = [(rank + 2**i) % size for i in range(num_indegree)]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            name = "neighbor_allreduce_{}_{}".format(dim, dtype)
            reduced_tensor = bf.neighbor_allreduce(
                tensor, name=name, self_weight=self_weight,
                neighbor_weights=neighbor_weights, send_neighbors=send_ranks)
            eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data.mul_(num_indegree+1) -
                 sum_value).abs().max() < eps
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_avg(self):
        """Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        num_indegree = int(np.ceil(np.log2(size)))
        neighbor_ranks = [(rank - 2**i) % size for i in range(num_indegree)]
        sum_value = np.sum(neighbor_ranks) + rank

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            name = "neighbor_allreduce_{}_{}".format(dim, dtype)
            reduced_tensor = bf.neighbor_allreduce(tensor, name=name)
            eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data.mul_(num_indegree+1) -
                 sum_value).abs().max() < eps
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_avg_meshgrid_topo(self):
        """
        Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors
        correctly in a 2D meshgrid topology.
        """
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        is_set = bf.set_topology(topology_util.MeshGrid2DGraph(size))
        assert is_set, "Topology set failed."

        topology = bf.load_topology()
        neighbor_array_with_self = np.nonzero(
            nx.to_numpy_matrix(topology)[rank])[1]
        num_indegree = len(neighbor_array_with_self)-1
        sum_value = neighbor_array_with_self.sum()

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            reduced_tensor = bf.neighbor_allreduce(tensor)
            eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data.mul_(num_indegree+1) -
                 sum_value).abs().max() < eps
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_avg_biring_topo(self):
        """
        Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly
        in a bidirectional ring topology.
        """
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        is_set = bf.set_topology(topology_util.RingGraph(size))
        assert is_set, "Topology set failed."

        if size > 2:
            num_indegree = 2
            sum_value = rank+(rank+1) % size+(rank-1) % size
        else:
            num_indegree = 1
            sum_value = 1

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            reduced_tensor = bf.neighbor_allreduce(tensor)
            eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data.mul_(num_indegree+1) -
                 sum_value).abs().max() < eps
            ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_avg_ring_topo(self):
        """
        Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly
        in a ring topology.
        """
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        for connect_direction in [1, 2]:
            is_set = bf.set_topology(
                topology_util.RingGraph(size, connect_direction))
            assert is_set, "Topology set failed."

            num_indegree = 1
            sum_value = rank + \
                (rank+(1 if connect_direction == 1 else -1)) % size

            dims = [1, 2, 3]
            for dtype, dim in itertools.product(dtypes, dims):
                tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
                tensor = self.cast_and_place(tensor, dtype)
                reduced_tensor = bf.neighbor_allreduce(tensor)
                eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
                tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
                assert (
                    list(reduced_tensor.shape) == [23] * dim
                ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
                assert (
                    (reduced_tensor.data.mul_(num_indegree+1) -
                     sum_value).abs().max() < eps
                ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_avg_star_topo(self):
        """
        Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly
        in a star topology.
        """
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        for center_rank in range(size):
            is_set = bf.set_topology(
                topology_util.StarGraph(size, center_rank))
            assert is_set, "Topology set failed."

            if rank == center_rank:
                num_indegree = size-1
                sum_value = size*(size-1)/2
            else:
                num_indegree = 1
                sum_value = rank+center_rank

            dims = [1, 2, 3]
            for dtype, dim in itertools.product(dtypes, dims):
                tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
                tensor = self.cast_and_place(tensor, dtype)
                reduced_tensor = bf.neighbor_allreduce(tensor)
                eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
                tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
                assert (
                    list(reduced_tensor.shape) == [23] * dim
                ), "bf.neighbor_allreduce (avg) produces incorrect reduced shape"
                assert (
                    (reduced_tensor.data.mul_(num_indegree+1) -
                     sum_value).abs().max() < eps
                ), "bf.neighbor_allreduce (avg) produces incorrect reduced tensor"

    def test_neighbor_allreduce_sum(self):
        """Test that the neighbor all reduce (sum) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        num_indegree = int(np.ceil(np.log2(size)))
        neighbor_ranks = [(rank - 2**i) % size for i in range(num_indegree)]
        sum_value = np.sum(neighbor_ranks) + rank

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            nw = {i: 1.0 for i in neighbor_ranks}
            reduced_tensor = bf.neighbor_allreduce(tensor, self_weight=1.0,
                                                   neighbor_weights=nw)
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (sum) produces incorrect reduced shape"
            assert (
                reduced_tensor.data.min() == sum_value
            ), "bf.neighbor_allreduce (sum) produces incorrect reduced tensor"
            assert (
                reduced_tensor.data.max() == sum_value
            ), "bf.neighbor_allreduce (sum) produces incorrect reduced tensor"

    def test_neighbor_allreduce_weighted_avg(self):
        """Test that the neighbor all reduce (avg) 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        bf.set_topology(topology_util.StarGraph(size), is_weighted=True)

        if rank == 0:
            expect_result = (size-1) / 2
        else:
            expect_result = 0 * (1/size) + rank * (1-1/size)
        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            reduced_tensor = bf.neighbor_allreduce(tensor)
            eps = EPSILON if tensor.dtype != torch.float16 else LOOSE_EPSILON
            tensor, reduced_tensor = self.convert_cpu_fp16_to_fp32(tensor, reduced_tensor)
            assert (
                list(reduced_tensor.shape) == [23] * dim
            ), "bf.neighbor_allreduce (weighted_avg) produces incorrect reduced shape"
            assert (
                (reduced_tensor.data - expect_result).abs().max() < eps
            ), "bf.neighbor_allreduce (weighted_avg) produces incorrect reduced tensor"

    def test_neighbor_allgather(self):
        """Test that the neighbor all gather 1D, 2D, 3D tensors correctly."""
        size = bf.size()
        rank = bf.rank()
        if size <= 1:
            fname = inspect.currentframe().f_code.co_name
            warnings.warn("Skip {} due to size 1".format(fname))
            return
        dtypes = [torch.FloatTensor, torch.IntTensor, torch.DoubleTensor, torch.LongTensor,
                  torch.ByteTensor, torch.CharTensor, torch.ShortTensor, torch.HalfTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        # By default, we use power two ring topology.
        num_indegree = int(np.ceil(np.log2(size)))
        neighbor_ranks = [(rank - 2**i) % size for i in range(num_indegree)]

        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            gathered = bf.neighbor_allgather(tensor)
            tensor, gathered = self.convert_cpu_fp16_to_fp32(tensor, gathered)

            assert list(gathered.shape) == [
                23 * num_indegree] + [23] * (dim - 1)

            candidate_ranks = map(float, sorted(neighbor_ranks[:]))
            gathered_ranks = []

            for i, _ in enumerate(neighbor_ranks):
                rank_tensor = gathered[i * 23: (i + 1) * 23]
                assert (
                    list(rank_tensor.shape) == [23] * dim
                ), "bf.neighbor_allgather produces incorrect gathered shape"
                assert (
                    rank_tensor.data.min() == rank_tensor.data.max()
                ), "bf.neighbor_allgather produces incorrect gathered tensor"
                gathered_ranks.append(rank_tensor.data.max().item())

            assert sorted(candidate_ranks) == gathered_ranks, \
                "bf.neighbor_allgather produces incorrect gathered tensor"

    @unittest.skip("Skip due to coordinate operation development.")
    def test_pair_gossip(self):
        size = bf.size()
        rank = bf.rank()
        target_rank = rank - 1 if rank % 2 else rank + 1
        if bf.size() % 2:
            warnings.warn("Pair gossip only run with even processes. Skipped.")
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        expect_result = (rank+target_rank) / 2
        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            gossiped_tensor = bf.pair_gossip(tensor, target_rank)
            tensor, gossiped_tensor = self.convert_cpu_fp16_to_fp32(tensor, gossiped_tensor)

            assert (
                list(gossiped_tensor.shape) == [23] * dim
            ), "bf.pair_gossip produces incorrect reduced shape"
            assert (
                (gossiped_tensor.data - expect_result).abs().max() < EPSILON
            ), "bf.pair_gossip produces incorrect reduced tensor"

    @unittest.skip("Skip due to coordinate operation development.")
    def test_pair_gossip_weighted(self):
        size = bf.size()
        rank = bf.rank()
        target_rank = rank - 1 if rank % 2 else rank + 1
        if bf.size() % 2:
            warnings.warn(
                "Pair gossip(weighted) only run with even processes. Skipped.")
            return
        dtypes = [torch.HalfTensor, torch.FloatTensor, torch.DoubleTensor]
        if TEST_ON_GPU:
            dtypes += [torch.cuda.FloatTensor]
        if bf.nccl_built():  # MPI with CUDA aware may have problem on double tensor format
            dtypes += [torch.cuda.DoubleTensor]

        expect_result = 0.25*rank + 0.75*target_rank
        dims = [1, 2, 3]
        for dtype, dim in itertools.product(dtypes, dims):
            tensor = torch.FloatTensor(*([23] * dim)).fill_(1).mul_(rank)
            tensor = self.cast_and_place(tensor, dtype)
            gossiped_tensor = bf.pair_gossip(
                tensor, target_rank, self_weight=0.25, pair_weight=0.75)
            tensor, gossiped_tensor = self.convert_cpu_fp16_to_fp32(tensor, gossiped_tensor)
            assert (
                list(gossiped_tensor.shape) == [23] * dim
            ), "bf.pair_gossip(weighted) produces incorrect reduced shape"
            assert (
                (gossiped_tensor.data - expect_result).abs().max() < EPSILON
            ), "bf.pair_gossip(weighted) produces incorrect reduced tensor"


if __name__ == "__main__":
    unittest.main()
