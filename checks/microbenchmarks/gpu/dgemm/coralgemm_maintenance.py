# Copyright Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause
# --> JIRA/SSA-900

import os
import reframe as rfm
import reframe.utility.sanity as sn
from uenv import uarch

PM_ENERGY = ['accel0_energy', 'accel1_energy', 'accel2_energy',
             'accel3_energy', 'energy']
PM_POWER = ['accel0_power', 'accel1_power', 'accel2_power', 'accel3_power',
            'power']
PM_CAP = ['accel0_power_cap', 'accel1_power_cap', 'accel2_power_cap',
          'accel3_power_cap',
          'power_cap']
PM_RAW = ['freshness', 'generation', 'raw_scan_hz', 'startup', 'version']
# MI300: overshoot, overshoot_energy, capped_energy
# MI200: cpu0_temp, cpu_energy/power, memory_energy/power


def _pm_metric(pm_file, field=None):
    '''
CSCS_RFM_UENV=prgenv-gnu/7.2.3:v1 reframe \
-C cscs-reframe-tests.git/config/cscs.py     --keep-stage-files \
--report-file latest.json \
-c checks/microbenchmarks/gpu/dgemm/coralgemm_maintenance.py \
-n 128000.*64F --repeat 3 -J w=nid002520 --system beverin:mi300 \
--exec-policy serial -r

    Reads /sys/cray/pm_counters/* and extract by format:
      *_energy     -> '<n> J <n> us'
      *_power      -> '<n> W <n> us'
      *_power_cap  -> '<n> W'
      the rest     -> '<n>'

    `field` is one of 'J', 'W', 'us' or 'None' for files holding a
    single integer. The unit of the metric is the field itself.
    '''
    if field:
        regex, tag = rf'(?P<{field}>\d+) {field}', field
    else:
        regex, tag = r'(?P<val>\d+)', 'val'

    return sn.make_performance_function(
        sn.extractsingle(regex, pm_file, tag, int), field or ''
    )

def _gflops(self, pf_op):
    regex = r'^\s+(?P<GF>\S+)\s+\d'
    if pf_op == 'min':
        return sn.make_performance_function(
            sn.min(sn.extractall(regex, self.stdout, 'GF', float)), 'GFlops')
    elif pf_op == 'avg':
        return sn.make_performance_function(
            sn.avg(sn.extractall(regex, self.stdout, 'GF', float)), 'GFlops')
    elif pf_op == 'max':
        return sn.make_performance_function(
            sn.max(sn.extractall(regex, self.stdout, 'GF', float)), 'GFlops')
    else:
        return None


@rfm.simple_test
class CoralGemm(rfm.RunOnlyRegressionTest):
    descr = 'AMD CoralGemm test'
    valid_systems = ['+amdgpu +uenv']
    valid_prog_environs = ['+uenv +prgenv +rocm']
    maintainers = ['SSA']
    sourcesdir = 'scripts'
    build_system = 'CMake'
    prebuild_cmds = [
        # 'git clone --depth 1 --branch 2025.11 '
        # 'https://github.com/AMD-HPC/CoralGemm.git'
        'tar xf CoralGemm.git.tgz',
        'ln -s CoralGemm.git CoralGemm'
    ]
    postbuild_cmds = ['rm -fr CoralGemm.git.tgz CoralGemm.git']
    time_limit = '3m'
    build_locally = False
    num_tasks_per_node = 1
    ### regex = r'    (?P<A0>\S+)\s+(?P<A1>\S+)\s+(?P<A2>\S+)\s+(?P<A3>\S+)\s+\d'
    rocr_visible_devices = parameter(['0', '1', '2', '3'])
    # rocr_visible_devices = parameter(['0', '3'])
    rocr_visible_devices_on = variable(str, value='True')
    tags = {'production', 'uenv', 'benchmark', 'bencher'}

    # {{{ Sweep matrix sizes and precisions
    # dimensions are in bytes for one dimension of a square matrix
    _size_bytes = parameter([12800, 25600, 51200, 128000])
    _precisions = parameter(['R_16B', 'R_32F', 'R_64F'])

    # Data precision for matrix A, B, C and computation
    precision_A = variable(str, value='R_64F')
    precision_B = variable(str, value='R_64F')
    precision_C = variable(str, value='R_64F')
    compute_precision = variable(str, value='R_64F')

    # Operation applied to matrix A and B, eg. OP_N, OP_T, OP_C
    op_A = variable(str, value='OP_N')
    op_B = variable(str, value='OP_T')

    # Matrix dimensions
    M = variable(int, value=9728)
    N = variable(int, value=6144)
    K = variable(int, value=8192)

    # Leading dimensions of matrix A, B, C
    lda = variable(int, value=9728)
    ldb = variable(int, value=6144)
    ldc = variable(int, value=9728)

    # Number of batched matrices
    batch_count = variable(int, value=1)

    # Duration to run the GEMM operation in seconds
    duration = variable(int, value=45)

    # Optional argument to run the extended version of the benchmark
    batched = variable(bool, value=False)
    strided = variable(bool, value=False)
    ex_api = variable(bool, value=False)
    hipBLASLt_api = variable(bool, value=False)

    # A, B, C matrices are stored in host memory
    host_A = variable(bool, value=False)
    host_B = variable(bool, value=False)
    host_C = variable(bool, value=False)

    # if in host memory, A/B/C is coherent (not cached)
    coherent_A = variable(bool, value=False)
    coherent_B = variable(bool, value=False)
    coherent_C = variable(bool, value=False)

    shared_A = variable(bool, value=False)
    shared_B = variable(bool, value=False)

    # set beta to zero
    zero_beta = variable(bool, value=False)
    # }}}

