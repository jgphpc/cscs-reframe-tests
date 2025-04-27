# Copyright Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause
import os

import reframe as rfm
import reframe.utility.sanity as sn
# import uenv


# ref_nb_gflops = {
#     'a100': {'nb_gflops': (9746*2*0.85, -0.1, None, 'GFlops')},
#     # https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/
#     # + nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf (FP64 Tensor Core)
#     'gh200': {'nb_gflops': (42700, -0.1, None, 'GFlops')},
#     # from https://confluence.cscs.ch/display/SCISWDEV/Feeds+and+Speeds
# }


# {{{ DummySPH_Uenv_Ascent
@rfm.simple_test
class DummySPH_Uenv_Ascent(rfm.RegressionTest):
    """
    UENV=insitu_ascent/0.9.3:1730216054 ./R \
    -c cscs-reframe-tests.git/checks/apps/dummysph/dummysph.py \
    --system santis:normal -l
    """
    valid_systems = ['+remote']
    valid_prog_environs = ['+uenv +ascent -cuda', '+uenv +ascent +cuda']
    #
    version = variable(str, value='build')  # main
    aos = parameter(['ON', 'OFF'])
    # ON = struct tipsy (AOS) / OFF = std::vector (SOA)
    # tipsy = variable(str, value='OFF')
    # tipsy_file = variable(str, value='hr8799_bol_bd1.017300')
    h5part = variable(str, value='OFF')
    datadump = variable(str, value='OFF')
    fp64 = parameter(['OFF', 'ON']) # OFF=<float>, ON=<double>
    num_gpus = variable(int, value=4)
    sourcesdir = 'https://github.com/jgphpc/DummySPH.git'
    # sourcesdir = 'https://github.com/jfavre/DummySPH.git'
    # ascentdir = variable(str, value='/user-environment/env/default/lib/cmake')
    ascentdir = variable(str, value='/capstor/scratch/cscs/jfavre/Ascent-cuda/install/ascent-checkout/lib/cmake')
    build_system = 'CMake'
    build_locally = False
    executable = 'hostname'
    exe = '../src/bin/dummysph_ascent'

    @run_before('compile')
    def set_build_system(self):
        self.build_system.max_concurrency = 6
        self.build_system.srcdir = 'src'
        self.prebuild_cmds += [
            f"git checkout {self.version}",
            f"touch STRIDED_SCALARS_{self.aos}",
            f"touch SPH_DOUBLE_{self.fp64}",
            "cd src"
        ]
        # TODO: --depth=1
        self.build_system.config_opts = [
            # '-DCMAKE_C_COMPILER=mpicc',
            # '-DCMAKE_CXX_COMPILER=mpicxx',
            '-DCMAKE_BUILD_TYPE=Debug',
            # '-DCMAKE_BUILD_TYPE=Release',
            f'-DSTRIDED_SCALARS={self.aos}',
            # f'-DCAN_LOAD_TIPSY={self.tipsy}',
            f'-DCAN_LOAD_H5Part={self.h5part}',
            f'-DCAN_DATADUMP={self.datadump}',
            f'-DSPH_DOUBLE={self.fp64}',
            '-DINSITU=Ascent',
            f'-DAscent_DIR={self.ascentdir}',
            # '-DAscent_DIR=/user-environment/env/default/lib/cmake',
            # '-DAscent_DIR=/capstor/scratch/cscs/jfavre/Ascent-cuda/install/ascent-checkout/lib/cmake',
        ]

    @run_before('run')
    def set_executable_tests(self):
        self.job.options = [f'--nodes=1']
        in_dir = '/capstor/store/cscs/userlab/vampir'
        out_dir = '/dev/shm/$USER'
        self.rpt = 'rpt'

        self.prerun_cmds += [
            f'mkdir -p {out_dir}',
            # separate dirs to avoid overwriting simple_trigger_actions.yaml:
            f'(mkdir -p 0 ;cd 0 ;'
            f'CUDA_VISIBLE_DEVICES=0 {self.exe} --rendering {out_dir}/image-t'
            f' &> {self.rpt} ;cd ..) &',
            #
            f'(mkdir -p 1 ;cd 1 ;'
            f'CUDA_VISIBLE_DEVICES=1 {self.exe} --thresholding {out_dir}/threshold-t'
            f' &> {self.rpt} ;cd ..) &',
            #
            f'(mkdir -p 2 ;cd 2 ;'
            f'CUDA_VISIBLE_DEVICES=2 {self.exe} --compositing {out_dir}/composite-t'
            f' &> {self.rpt} ;cd ..) &',
            #
            f'(mkdir -p 3 ;cd 3 ;'
            f'CUDA_VISIBLE_DEVICES=3 {self.exe} --histsampling {out_dir}/histsampl-t'
            f' &> {self.rpt} ;cd ..) &',
            'wait',
        ]

        self.postrun_cmds += [
            f'mv {out_dir}/* .',
        ]

