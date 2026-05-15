import os
import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class memory(rfm.RunOnlyRegressionTest):
    descr = "Reporte la memoire du noeud"
    maintainers = ['pmcs2i', '@jgphpc']
    valid_systems = ['+scontrol']
    valid_prog_environs = ['*']
    # build_system = 'SingleSource'
    sourcesdir = 'src/mem'

    executable = './mem.sh'
    # intervalles = parameter([1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
    num_nodes = variable(int, value=1)
    time_limit = '1m'

    @run_before('run')
    def setup_job(self):
        # self.job.options = [f'--nodes=1']
        # self.executable_opts = [f'{int(self.intervalles)}']
        self.prerun_cmds = [r'echo t0=$(date +%s%N)']  # ns2ms -> *10^-6
        self.postrun_cmds = [r'echo t1=$(date +%s%N)']

    @sanity_function
    def validate_test(self):
        """
        nid001034 / MemTotal:263242652kB / MemAvailable:698099288kB / RealMemory=241746 AllocMem=241746 FreeMem=239037 /
        haswell-t16-49 / MemTotal:65710212kB / RealMemory=64000 AllocMem=4000 FreeMem=62899 /
            MemTotal: Total usable RAM i.e., physical RAM minus a few reserved
                      bits and the kernel binary code (man 5 proc, /proc/meminfo)
            RealMemory: The total memory, in MB, on the node (man scontrol)

MemFree:        50333592 kB = LowFree+HighFree
MemAvailable:   698088724 kB estimate of how much memory is available for starting new applications, without swapping.
        """
        regexes = [
            r'\S+ \/ MemTotal:(?P<mem_tot>\S+)kB \/ MemAvailable:(?P<mem_avail>\S+)kB \/ RealMemory=(?P<mem_real>\S+)',
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

    @performance_function('kB')
    def mem_total(self):
        regex = r'\S+ \/ MemTotal:(?P<mem_tot>\S+)kB \/ MemAvailable:(?P<mem_avail>\S+)kB \/ RealMemory=(?P<mem_real>\S+)'
        return sn.extractsingle(regex, self.stdout, 'mem_tot', int)

    @performance_function('kB')
    def mem_avail(self):
        regex = r'\S+ \/ MemTotal:(?P<mem_tot>\S+)kB \/ MemAvailable:(?P<mem_avail>\S+)kB \/ RealMemory=(?P<mem_real>\S+)'
        return sn.extractsingle(regex, self.stdout, 'mem_avail', int)

    @performance_function('MB')
    def mem_real(self):
        """
jq .runs[0].testcases[0].perfvalues latest.json |jq keys
[
  "pilatus:normal:mem_real",
  "pilatus:normal:mem_total",
  "pilatus:normal:sim_elapsed"
]

jq -r '.runs[].testcases[] | [
    .job_nodelist[0],
    (.perfvalues | to_entries[] | select(.key | test("^.*:.*:mem_total$")) | .value[0]),
    .partition, .environ ] | @csv ' latest.json

"nid001036",263242712,"normal","builtin"
"nid001131",263242644,"normal","builtin"
"nid001129",263242660,"normal","builtin"
        """
        regex = r'\S+ \/ MemTotal:(?P<mem_tot>\S+)kB \/ MemAvailable:(?P<mem_avail>\S+)kB \/ RealMemory=(?P<mem_real>\S+)'
        return sn.extractsingle(regex, self.stdout, 'mem_real', int)


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
