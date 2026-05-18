import os
import reframe as rfm
import reframe.utility.sanity as sn


class tuto_base(rfm.RegressionTest):
    descr = "Compile, execute et analyse le code pi_integral"
    maintainers = ['pmcs2i', '@jgphpc']
    build_system = 'SingleSource'

    executable = './pi.exe'
    time_limit = '1m'

    @run_before('compile')
    def setup_build(self):
        self.prebuild_cmds = ['module list']
        self.build_system.ldflags += ['-lm']

    @sanity_function
    def validate_test(self):
        """
        ./pi.exe 10
        Number of intervals = 10
        Estimation of Pi  3.1045183262483182E+00
        Exact value       3.1415926535897931E+00 Error : 3.7074327341474866E-02
        """
        regex1 = r'^Number of intervals = \d+'
        regex2 = r'^Exact value\s+\S+ Error :\s+(\S+)'
        return sn.all([
            sn.assert_found(regex1, self.stdout),
            sn.assert_found(regex1, self.stdout)
        ])

    @performance_function('')
    def sim_error(self):
        regex = r'^Exact value\s+\S+ Error :\s+(?P<err>\S+)'
        return sn.extractsingle(regex, self.stdout, 'err', float)


@rfm.simple_test
class tuto_serial(tuto_base):
    valid_systems = ['+scontrol']
    valid_prog_environs = ['+serial']
    intervalles = parameter([10])
    sourcesdir = 'src/hpc-quick-start.git/pi_integral/src'
    sourcepath = 'pi.c'
    # build_locally = False

    @run_before('run')
    def setup_executable_opts(self):
        self.executable_opts = [f'{int(self.intervalles)}']


@rfm.simple_test
class tuto_mpi(tuto_base):
    valid_systems = ['+scontrol']
    valid_prog_environs = ['+mpi']
    sourcesdir = 'src/hpc-quick-start.git/pi_integral/src_mpi'
    sourcepath = 'pi.c'
    build_locally = False
    flexible = variable(bool, value=False)
    num_tasks_per_node = 4

    @run_before('run')
    def setup_job(self):
        if self.flexible:
            self.num_tasks = 0
        else:
            self.num_tasks = self.num_tasks_per_node