#del        self.postrun_cmds += [
#del            f'file 0/datasets/image.00003.png >> 0/{self.rpt}',
#del            f'file 1/datasets/s1_03.png >> 1/{self.rpt}',
#del            f'file 2/pl_geometric_clip.cycle_000002.root >> 2/{self.rpt}',
#del            f'file 3/datasets/pl_geometric_clip.cycle_000000.root >> 3/{self.rpt}' if self.aos == 'ON' else None,
#del        ]
        self.extra_resources = {'gres': {'gres': f'gpu:{self.num_gpus}'}}

    @sanity_function
    def validate_test(self):
        """
# 0/datasets/image.00003.png: PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced
# 1/datasets/s1_03.png: PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced
# 2/pl_geometric_clip.cycle_000002.root: Hierarchical Data Format (version 5) data
# 3/datasets/pl_geometric_clip.cycle_000000.root: Hierarchical Data Format (version 5) data
        """
        regex = 'AscentFinalize'
        regex_png = 'PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced'
        regex_hdf = 'Hierarchical Data Format (version 5) data'
        #
        rpt_0 = f'0/{self.rpt}'
        rpt_1 = f'1/{self.rpt}'
        rpt_2 = f'2/{self.rpt}'
        rpt_3 = f'3/{self.rpt}'
        #
        return sn.all([
            sn.assert_found(regex, rpt_0, msg=f'sanity failed in {rpt_0}'),
            sn.assert_found(regex, rpt_1, msg=f'sanity failed in {rpt_1}'),
            sn.assert_found(regex, rpt_2, msg=f'sanity failed in {rpt_2}'),
            sn.assert_found(regex, rpt_3, msg=f'sanity failed in {rpt_3}') if self.aos == 'ON' else None,
            #
            sn.assert_found(regex_png, rpt_0, msg=f'sanity failed in {rpt_0} png'),
            sn.assert_found(regex_png, rpt_1, msg=f'sanity failed in {rpt_1} png'),
            sn.assert_found(regex_hdf, rpt_2, msg=f'sanity failed in {rpt_2} hdf'),
            sn.assert_found(regex_hdf, rpt_3, msg=f'sanity failed in {rpt_3} hdf') if self.aos == 'ON' else None,
        ])
        # num_gpus_res = sn.count(sn.extractall(regex, self.stdout, 1, float))
        # return sn.assert_eq(self.num_gpus, num_gpus_res)

#     @performance_function('GFlops')
#     def nb_gflops(self):
#         regex = r'nid\d+:gpu.*\s+(\d+\.\d+)\s+GFlops,'
#         return sn.min(sn.extractall(regex, self.stdout, 1, float))
#         # TODO: report power cap (nodelist is already in json)
# 
#     @run_before('performance')
#     def validate_perf(self):
#         self.uarch = uenv.uarch(self.current_partition)
#         if (
#             self.uarch is not None and
#             self.uarch in ref_nb_gflops
#         ):
#             self.reference = {
#                 self.current_partition.fullname: ref_nb_gflops[self.uarch]
#             }
#}}}


