import os
import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class tuto_serial(rfm.RegressionTest):
    descr = "Compile, execute et analyse le code pi_integral"
    maintainers = ['pmcs2i', '@jgphpc']
    valid_systems = ['+cpu']
    valid_prog_environs = ['+serial']
    # no:sourcesdir = 'git@gitlab.pmcs2i.ec-lyon.fr:PMCS2I/hpc-quick-start.git'
    repo = 'git@gitlab.pmcs2i.ec-lyon.fr:PMCS2I/hpc-quick-start.git'
    build_system = 'SingleSource'
    sourcesdir = 'src/hpc-quick-start.git/pi_integral/src'
    sourcepath = 'pi.c'
    # build_locally = False

    executable = './pi.exe'
    intervalles = parameter([1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
    # intervalles = parameter([1000, 10000])
    num_nodes = variable(int, value=1)
    time_limit = '2m'

    @run_before('compile')
    def setup_build(self):
#         self.prebuild_cmds = [
#             f'git clone --depth=1 {self.repo} '
#             f';cd hpc-quick-start ;git log --pretty=oneline ;cd ..',
#         ]
        self.build_system.ldflags += ['-lm']

    @run_before('run')
    def setup_job(self):
        # self.job.options = [f'--nodes=1']
        self.executable_opts = [f'{int(self.intervalles)}']
        self.prerun_cmds = [r'echo t0=$(date +%s%N)']  # ns2ms -> *10^-6
        self.postrun_cmds = [r'echo t1=$(date +%s%N)']

    @sanity_function
    def validate_test(self):
        """
        ./pi.exe 10
        Number of intervals = 10
        Estimation of Pi  3.1045183262483182E+00
        Exact value       3.1415926535897931E+00 Error : 3.7074327341474866E-02
        """
        regexes = [
            r'^Number of intervals = \d+',
            r'^Exact value\s+\S+ Error :\s+(\S+)',
            r'^t0=', r'^t1='
        ]
        assert_list = []
        for regex in regexes:
            assert_list.append(
                sn.assert_found(regex, self.stdout, msg=f'found "{regex}"'))

        return sn.all(assert_list)

    @performance_function('ns')
    def sim_elapsed(self):
        regex_t0 = r'^t0=(?P<nsec>\d+)'
        regex_t1 = r'^t1=(?P<nsec>\d+)'
        t0 = sn.extractsingle(regex_t0, self.stdout, 'nsec', int)
        t1 = sn.extractsingle(regex_t1, self.stdout, 'nsec', int)
        return t1 - t0

    @performance_function('')
    def sim_error(self):
        regex = r'^Exact value\s+\S+ Error :\s+(?P<err>\S+)'
        return sn.extractsingle(regex, self.stdout, 'err', float)

#     # def setup_logs(self):
#     @run_before('performance')
#     def set_perf_reference(self):
#         self.uarch = uarch(self.current_partition)
#         ref_sec_per_step = self._ref_sec_per_step.get(
#             self.sph_testcase, {}).get(self.uarch)
#         if ref_sec_per_step is not None:
#             self.reference = {
#                 self.current_partition.fullname: {
#                     'sec_per_step': (ref_sec_per_step, None, 0.15, 's')
#                 }
#             }
