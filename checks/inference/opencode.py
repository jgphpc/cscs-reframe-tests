import os

import reframe as rfm
import reframe.utility.sanity as sn

urls = {
    'prod': 'https://api.inference.cscs.ch/v1',
    'tds': 'https://ai-gateway.forno-tds.tds.cscs.ch/v1'
}


@rfm.simple_test
class inference_api(rfm.RunOnlyRegressionTest):
    valid_systems = ['*']
    valid_prog_environs = ['*']
    executable = './curl.sh'
    time_limit = '10m'
    target = parameter(['prod', 'tds'], type=str, loggable=True)

    @run_before('run')
    def set_runtime_args(self):
        self.executable_opts = [self.target, urls[self.target]]
        # self.postrun_cmds = ['']

    @sanity_function
    def set_sanity(self):
        return sn.all([sn.assert_not_found(r'Error', self.stderr)])

#     @performance_function('MB/s')
#     def perf1(self):
#         return sn.extractsingle(r'(\S+)', self.stdout, 1) # , float)