# {{{ DummySPH_Uenv_VTKm
@rfm.simple_test
class DummySPH_Uenv_VTKm(rfm.RegressionTest):
    """
    UENV=insitu_ascent/develop-nocuda:1730216486 ~/R \
    -c cscs-reframe-tests.git/checks/apps/dummysph/dummysph.py \
    -n DummySPH_Uenv_VTKm \
    -r \
    --system santis:normal -J p=debug
    """
    valid_systems = ['+remote']
    #ok: valid_prog_environs = ['+uenv +ascent -cuda']
    valid_prog_environs = ['+uenv +ascent -cuda', '+uenv +ascent +cuda']
    #
    version = variable(str, value='main')
    aos = parameter(['OFF', 'ON'])
    # ON = struct tipsy (AOS) / OFF = std::vector (SOA)
    tipsy = variable(str, value='ON')
    tipsy_file = variable(str, value='hr8799_bol_bd1.017300')
    h5part = variable(str, value='ON')
    datadump = variable(str, value='OFF')
    fp64 = parameter(['OFF', 'ON']) # OFF=<float>, ON=<double>
    num_gpus = variable(int, value=4)
    sourcesdir = 'https://github.com/jfavre/DummySPH.git'
    build_system = 'CMake'
    build_locally = False
    executable = 'hostname'
    exe = './src/bin/dummysph_vtkm'

    @run_before('compile')
    def set_build_system(self):
        self.build_system.max_concurrency = 6
        self.build_system.srcdir = 'src'
        self.prebuild_cmds += [
            f"git checkout {self.version}",
            f"touch STRIDED_SCALARS_{self.aos}",
            f"touch SPH_DOUBLE_{self.fp64}",
            "cd src",
            'ln -s Driver.cxx Driver.cu'
        ]
        self.env_vars = {
            'CPATH': '/user-environment/env/default/include'
        }
        # TODO: --depth=1
        self.build_system.config_opts = [
            # '-DCMAKE_C_COMPILER=mpicc',
            # '-DCMAKE_CXX_COMPILER=mpicxx',
            '-DCMAKE_BUILD_TYPE=Debug',
            # '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_CUDA_ARCHITECTURES=90',
            f'-DSTRIDED_SCALARS={self.aos}',
            f'-DCAN_LOAD_TIPSY={self.tipsy}',
            f'-DCAN_LOAD_H5Part={self.h5part}',
            f'-DCAN_DATADUMP={self.datadump}',
            f'-DSPH_DOUBLE={self.fp64}',
            '-DINSITU=VTK-m',
            '-DVTKm_DIR=`find /user-environment/ -name "vtkm-2.2" |grep -m1 cmake`',
            # '-DVTKm_DIR=/user-environment/ParaView-5.13/lib64/cmake/paraview-5.13/vtk/vtkm',
            #OK: '-DVTKm_DIR=/capstor/scratch/cscs/jfavre/Ascent-cuda/install/vtk-m-v2.2.0/lib/cmake/vtkm-2.2',
            # '-DCMAKE_CXX_FLAGS="-DVTKM_NO_ERROR_ON_MIXED_CUDA_CXX_TAG=1"',
        ]

    @run_before('run')
    def set_executable_tests(self):
        self.job.options = [f'--nodes=1']
        in_dir = '/capstor/store/cscs/userlab/vampir'
        out_dir = '/dev/shm/$USER'
        tipsy_flag = f'--tipsy {self.tipsy_file}'
        self.rpt = 'rpt'
        self.prerun_cmds += [f'mkdir -p {out_dir}']
        if self.tipsy and self.fp64 == 'OFF':
        # and self.aos == 'ON':
            # TODO: jfrog
            self.prerun_cmds += [
                f'ln -s {in_dir}/{self.tipsy_file} .',
                #
                f'{self.exe} {tipsy_flag} --rendering {out_dir}/image+t'
                f' &> {self.rpt}+rt &',
                f'{self.exe} {tipsy_flag} --thresholding {out_dir}/threshold+t'
                f' &> {self.rpt}+tt &',
                f'{self.exe} {tipsy_flag} --compositing {out_dir}/composite+t'
                f' &> {self.rpt}+ct &',
                f'{self.exe} {tipsy_flag} --histsampling {out_dir}/histsampl+t'
                f' &> {self.rpt}+ht &',
            ]

        self.prerun_cmds += [
            f'{self.exe} --rendering {out_dir}/image-t'
            f' &> {self.rpt}-rt &',
            f'{self.exe} --thresholding {out_dir}/threshold-t'
            f' &> {self.rpt}-tt &',
            f'{self.exe} --compositing {out_dir}/composite-t'
            f' &> {self.rpt}-ct &',
            f'{self.exe} --histsampling {out_dir}/histsampl-t'
            f' &> {self.rpt}-ht &',
            'wait',
        ]

        self.postrun_cmds += [
            f'mv {out_dir}/* .',
        ]
