import os
import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class memory(rfm.RunOnlyRegressionTest):
    descr = "Valide la memoire disponible du CPU"
    maintainers = ['pmcs2i', '@jgphpc']
    valid_systems = ['+cpu']
    valid_prog_environs = ['builtin']
    time_limit = '1m'
    sourcesdir = 'src/mem'
    executable = './mem.sh'
    regex = r'\S+ \/ MemAvailable:(?P<mem_avail>\S+)kB \/'

    @sanity_function
    def validate_test(self):
        """
        Typical output: haswell-t16-30 / MemAvailable:64149212kB /
        """
        return sn.assert_found(self.regex, self.stdout)

    @performance_function('kB')
    def mem_avail(self):
        return sn.extractsingle(self.regex, self.stdout, 'mem_avail', float)

    @run_before('performance')
    def set_perf_reference(self):
        """
        https://reframe-hpc.readthedocs.io/en/latest/regression_test_api.html
        -> "The performance reference values for this test"
        """
        # haswell t16:64, f20:270, x20:384, x44:512
        # cascade t32:190, f32:384, x32:768
        # skylake t32:190, f32:384
        # genoa   t64:384
        ref_low = -0.05  # -5%
        self.reference = {
            # self.current_partition.fullname: {...}
            'newton:haswell-t16': {'mem_avail_GB': (64, ref_low, None, 'GB')},
            'newton:haswell-f20': {'mem_avail_GB': (270, ref_low, None, 'GB')},
            'newton:haswell-x20': {'mem_avail_GB': (384, -0.04, None, 'GB')},
            'newton:haswell-x44': {'mem_avail_GB': (512, ref_low, None, 'GB')},
            'newton:cascade-t32': {'mem_avail_GB': (190, ref_low, None, 'GB')},
            'newton:cascade-f32': {'mem_avail_GB': (384, ref_low, None, 'GB')},
            'newton:cascade-x32': {'mem_avail_GB': (768, ref_low, None, 'GB')},
            'newton:skylake-t32': {'mem_avail_GB': (190, ref_low, None, 'GB')},
            'newton:skylake-f32': {'mem_avail_GB': (384, ref_low, None, 'GB')},
            'newton:genoa': {'mem_avail_GB': (384, ref_low, None, 'GB')},
        }
        # TODO: 'extras': {'cn_memory': 64},

    @performance_function('GB')
    def mem_avail_GB(self):
        return sn.extractsingle(self.regex, self.stdout, 'mem_avail',
                                conv=lambda x: round(int(x) / 1024**2, 3))

#     @performance_function('MB')
#     def mem_real(self):
#         """
# jq .runs[0].testcases[0].perfvalues latest.json |jq keys
# [
#   "pilatus:normal:mem_real",
#   "pilatus:normal:mem_total",
#   "pilatus:normal:sim_elapsed"
# ]
# 
# jq -r '.runs[].testcases[] | [
#     .job_nodelist[0],
#     (.perfvalues | to_entries[] | select(.key | test("^.*:.*:mem_total$")) | .value[0]),
#     .partition, .environ ] | @csv ' latest.json
# 
# "nid001036",263242712,"normal","builtin"
# "nid001131",263242644,"normal","builtin"
# "nid001129",263242660,"normal","builtin"
#         """
#         regex = r'\S+ \/ MemTotal:(?P<mem_tot>\S+)kB \/ MemAvailable:(?P<mem_avail>\S+)kB \/ RealMemory=(?P<mem_real>\S+)'
#         return sn.extractsingle(regex, self.stdout, 'mem_real', int)
