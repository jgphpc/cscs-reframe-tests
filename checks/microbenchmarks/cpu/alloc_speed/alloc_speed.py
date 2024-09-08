# Copyright 2016 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


alloc_reference = {
    'zen2': {
        # cce:0.32,0.16 intel:0.13:0.06 gnu:0.14,0.07
        'no': (0.32, None, 0.15, 's'),
        '2M': (0.16, None, 0.15, 's'),
    },
    'neoverse_v2': {
        # cce:0.13,0.04 gnu:0.08,0.04
        'no': (0.13, None, 0.15, 's'),
        '2M': (0.07, None, 0.15, 's'),
    },
}


class AllocSpeedTestBase(rfm.RegressionTest):
    sourcepath = 'alloc_speed.cpp'
    build_system = 'SingleSource'

    @run_after('init')
    def set_descr(self):
        self.descr = (f'Time to allocate 4096 MB using {self.hugepages} '
                      f'hugepages')

    @run_before('compile')
    def set_cxxflags(self):
        # avoid -O3 because some compilers over-optimize
        self.build_system.cxxflags = ['-std=c++11']

    @sanity_function
    def assert_4GB(self):
        return sn.assert_found('4096 MB', self.stdout)

    @performance_function('s')
    def elapsed(self):
        return sn.extractsingle(r'4096 MB, allocation time (?P<time>\S+)',
                                self.stdout, 'time', float)

    @run_before('performance')
    def set_performance_reference(self):
        self.skip_if_no_procinfo()
        proc_info_arch = self.current_partition.processor.info['arch']
        self.reference = {
            '*': {
                'elapsed': alloc_reference[proc_info_arch][self.hugepages]
            }
        }


@rfm.simple_test
class CPE_AllocSpeedTest(AllocSpeedTestBase):
    hugepages = parameter(['no', '2M'])
    valid_systems = ['+remote +cpe']
    valid_prog_environs = ['+cpe']
    tags = {'production', 'craype'}

    @run_after('setup')
    def skip_builtin_env(self):
        self.skip_if(self.current_environ.name.startswith('PrgEnv-aocc'))

    @run_after('setup')
    def set_modules(self):
        if self.hugepages == 'no':
            return

        self.modules += [f'craype-hugepages{self.hugepages}']


@rfm.simple_test
class UENV_AllocSpeedTest(AllocSpeedTestBase):
    hugepages = parameter(['no'])
    valid_systems = ['+remote +uenv']
    valid_prog_environs = ['+uenv']
    tags = {'production', 'uenv'}
    build_locally = False