# #             f'file 0/datasets/image.00003.png >> 0/{self.rpt}',
# #             f'file 1/datasets/s1_03.png >> 1/{self.rpt}',
# #             f'file 2/pl_geometric_clip.cycle_000002.root >> 2/{self.rpt}',
#             f'file /dev/shm/insitu.0001.png >> 3/{self.rpt}' if self.aos == 'ON' else None,
#             # TODO: clean /dev/shm
#         ]
#         self.extra_resources = {
#             'gres': {'gres': f'gpu:{self.num_gpus}'}
#         }
        self.extra_resources = {'gres': {'gres': f'gpu:{self.num_gpus}'}}

#     @run_after('init')
#     def skip_on_purpose(self):
#         self.skip_if(self.aos == 'ON' and self.fp64 == 'ON',
#                      f'Not implemented for AOS and <double>')

    @sanity_function
    def validate_test(self):
        """
# 0/datasets/image.00003.png: PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced
# 1/datasets/s1_03.png: PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced
# 2/pl_geometric_clip.cycle_000002.root: Hierarchical Data Format (version 5) data
# 3/datasets/pl_geometric_clip.cycle_000000.root: Hierarchical Data Format (version 5) data
        """
        regex = 'AscentFinalize'
        regex_png = 'PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced'
        regex_hdf = 'Hierarchical Data Format (version 5) data'
        #
        rpt_0 = f'0/{self.rpt}'
        rpt_1 = f'1/{self.rpt}'
        rpt_2 = f'2/{self.rpt}'
        rpt_3 = f'3/{self.rpt}'
        #
        return sn.all([
#             sn.assert_found(regex, rpt_0, msg=f'sanity failed in {rpt_0}'),
#             sn.assert_found(regex, rpt_1, msg=f'sanity failed in {rpt_1}'),
#             sn.assert_found(regex, rpt_2, msg=f'sanity failed in {rpt_2}'),
            sn.assert_found(regex, rpt_3, msg=f'sanity failed in {rpt_3}') if self.aos == 'ON' else None,
            #
#             sn.assert_found(regex_png, rpt_0, msg=f'sanity failed in {rpt_0} png'),
#             sn.assert_found(regex_png, rpt_1, msg=f'sanity failed in {rpt_1} png'),
#             sn.assert_found(regex_hdf, rpt_2, msg=f'sanity failed in {rpt_2} hdf'),
            sn.assert_found(regex_png, rpt_3, msg=f'sanity failed in {rpt_3} hdf') if self.aos == 'ON' else None,
        ])
        # num_gpus_res = sn.count(sn.extractall(regex, self.stdout, 1, float))
        # return sn.assert_eq(self.num_gpus, num_gpus_res)

#     @performance_function('GFlops')
#     def nb_gflops(self):
#         regex = r'nid\d+:gpu.*\s+(\d+\.\d+)\s+GFlops,'
#         return sn.min(sn.extractall(regex, self.stdout, 1, float))
#         # TODO: report power cap (nodelist is already in json)
# 
#     @run_before('performance')
#     def validate_perf(self):
#         self.uarch = uenv.uarch(self.current_partition)
#         if (
#             self.uarch is not None and
#             self.uarch in ref_nb_gflops
#         ):
#             self.reference = {
#                 self.current_partition.fullname: ref_nb_gflops[self.uarch]
#             }
#}}}