#ori     @run_before('compile')
#ori     def set_build_options(self):
#ori         self.build_system.configuredir = 'CoralGemm'
#ori         self.build_system.builddir = 'build'
#ori 
#ori         gpu_arch = self.current_partition.select_devices('gpu')[0].arch
#ori         if 'rocm' in self.current_environ.features:
#ori             self.build_system.config_opts = [
#ori                 '-DCMAKE_BUILD_TYPE=Release',
#ori                 '-DUSE_CUDA=OFF',
#ori                 '-DUSE_HIP=ON',
#ori                 f'-DCMAKE_HIP_ARCHITECTURES="{gpu_arch}"'
#ori             ]
#ori         else:  # cuda
#ori             gpu_arch = (
#ori                 gpu_arch[len("sm_"):]
#ori                 if gpu_arch.startswith("sm_")
#ori                 else gpu_arch
#ori             )
#ori             self.build_system.config_opts = [
#ori                 '-DCMAKE_BUILD_TYPE=Release',
#ori                 '-DUSE_CUDA=ON',
#ori                 '-DUSE_HIP=OFF',
#ori                 f'-DCMAKE_CUDA_ARCHITECTURES="{gpu_arch}"'
#ori             ]

    @run_after('setup')
    def set_num_gpus(self):
        curr_part = self.current_partition
        self.num_gpus = curr_part.select_devices('gpu')[0].num_devices

    @run_before('run')
    def set_executable(self):
        # {{{
        # Set mandatory arguments of the benchmark
        ## self.executable = os.path.join(self.build_system.builddir, 'gemm')
        self.executable = './___gemm'

        # Data precision for matrix A, B, C and computation
        self.precision_A = self._precisions
        self.precision_B = self._precisions
        self.precision_C = self._precisions
        self.compute_precision = self._precisions

        if self.precision_A == 'R_16B':
            self.precision_C = 'R_32F'
            self.compute_precision = 'R_32F'

        # Adjust matrix sizes based on the current parameters
        if self.precision_C == 'R_32F':
            self.M = self._size_bytes // 4
            self.N = self._size_bytes // 4
            self.K = self._size_bytes // 4
        else:  # R_64F
            self.M = self._size_bytes // 8
            self.N = self._size_bytes // 8
            self.K = self._size_bytes // 8

        # Leading dimensions of matrix A, B, C
        self.lda = self.M
        self.ldb = self.N
        self.ldc = self.M

        self.executable_opts = [
            f'{self.precision_A} ',
            f'{self.precision_B} ',
            f'{self.precision_C} ',
            f'{self.compute_precision} ',
            f'{self.op_A} ',
            f'{self.op_B} ',
            f'{self.M} ',
            f'{self.N} ',
            f'{self.K} ',
            f'{self.lda} ',
            f'{self.ldb} ',
            f'{self.ldc} ',
            f'{self.batch_count} ',
            f'{self.duration}'
        ]

        # Fix option for BF16 precision
        if self._precisions == 'R_16B':
            self.executable_opts.append('ex')

        # Set optional arguments of the benchmark
        if self.batched:
            self.executable_opts.append('batched')

        if self.strided:
            self.executable_opts.append('strided')

        if self.ex_api:
            self.executable_opts.append('ex')

        if self.hipBLASLt_api:
            self.executable_opts.append('lt')

        if self.host_A:
            self.executable_opts.append('hostA')

        if self.host_B:
            self.executable_opts.append('hostB')

        if self.host_C:
            self.executable_opts.append('hostC')

        if self.coherent_A:
            self.executable_opts.append('coherentA')

        if self.coherent_B:
            self.executable_opts.append('coherentB')

        if self.coherent_C:
            self.executable_opts.append('coherentC')

        if self.shared_A:
            self.executable_opts.append('sharedA')

        if self.shared_B:
            self.executable_opts.append('sharedB')

        if self.zero_beta:
            self.executable_opts.append('zeroBeta')

        # Set the time limit with a padding of 2 minutes
        self.time_limit = self.duration + 120
    # }}}

    @sanity_function
    def assert_results(self):
        return True
