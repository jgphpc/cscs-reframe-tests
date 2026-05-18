import os
import reframe as rfm
import reframe.utility.sanity as sn


class tuto_base(rfm.RegressionTest):
    descr = "Compile, execute et analyse le code pi_integral"
    maintainers = ['pmcs2i', '@jgphpc']
    # no:sourcesdir = 'git@gitlab.pmcs2i.ec-lyon.fr:PMCS2I/hpc-quick-start.git'
    # repo = 'git@gitlab.pmcs2i.ec-lyon.fr:PMCS2I/hpc-quick-start.git'
    build_system = 'SingleSource'
    # build_locally = False

    executable = './pi.exe'
    # intervalles = parameter([1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
    num_nodes = variable(int, value=1)
    time_limit = '2m'

    @run_before('compile')
    def setup_build(self):
#         self.prebuild_cmds = [
#             f'git clone --depth=1 {self.repo} '
#             f';cd hpc-quick-start ;git log --pretty=oneline ;cd ..',
#         ]
        self.build_system.ldflags += ['-lm']

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
            # r'^t0=', r'^t1='
        ]
        assert_list = []
        for regex in regexes:
            assert_list.append(
                sn.assert_found(regex, self.stdout, msg=f'found "{regex}"'))

        return sn.all(assert_list)

#     @performance_function('ns')
#     def sim_elapsed(self):
#         regex_t0 = r'^t0=(?P<nsec>\d+)'
#         regex_t1 = r'^t1=(?P<nsec>\d+)'
#         t0 = sn.extractsingle(regex_t0, self.stdout, 'nsec', int)
#         t1 = sn.extractsingle(regex_t1, self.stdout, 'nsec', int)
#         return t1 - t0

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
    build_locally = False

    @run_before('run')
    def setup_job(self):
        # self.job.options = [f'--nodes=1']
        self.executable_opts = [f'{int(self.intervalles)}']
        # self.prerun_cmds = [r'echo t0=$(date +%s%N)']  # ns2ms -> *10^-6
        # self.postrun_cmds = [r'echo t1=$(date +%s%N)']



@rfm.simple_test
class tuto_mpi(tuto_base):
    valid_systems = ['+scontrol']
    valid_prog_environs = ['+mpi']
    sourcesdir = 'src/hpc-quick-start.git/pi_integral/src_mpi'
    sourcepath = 'pi.c'
    build_locally = False
    num_tasks = 4


#{{{ mpi README 
# @rfm.simple_test
# class tuto_mpi(rfm.RunOnlyRegressionTest):
# # class tuto_mpi(rfm.RegressionTest):
#     """
#     PARTITION NODES(A/I/O/T)
#     normal*         0/9/4/13
# 
#    --flex-alloc-nodes {all|STATE|NUM}
#                          Set strategy for the flexible node allocation (default: "idle")
#    --flex-alloc-strict   Fail the flexible tests if not enough nodes can be found
# 
#     num_tasks = 0 + num_tasks_per_node = 4 + --flex-alloc-nodes=all  -> ntasks=52 / 13 nodes
#     num_tasks = 0 + num_tasks_per_node = 4 + --flex-alloc-nodes=idle -> ntasks=36 /  9 nodes
#     num_tasks = 0 + num_tasks_per_node = 4                           -> ntasks=36 /  9 nodes (idem)
#     num_tasks = 0 + num_tasks_per_node = 4 + --flex-alloc-nodes=2    -> ntasks=8  /  2 nodes
# 
# # https://code.ornl.gov/olcf/hello_mpi_omp/-/raw/master/hello_mpi_omp.c
# OMP_NUM_THREADS=1 srun --uenv=/capstor/scratch/cscs/piccinal/.uenv-images-x86_64/images/39ed0d2f2aca90d1c86e6300379ce265941544a16162ede41a383c15fb0fea59/store.squashfs --view=oneapi -N2 -n256 -t1 -A `id -gn` ./a.out  > o
# 
# git clone https://github.com/TACC/amask.git amask.git
# OMP_NUM_THREADS=1 srun --uenv=/capstor/scratch/cscs/piccinal/.uenv-images-x86_64/images/39ed0d2f2aca90d1c86e6300379ce265941544a16162ede41a383c15fb0fea59/store.squashfs --view=oneapi -N2 -n256 -t1 -A `id -gn` --hint=nomultithread --cpu-bind=cores /capstor/scratch/cscs/piccinal/pilatus/rfm/DEL/amask.git/src/amask_mpi -vs > oo
# 
# cat ps.sh
# #!/bin/bash
# ps -o pid=,psr= -p $$
# # ps -o pid=,psr=,comm= -p $$
# 
# 
# srun -N1 -n32 -t1 -pskylake lstopo --no-io  --no-caches --output-format ascii
# 
# 
#     """
#     descr = "Compile, execute et analyse le code MPI pi_integral"
#     maintainers = ['pmcs2i', '@jgphpc']
#     valid_systems = ['+uenv']
#     valid_prog_environs = ['+mpi']
#     build_system = 'SingleSource'
#     sourcesdir = 'src/hpc-quick-start.git/pi_integral/src_mpi'
#     sourcepath = 'pi.c'
#     build_locally = False
# 
#     executable = '~/pi.exe'
#     # executable = './pi.exe'
#     # intervalles = parameter([1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
#     # intervalles = parameter([1000, 10000])
#     # num_nodes = variable(int, value=1)
#     num_tasks = 0
#     num_tasks_per_node = 4
#     time_limit = '30s'
# 
#     @run_before('compile')
#     def setup_build(self):
#         self.build_system.ldflags += ['-lm']
# 
# #     @run_before('run')
# #     def setup_job(self):
# #         # self.job.options = [f'--nodes=1']
# #         # self.executable_opts = [f'{int(self.intervalles)}']
# #         self.prerun_cmds = [r'echo t0=$(date +%s%N)']  # ns2ms -> *10^-6
# #         self.postrun_cmds = [r'echo t1=$(date +%s%N)']
# 
#     @sanity_function
#     def validate_test(self):
#         """
#         ./pi.exe 10
#         Number of intervals = 10
#         Estimation of Pi  3.1045183262483182E+00
#         Exact value       3.1415926535897931E+00 Error : 3.7074327341474866E-02
#         """
#         regexes = [
#             r'^Number of intervals = \d+',
#             r'^Exact value\s+\S+ Error :\s+(\S+)',
#             # r'^t0=', r'^t1='
#         ]
#         assert_list = []
#         for regex in regexes:
#             assert_list.append(
#                 sn.assert_found(regex, self.stdout, msg=f'found "{regex}"'))
# 
#         return sn.all(assert_list)
# 
#     @performance_function('')
#     def sim_error(self):
#         regex = r'^Exact value\s+\S+ Error :\s+(?P<err>\S+)'
#         return sn.extractsingle(regex, self.stdout, 'err', float)
#}}}