# {{{ CompileOnly
@rfm.simple_test
class DummySPH_Uenv_Build(rfm.CompileOnlyRegressionTest):
    """
    ./R -c cscs-reframe-tests.git/checks/apps/dummysph/dummysph.py -n DummySPH_Uenv_Build -r --system santis:login
    """
    valid_systems = ['santis']
    #ok: valid_prog_environs = ['+uenv +ascent -cuda']
    #valid_prog_environs = ['+uenv +ascent -cuda', '+uenv +ascent +cuda']
    valid_prog_environs = ['*']
    #
    # sourcesdir = 'https://github.com/jfavre/DummySPH.git'
    sourcesdir = 'https://github.com/jgphpc/DummySPH.git'
    version = variable(str, value='build')  # main
    insitu = parameter(['ascent'])
    # insitu = parameter(['vtkm', 'ascent'])
    aos = parameter(['OFF', 'ON'])
    # ON = struct tipsy (AOS) / OFF = std::vector (SOA)
    tipsy = variable(str, value='ON')
    tipsy_file = variable(str, value='hr8799_bol_bd1.017300')
    h5part_file = variable(str, value='/capstor/scratch/cscs/piccinal/santis/sk/dump_wind-shock.h5')
    h5part = variable(str, value='ON')
    datadump = variable(str, value='OFF')
    fp64 = parameter(['OFF', 'ON']) # OFF=<float>, ON=<double>
    num_gpus = variable(int, value=4)
    uenv_sqfs = variable(str, value='insitu_ascent/develop:1753161369')
    uenv_view = variable(str, value='default')
    build_system = 'CMake'
    # build_locally = False
    # executable = 'hostname'
    # exe = './src/bin/dummysph_vtkm'
    ascentdir = variable(str, value='/user-environment/env/default/lib/cmake')
    # ascentdir = variable(str, value='/capstor/scratch/cscs/jfavre/Ascent-cuda/install/ascent-checkout/lib/cmake')

    @run_before('compile')
    def set_build_system(self):
        cmake_insitu = 'VTK-m' if self.insitu == 'vtkm' else 'Ascent'
        self.executable = './dummysph_vtkm' if self.insitu == 'vtkm' else './dummysph_ascent'
        self.build_system.max_concurrency = 6
        self.build_system.srcdir = 'src'
        self.prebuild_cmds += [
            f'git checkout {self.version}',
            f'touch STRIDED_SCALARS_{self.aos}',
            f'touch SPH_DOUBLE_{self.fp64}',
            'cd src', 'ln -s Driver.cxx Driver.cu', 'cd ..',
        ]
        self.env_vars = {
            'CPATH': '/user-environment/env/default/include',
            # 'LD_LIBRARY_PATH': '/user-environment/env/default/lib:$LD_LIBRARY_PATH',
            # 'CMAKE_PREFIX_PATH': '/user-environment/linux-*/gcc-*/hdf5-*/cmake:$CMAKE_PREFIX_PATH'
            # 'CMAKE_PREFIX_PATH': '`find /user-environment/ -name cmake |grep hdf5 |grep -v spack `:$CMAKE_PREFIX_PATH'
        }
        # /capstor/scratch/cscs/jfavre/SPH-EXA/Ascent/datasets/
        # convert -pointsize  32 -fill white -weight bold-font -annotate +0+1040 'T = 0.0031'  density301.00250.png ldensity301.00250.png
        # TODO: --depth=1
        self.build_system.config_opts = [
            '-DCMAKE_C_COMPILER=mpicc',
            '-DCMAKE_CXX_COMPILER=mpicxx', # needed
            # '-DCMAKE_CUDA_COMPILER=nvcc',
            '-DCMAKE_BUILD_TYPE=Debug',
            # '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_CUDA_ARCHITECTURES=90',
            f'-DSTRIDED_SCALARS={self.aos}',
            f'-DCAN_LOAD_TIPSY={self.tipsy}',
            f'-DCAN_LOAD_H5Part={self.h5part}',
            f'-DCAN_DATADUMP={self.datadump}',
            f'-DSPH_DOUBLE={self.fp64}',
            f'-DINSITU={cmake_insitu}',
            f'-DVTKm_DIR=`find /user-environment/ -name vtkm-2.2 |grep -m1 cmake`',
            f'-DAscent_DIR={self.ascentdir}',
            # '-DVTKm_DIR=/user-environment/ParaView-5.13/lib64/cmake/paraview-5.13/vtk/vtkm',
            #OK: '-DVTKm_DIR=/capstor/scratch/cscs/jfavre/Ascent-cuda/install/vtk-m-v2.2.0/lib/cmake/vtkm-2.2',
            # '-DCMAKE_CXX_FLAGS="-DVTKM_NO_ERROR_ON_MIXED_CUDA_CXX_TAG=1"',
        ]
        cmake_1 = ",".join(self.build_system.config_opts).replace(",", " ")
        tipsy_flag = f'--tipsy {self.tipsy_file}'
        h5part_flag = f'--h5part {self.h5part_file}'
        in_dir = '/capstor/store/cscs/userlab/vampir'
        out_dir = f'/dev/shm/$USER/INSITU_{self.insitu}_STRIDED_SCALARS_{self.aos}-SPH_DOUBLE_{self.fp64}'
        self.prebuild_cmds += [
            f'ln -fs $PWD ../INSITU_{self.insitu}_STRIDED_SCALARS_{self.aos}-SPH_DOUBLE_{self.fp64}',
            f"echo 'export CMAKE_PREFIX_PATH=`find /user-environment/ -name cmake |grep hdf5 |grep -v spack`:$CMAKE_PREFIX_PATH' > 0.sh",
            f"echo cmake '{cmake_1}' -B build -S src '2>&1' >> 0.sh",
            f"echo cmake --build build -v '2>&1' >> 0.sh",
            f'chmod 700 ./0.sh',
            f'uenv run --view={self.uenv_view} {self.uenv_sqfs} -- ./0.sh',
            #
            f'ln -s build/bin/dummysph_*',
            ## f'ldd dummysph_* |grep found',
            f'ln -s {in_dir}/{self.tipsy_file} .',
            f'mkdir -p {out_dir}',
            #
            # f'echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/user-environment/env/default/lib" > 1.sh',
            f'echo "./dummysph_vtkm {tipsy_flag} --rendering {out_dir}/image+t" > 1.sh' if self.insitu == 'vtkm' else f'echo "./dummysph_ascent {h5part_flag} --rendering {out_dir}/image+t" > 1.sh',
            f'chmod 700 ./1.sh',
            f'uenv run --view={self.uenv_view} {self.uenv_sqfs} -- ./1.sh',
            f'mv {out_dir}/image+t* .',
            #
            'exit 0',
# uenv run /capstor/scratch/cscs/piccinal/.uenv-images/images/f710fb44b74e96d501e91ae2fa7f52d2c2c95c29db036683fab5e9f2e15f8bb2/store.squashfs -v default -- ./rfm_build.sh
        ]