#ori         # The binary automatically launches on all available GPUs
#ori         # simultaneously, so we check that the output contains performance
#ori         # results for all GPUs.
#ori         s1 = sn.all([
#ori             sn.assert_found(rf'device_{i}_\[GFLOPS\]', self.stdout)
#ori             for i in range(self.num_gpus)
#ori         ])
#ori 
#ori         # We also check that the output does not contain more GPUs than
#ori         # the expected number. In case of misconfiguration, the node can
#ori         # appear to have more GPUs than it actually has, with lower
#ori         # performance.
#ori         s2 = sn.assert_not_found(rf'device_{self.num_gpus}', self.stdout)
#ori 
#ori         return sn.all([s1, s2])

    @run_before('run')
    def pre_post_scripts(self):
        self.env_vars = {
            'ROCR_VISIBLE_DEVICES': self.rocr_visible_devices,
            'HIP_VISIBLE_DEVICES': self.rocr_visible_devices
        }
        self.prerun_cmds += [
            './boot_time.sh',
            './coral/gpumon.sh start 1',
            './pm_counters.sh pm_t0',
            'echo "# _t0=$(date +%s)"'
        ]

        self.postrun_cmds += [
            'echo "# _t1=$(date +%s)"',
            './pm_counters.sh pm_t1',
            './coral/gpumon.sh stop',
            '# if the test crash or is cancelled:',
            'trap "./coral/gpumon.sh stop" EXIT INT TERM'
        ]

        self.uarch = uarch(self.current_partition)
        if self.uarch == 'mi200':
            PM_ENERGY.extend(['cpu_energy', 'memory_energy'])
            PM_POWER.extend(['cpu_power', 'memory_power'])

        if self.uarch == 'mi300':
            PM_ENERGY.extend(['overshoot_energy', 'capped_energy'])
            PM_RAW.append('overshoot')
