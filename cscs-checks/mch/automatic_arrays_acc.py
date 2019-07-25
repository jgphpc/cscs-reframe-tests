import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class AutomaticArraysCheck(rfm.RegressionTest):
    def __init__(self):
        super().__init__()
        self.valid_systems = ['daint:gpu', 'dom:gpu', 'kesch:cn', 'tsa:cn', 'arolla:cn']
        self.valid_prog_environs = ['PrgEnv-cray', 'PrgEnv-cce', 'PrgEnv-pgi']
        if self.current_system.name in ['daint', 'dom']:
            self.modules = ['craype-accel-nvidia60']
        elif self.current_system.name == 'kesch':
            self.exclusive_access = True
            self.modules = ['craype-accel-nvidia35']
            # FIXME: workaround -- the variable should not be needed since
            # there is no GPUdirect in this check
            self.variables = {'MV2_USE_CUDA': '1'}
        elif self.current_system.name == 'arolla':
            self.exclusive_access = True
            self.modules = [
                'cuda92/toolkit/9.2.88',
                'craype-accel-nvidia70',
            ]
        elif self.current_system.name == 'tsa':
            self.exclusive_access = True
            self.modules = [
                'cuda10.0/toolkit/10.0.130',
                'craype-accel-nvidia70',
            ]

        # This test requires an MPI compiler, although it uses a single task
        self.num_tasks = 1
        self.num_gpus_per_node = 1
        self.num_tasks_per_node = 1
        self.sourcepath = 'automatic_arrays_OpenACC.F90'
        self.build_system = 'SingleSource'
        self.build_system.fflags = ['-O2']
        self.sanity_patterns = sn.assert_found(r'Result: ', self.stdout)
        self.perf_patterns = {
            'time': sn.extractsingle(r'Timing:\s+(?P<time>\S+)',
                                     self.stdout, 'time', float)
        }

        self.arrays_reference = {
            'PrgEnv-cce': {
                'kesch:cn': {'time': (2.9E-04, None, 0.15)},
                'arolla:cn': {'time': (2.9E-04, None, 0.15)},
                'tsa:cn': {'time': (2.9E-04, None, 0.15)},
            },
            'PrgEnv-cray': {
                'daint:gpu': {'time': (5.7E-05, None, 0.15)},
                'dom:gpu': {'time': (5.8E-05, None, 0.15)},
                'kesch:cn': {'time': (2.9E-04, None, 0.15)},
            },
            'PrgEnv-pgi': {
                'daint:gpu': {'time': (6.4E-05, None, 0.15)},
                'dom:gpu': {'time': (6.3E-05, None, 0.15)},
                'kesch:cn': {'time': (1.4E-04, None, 0.15)},
                'arolla:cn': {'time': (1.4E-04, None, 0.15)},
                'tsa:cn': {'time': (1.4E-04, None, 0.15)},
            }
        }

        self.maintainers = ['AJ', 'VK']
        self.tags = {'production', 'mch'}

    def setup(self, partition, environ, **job_opts):
        if environ.name.startswith('PrgEnv-cray'):
            envname = 'PrgEnv-cray'
            self.build_system.fflags += ['-hacc', '-hnoomp']
        elif environ.name.startswith('PrgEnv-cce'):
            envname = 'PrgEnv-cce'
            self.build_system.fflags += ['-hacc', '-hnoomp']
        elif environ.name.startswith('PrgEnv-pgi'):
            envname = 'PrgEnv-pgi'
            self.build_system.fflags += ['-acc']
            if self.current_system.name in ['daint', 'dom']:
                self.build_system.fflags += ['-ta=tesla,cc60', '-Mnorpath']
            elif self.current_system.name == 'kesch':
                self.build_system.fflags += ['-ta=tesla,cc35,cuda9.2']
            elif self.current_system.name == 'arolla':
                self.build_system.fflags += ['-ta=tesla,cc70,cuda9.2']
            elif self.current_system.name == 'tsa':
                self.build_system.fflags += ['-ta=tesla,cc70,cuda10.0']
        else:
            envname = environ.name

        self.reference = self.arrays_reference[envname]
        super().setup(partition, environ, **job_opts)
