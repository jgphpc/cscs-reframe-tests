# https://reframe-hpc.readthedocs.io/en/latest/config_reference.html

import os


site_configuration = {
    # {{{ systems
    'systems': [
        {
            # {{{ newton
            'name': 'newton',
            'descr': 'https://pmcs2i.ec-lyon.fr/documentation/resources/',
            'hostnames': ['prepost-haswell', 'prepost-skylake',
                          'prepost-cascade', 'prepost-genoa'],
            'modules_system': 'tmod4',  # tcl modules
            # max_local_jobs
            # modules
            # env_vars
            # variables
            # prefix
            # stagedir
            # outputdir
            # sched_options
            'resourcesdir': '/store/pmcs2i/',
            'partitions': [
                # {{{ haswell-t16-[01-54] - test:haswell-t16-[01-02,30,32]
                {
                    'name': 'haswell-t16',
                    'descr': 'haswell-t16-[01-54] - test nodes * 064G',
                    'scheduler': 'slurm',
                    # https://reframe-hpc.readthedocs.io/en/latest/config_reference.html#config.systems.partitions.scheduler
                    'launcher': 'mpirun',
                    # 'launcher': 'srun',
                    # https://reframe-hpc.readthedocs.io/en/latest/config_reference.html#config.systems.partitions.launcher
                    'access': ['-p haswell',
                               '-w haswell-t16-[03-29,31,33-54]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel-old'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 64},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ haswell-f20-[01-03]
                {
                    'name': 'haswell-f20',
                    'descr': 'haswell-f20-[01-03] * 270G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p haswell',
                               '-w haswell-f20-[01-03]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel-old'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 270},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ haswell-x20-[01-08]
                {
                    'name': 'haswell-x20',
                    'descr': 'haswell-x20-[01-08] * 384G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p haswell',
                               '-w haswell-x20-[01-08]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel-old'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 384},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ haswell-x44-01
                {
                    'name': 'haswell-x44',
                    'descr': 'haswell-x44-01 * 512G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p haswell',
                               '-w haswell-x44-01'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel-old'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 512},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ haswell
                {
                    'name': 'haswell-all',
                    'descr': 'haswell',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p haswell'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel-old'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 100,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 512},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ haswell-test
                {
                    'name': 'haswell-test',
                    'descr': 'test partition',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p test'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel-old'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 100,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 64},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}

                # {{{ cascade-t32-[01-40]
                {
                    'name': 'cascade-t32',
                    'descr': 'cascade-t32-[01-40] * 190G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p cascade',
                               '-w cascade-t32-[01-40]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/cascade/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 190},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ cascade-f32-[01-08]
                {
                    'name': 'cascade-f32',
                    'descr': 'cascade-f32-[01-08] * 384G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p cascade',
                               '-w cascade-f32-[01-08]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/cascade/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 384},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ cascade-x32-[01-04]
                {
                    'name': 'cascade-x32',
                    'descr': 'cascade-x32-[01-04] * 768G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p cascade',
                               '-w cascade-x32-[01-04]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/cascade/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 768},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ cascade
                {
                    'name': 'cascade-all',
                    'descr': 'cascade',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p cascade'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/cascade/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 768},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}

                # {{{ skylake-t32-[01-14]
                {
                    'name': 'skylake-t32',
                    'descr': 'skylake-t32-[01-14] * 190G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p skylake',
                               '-w skylake-t32-[01-14]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/skylake/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 190},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ skylake-f32-[01-06]
                {
                    'name': 'skylake-f32',
                    'descr': 'skylake-f32-[01-06] * 384G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p skylake',
                               '-w skylake-f32-[01-06]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/skylake/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 384},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ skylake
                {
                    'name': 'skylake-all',
                    'descr': 'skylake',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p skylake'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/skylake/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 384},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}

                # {{{ genoa-t64-[01-08]
                {
                    'name': 'genoa-t64',
                    'descr': 'genoa-t64-[01-08] * 384G',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p genoa',
                               '-w genoa-t64-[01-08]'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/genoa/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 384},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}
                # {{{ genoa
                {
                    'name': 'genoa-all',
                    'descr': 'genoa',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-p genoa'],
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/genoa/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'remote', 'scontrol'],
                    'extras': {'cn_memory': 384},
                    'prepare_cmds': ['source /usr/share/Modules/init/bash']
                },
                # }}}

                # {{{ prepost-haswell
                {
                    'name': 'prepost-haswell',
                    'descr': 'Haswell Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/haswell/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'scontrol'],
                    # variables
                    # prepare_cmds
                    # processor
                    # devices
                    # extras
                    # resources
                },
                # }}}
                # {{{ prepost-cascade
                {
                    'name': 'prepost-cascade',
                    'descr': 'Cascade Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/cascade/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'scontrol'],
                },
                # }}}
                # {{{ prepost-skylake
                {
                    'name': 'prepost-skylake',
                    'descr': 'Skylake Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/skylake/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'scontrol'],
                },
                # }}}
                # {{{ prepost-genoa
                {
                    'name': 'prepost-genoa',
                    'descr': 'Genoa Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    'env_vars': [
                        ['MODULEPATH',
                         '/softs/eb/genoa/modules/all:/softs/manual/modules']
                    ],
                    'time_limit': '10m',
                    'max_jobs': 4,
                    'features': ['cpu', 'scontrol'],
                },
                # }}}

            ]  # partitions
            # }}}
        }  # systems
    ],     # systems
    # }}}
    # {{{ environments
    'environments': [
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'features': ['serial', 'openmp', 'alloc_speed', 'hdf5'],
        },
        {
            'name': 'PrgEnv-gnu',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpif90',
            'features': [
                'serial', 'openmp', 'mpi', 'alloc_speed', 'hdf5'
            ],
            'prepare_cmds': ['echo SLURM_JOBID=$SLURM_JOBID'],
            'modules': ['foss']  # hwl:foss/2023a, else:foss/2025b (new:foss/2026.1)
        },
        {
            'name': 'PrgEnv-intel-old',
            'cc': 'mpiicc',
            'cxx': 'mpiicpc',
            'ftn': 'mpiifort',
            # 'target_systems': ['haswell-t16', 'haswell-f20', 'haswell-x20',
            #                    'haswell-x44', 'prepost-haswell'],
            'features': [
                'serial', 'openmp', 'mpi', 'alloc_speed', 'hdf5'
            ],
            'prepare_cmds': ['echo SLURM_JOBID=$SLURM_JOBID'],
            'modules': ['intel']  # hwl:intel/2023a, else:intel/2026
        },
        {
            'name': 'PrgEnv-intel',
            'cc': 'mpiicx',
            'cxx': 'mpiicpx',
            'ftn': 'mpiifx',
            # 'target_systems': ['cascade-t32', 'cascade-f32', 'cascade-x32',
            #     'skylake-t32', 'skylake-f32', 'genoa-t64', 'prepost-cascade',
            #     'prepost-skylake', 'prepost-genoa'],
            'features': [
                'serial', 'openmp', 'mpi', 'alloc_speed', 'hdf5'
            ],
            'prepare_cmds': ['echo SLURM_JOBID=$SLURM_JOBID'],
            'modules': ['intel']  # hwl:intel/2023a, else:intel/2026
        }
    ],
    # }}} environments
    # {{{ logging
    # reframe -C newton.py --show-config=logging
    'logging': [
        {
            # 'perflog_compat': True,
            # {{{ handlers
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'name': 'reframe.out',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': False
                }
            ],
            # }}}
            # {{{ handlers_perflog
            'handlers_perflog': [
                {
                    'type': 'httpjson',
                    # Set in the CI with environment variable: RFM_HTTPJSON_URL
                    # http://log.cscs.ch:31311
                    # http://vminsert.o11y.cscs.ch:8480/insert/0/prometheus/api/v1/import
                    'url': 'http://httpjson-server:12345/rfm',
                    'level': 'info',
#ok                     'extras': {
#ok                         'data_stream': {
#ok                             'type': 'logs',
#ok                             'dataset': 'performance_values',
#ok                             'namespace': 'reframe'
#ok                         },
#ok                         # 'rfm_ci_pipeline': os.getenv("CI_PIPELINE_URL", "#"),
#ok                         # 'rfm_ci_project': os.getenv("CI_PROJECT_PATH", "Unknown CI Project")
#ok                     },
                    'debug': True,
                    # 'json_formatter': _format_httpjson,
                    'ignore_keys': ['check_perfvalues']
                }
            ]
        }
    ]  # }}} logging
    # }}}  # logging

}  # site_configuration
