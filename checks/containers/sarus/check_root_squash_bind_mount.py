import os
import tempfile

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.osext as osext


@rfm.simple_test
class SarusRootSquashBindMount(rfm.RunOnlyRegressionTest):
    valid_systems = ['dom:gpu', 'dom:mc', 'daint:gpu', 'daint:mc',
                     'eiger:mc', 'pilatus:mc']
    valid_prog_environs = ['builtin']
    sourcesdir = None
    container_platform = 'Sarus'
    num_tasks = 1
    num_tasks_per_node = 1
    maintainers = ['amadonna', 'taliaga']
    tags = {'production'}

    @run_after('setup')
    def set_commands_and_executable(self):
        self.container_platform.image = 'alpine'
        self.test_dir = tempfile.mkdtemp(
            prefix='sarus-root-squash-reframe-test-', dir=os.environ['HOME'])
        self.prerun_cmds = [
            f'echo "CHECK_SUCCESSFUL" > {self.test_dir}/test-file',
            'sarus --version'
        ]
        self.container_platform.mount_points = [
            (self.test_dir, '/reframe-test')
        ]
        self.container_platform.command = 'cat /reframe-test/test-file'

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'CHECK_SUCCESSFUL', self.stdout)

    @run_after('cleanup')
    def rm_testdir(self):
        osext.rmtree(self.test_dir)