#         warnings:
#             'pm_t0_cpu_energy_J':     'pm_t0_memory_energy_J':
#             'pm_t0_cpu_energy_us':    'pm_t0_memory_energy_us':
#             'pm_t0_cpu_power_us':     'pm_t0_memory_power_us':
#             'pm_t0_cpu_power_W':      'pm_t0_memory_power_W':

    # {{{ _elapsed, _boot_time, MI200/MI300
    @performance_function('s')
    def _elapsed(self):
        regex0 = r'# _t0=(?P<tt>\d+)'
        regex1 = r'# _t1=(?P<tt>\d+)'
        _t0 = sn.extractsingle(regex0, self.stdout, 'tt', int)
        _t1 = sn.extractsingle(regex1, self.stdout, 'tt', int)
        return (_t1 - _t0)

    @performance_function('s')
    def _boot_time_epoch(self):
        regex = r'# boot_time (?P<hh>\d+) h (?P<mm>\d+) m / (?P<ee>\d+)'
        return sn.extractsingle(regex, self.stdout, 'ee', int)

    @performance_function('minutes')
    def _boot_time_elapsed(self):
        regex = r'# boot_time (?P<hh>\d+) h (?P<mm>\d+) m / (?P<ee>\d+)'
        hh = sn.extractsingle(regex, self.stdout, 'hh', int)
        mm = sn.extractsingle(regex, self.stdout, 'mm', int)
        return (hh*60 + mm)

    @loggable
    @property
    def _boot_time_mi(self):
        '''
        MI200:gfx90a, MI300:gfx942
        '''
        try:
            fname = sn.evaluate(self.stdout)
            if fname and not os.path.isabs(fname):
                fname = os.path.join(self.stagedir, fname)

            regex = r'# boot_time.* / MI=(?P<mi>\S+)'
            mi = sn.evaluate(sn.extractsingle(regex, fname, 'mi', str))
        except Exception:
            # No job yet, or the line is not in the output
            return None

        # self._boot_time_mi_value = mi
        return mi
    # }}}

    # {{{ (min,avg,max) gflops per gpu (0,1,2,3)
    @run_before('performance')
    def report_gflops(self):
        for ii in range(4):
            if self.rocr_visible_devices == str(ii):
                self.perf_variables[f'_gpu{ii}_min'] = _gflops(self, 'min')
                self.perf_variables[f'_gpu{ii}_avg'] = _gflops(self, 'avg')
                self.perf_variables[f'_gpu{ii}_max'] = _gflops(self, 'max')
            else:
                self.perf_variables[f'_gpu{ii}_min'] = sn.make_performance_function(lambda: -1, 'GFlops')
                self.perf_variables[f'_gpu{ii}_avg'] = sn.make_performance_function(lambda: -1, 'GFlops')
                self.perf_variables[f'_gpu{ii}_max'] = sn.make_performance_function(lambda: -1, 'GFlops')

    if not rocr_visible_devices_on:
        # --- GPU0
        @performance_function('GFlops')
        def _gpu0_min(self):
            return sn.min(sn.extractall(self.regex, self.stdout, 'A0', float))

        @performance_function('GFlops')
        def _gpu0_avg(self):
            return sn.avg(sn.extractall(self.regex, self.stdout, 'A0', float))

        @performance_function('GFlops')
        def _gpu0_max(self):
            return sn.max(sn.extractall(self.regex, self.stdout, 'A0', float))

        # --- GPU1
        @performance_function('GFlops')
        def _gpu1_min(self):
            return sn.min(sn.extractall(self.regex, self.stdout, 'A1', float))

        @performance_function('GFlops')
        def _gpu1_avg(self):
            return sn.avg(sn.extractall(self.regex, self.stdout, 'A1', float))

        @performance_function('GFlops')
        def _gpu1_max(self):
            return sn.max(sn.extractall(self.regex, self.stdout, 'A1', float))

        # --- GPU2
        @performance_function('GFlops')
        def _gpu2_min(self):
            return sn.min(sn.extractall(self.regex, self.stdout, 'A2', float))

        @performance_function('GFlops')
        def _gpu2_avg(self):
            return sn.avg(sn.extractall(self.regex, self.stdout, 'A2', float))

        @performance_function('GFlops')
        def _gpu2_max(self):
            return sn.max(sn.extractall(self.regex, self.stdout, 'A2', float))

        # --- GPU3
        @performance_function('GFlops')
        def _gpu3_min(self):
            return sn.min(sn.extractall(self.regex, self.stdout, 'A3', float))

        @performance_function('GFlops')
        def _gpu3_avg(self):
            return sn.avg(sn.extractall(self.regex, self.stdout, 'A3', float))

        @performance_function('GFlops')
        def _gpu3_max(self):
            return sn.max(sn.extractall(self.regex, self.stdout, 'A3', float))
    # }}}

    # {{{ pm_counters
    @run_before('performance')
    def _pm_counters(self):
        for pmd in ('pm_t0', 'pm_t1'):
            for f in PM_ENERGY:
                self.perf_variables[f'{pmd}_{f}_J'] = \
                    _pm_metric(f'{pmd}/{f}', 'J')
                self.perf_variables[f'{pmd}_{f}_us'] = \
                    _pm_metric(f'{pmd}/{f}', 'us')

            for f in PM_POWER:
                self.perf_variables[f'{pmd}_{f}_W'] = \
                    _pm_metric(f'{pmd}/{f}', 'W')
                self.perf_variables[f'{pmd}_{f}_us'] = \
                    _pm_metric(f'{pmd}/{f}', 'us')

            for f in PM_CAP:
                self.perf_variables[f'{pmd}_{f}_W'] = \
                    _pm_metric(f'{pmd}/{f}', 'W')

            for f in PM_RAW:
                self.perf_variables[f'{pmd}_{f}'] = \
                    _pm_metric(f'{pmd}/{f}')
    # }}}

    _ref_flops = {
        # These are the average GFLOPS observed on the respective systems,
        # sizes are in bytes.
        'mi200': {
            'R_16B': {12800: 92955, 25600: 108550, 51200: 119803, 128000: 87451},  # noqa: E501
            'R_32F': {12800: 31598, 25600: 30690, 51200: 32907, 128000: 28638},
            'R_64F': {12800: 19102, 25600: 23178, 51200: 26740, 128000: 23870}
        },
        'mi300': {
            'R_16B': {12800: 230008, 25600: 428416, 51200: 389497, 128000: 273200},  # noqa: E501
            'R_32F': {12800: 64777, 25600: 74340, 51200: 80478, 128000: 67092},
            'R_64F': {12800: 25702, 25600: 52668, 51200: 60874, 128000: 53913}
        },
        'gh200': {
            'R_16B': {12800: 548292, 25600: 570109, 51200: 574525, 128000: 599912},  # noqa: E501
            'R_32F': {12800: 47849, 25600: 50990, 51200: 52200, 128000: 51011},
            'R_64F': {12800: 42362, 25600: 40700, 51200: 39845, 128000: 51717}
        },
    }