#del     @run_before('run')
#del     def set_executable_tests(self):
#del         self.job.options = [f'--nodes=1']
#del         in_dir = '/capstor/store/cscs/userlab/vampir'
#del         out_dir = '/dev/shm/$USER'
#del         tipsy_flag = f'--tipsy {self.tipsy_file}'
#del         self.rpt = 'rpt'
#del         self.prerun_cmds += [f'mkdir -p {out_dir}']
#del         if self.tipsy and self.fp64 == 'OFF':
#del         # and self.aos == 'ON':
#del             # TODO: jfrog
#del             self.prerun_cmds += [
#del                 f'ln -s {in_dir}/{self.tipsy_file} .',
#del                 #
#del                 f'{self.exe} {tipsy_flag} --rendering {out_dir}/image+t'
#del                 f' &> {self.rpt}+rt &',
#del                 f'{self.exe} {tipsy_flag} --thresholding {out_dir}/threshold+t'
#del                 f' &> {self.rpt}+tt &',
#del                 f'{self.exe} {tipsy_flag} --compositing {out_dir}/composite+t'
#del                 f' &> {self.rpt}+ct &',
#del                 f'{self.exe} {tipsy_flag} --histsampling {out_dir}/histsampl+t'
#del                 f' &> {self.rpt}+ht &',
#del             ]
#del 
#del         self.prerun_cmds += [
#del             f'{self.exe} --rendering {out_dir}/image-t'
#del             f' &> {self.rpt}-rt &',
#del             f'{self.exe} --thresholding {out_dir}/threshold-t'
#del             f' &> {self.rpt}-tt &',
#del             f'{self.exe} --compositing {out_dir}/composite-t'
#del             f' &> {self.rpt}-ct &',
#del             f'{self.exe} --histsampling {out_dir}/histsampl-t'
#del             f' &> {self.rpt}-ht &',
#del             'wait',
#del         ]
#del 
#del         self.postrun_cmds += [
#del             f'mv {out_dir}/* .',
#del         ]
#del # #             f'file 0/datasets/image.00003.png >> 0/{self.rpt}',
#del # #             f'file 1/datasets/s1_03.png >> 1/{self.rpt}',
#del # #             f'file 2/pl_geometric_clip.cycle_000002.root >> 2/{self.rpt}',
#del #             f'file /dev/shm/insitu.0001.png >> 3/{self.rpt}' if self.aos == 'ON' else None,
#del #             # TODO: clean /dev/shm
#del #         ]
#del #         self.extra_resources = {
#del #             'gres': {'gres': f'gpu:{self.num_gpus}'}
#del #         }
#del         self.extra_resources = {'gres': {'gres': f'gpu:{self.num_gpus}'}}
#del 
#del #     @run_after('init')
#del #     def skip_on_purpose(self):
#del #         self.skip_if(self.aos == 'ON' and self.fp64 == 'ON',
#del #                      f'Not implemented for AOS and <double>')
#del 
    @sanity_function
    def validate_build(self):
        regex = '^\[100%\] Linking CXX executable bin/dummysph'
        #regex = 'AscentFinalize'
        #regex_png = 'PNG image data, 1024 x 1024, 8-bit/color RGB, non-interlaced'
        #regex_hdf = 'Hierarchical Data Format (version 5) data'
        #
        #rpt_0 = f'0/{self.rpt}'
        #rpt_1 = f'1/{self.rpt}'
        #rpt_2 = f'2/{self.rpt}'
        #rpt_3 = f'3/{self.rpt}'
        #
        return sn.all([
            sn.assert_found(regex, self.stdout),
#             sn.assert_found(regex, rpt_0, msg=f'sanity failed in {rpt_0}'),
#             sn.assert_found(regex, rpt_1, msg=f'sanity failed in {rpt_1}'),
#             sn.assert_found(regex, rpt_2, msg=f'sanity failed in {rpt_2}'),
#             sn.assert_found(regex, rpt_3, msg=f'sanity failed in {rpt_3}') if self.aos == 'ON' else None,
            #
#             sn.assert_found(regex_png, rpt_0, msg=f'sanity failed in {rpt_0} png'),
#             sn.assert_found(regex_png, rpt_1, msg=f'sanity failed in {rpt_1} png'),
#             sn.assert_found(regex_hdf, rpt_2, msg=f'sanity failed in {rpt_2} hdf'),
#             sn.assert_found(regex_png, rpt_3, msg=f'sanity failed in {rpt_3} hdf') if self.aos == 'ON' else None,
        ])
        # num_gpus_res = sn.count(sn.extractall(regex, self.stdout, 1, float))
        # return sn.assert_eq(self.num_gpus, num_gpus_res)

#     @performance_function('GFlops')
#     def nb_gflops(self):
#         regex = r'nid\d+:gpu.*\s+(\d+\.\d+)\s+GFlops,'
#         return sn.min(sn.extractall(regex, self.stdout, 1, float))
#         # TODO: report power cap (nodelist is already in json)
# 
#     @run_before('performance')
#     def validate_perf(self):
#         self.uarch = uenv.uarch(self.current_partition)
#         if (
#             self.uarch is not None and
#             self.uarch in ref_nb_gflops
#         ):
#             self.reference = {
#                 self.current_partition.fullname: ref_nb_gflops[self.uarch]
#             }
#}}}
