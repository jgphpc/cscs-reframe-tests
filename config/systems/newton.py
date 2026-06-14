# https://reframe-hpc.readthedocs.io/en/latest/config_reference.html
# ./R -c checks/eclyon/mem.py --system newton:haswell-t16 -p PrgEnv-gnu -r ###--skip-performance-check

import json
import os


# {{{ VICTORIAMETRICS
def _format_victoriametrics(record, extras, ignore_keys):
    data = {}
    for attr, val in record.__dict__.items():
        if attr in ignore_keys or attr.startswith('_'):
            continue

        if attr in ('check_perf_value', 'check_perf_ref') and val is not None:
            data[attr] = float(val)
        else:
            data[attr] = val

    data.update(extras)
    # data['@timestamp'] = _format_time_rfc3339(record.created, r'%FT%T%:z')

    timestamp = data.get('check_job_completion_time_unix')
    timestamps = [int(timestamp * 1000)] if timestamp is not None else None

    # VMetrics labels must be strings; keep perf values out of labels
    labels = {
        k: str(v) if v is not None else ''
        for k, v in data.items()
        if k not in ('check_perf_value', 'check_perf_ref')
    }
    labels.setdefault('__name__', labels.get('check_unique_name', 'reframe'))

    lines = []
    for perf_key, perf_type in (
        ('check_perf_value', 'value'),
        ('check_perf_ref', 'ref'),
    ):
        perf_val = data.get(perf_key)
        if perf_val is None:
            continue

        payload = {
            'metric': {**labels, 'check_perf_type': perf_type},
            'values': [perf_val],
        }
        if timestamps is not None:
            payload['timestamps'] = timestamps

        lines.append(json.dumps(payload, separators=(',', ':')))

    return '\n'.join(lines) + '\n' if lines else None
# }}}


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
            'perflog_multiline': True,
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
            # {{{ PERFLOGS
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'datefmt': '%FT%T%:z',
                    'append': True
                },
                # }}}
                # {{{ VICTORIAMETRICS
                {
                    'type': 'httpjson',
                    #1node: export RFM_HTTPJSON_URL_VMETRICS='http://127.0.0.1:8428/api/v1/import'
                    #xnode: export RFM_HTTPJSON_URL_VMETRICS='http://127.0.0.1:8428/insert/0/prometheus/api/v1/import'
                    #cscs: export RFM_HTTPJSON_URL_VMETRICS='http://vminsert.o11y.cscs.ch:8480/insert/0/prometheus/api/v1/import'
                    # -> could not initialize the httpjson handler;ignoring ...
                    'url': os.getenv('RFM_HTTPJSON_URL_VMETRICS',
                                     'http://dummy:1234/rfm'),
                    'level': 'info',
                    'extra_headers': {
                        'Content-Type': 'application/x-ndjson'
                    },
                    'extras': {
                        'rfm_ci_pipeline': os.getenv('CI_PIPELINE_URL', '#'),
                        'rfm_ci_project':
                            os.getenv('CI_PROJECT_PATH', 'Unknown CI Project')
                    },
                    'json_formatter': _format_victoriametrics,
                    'ignore_keys': [
                        'check_perfvalues',
                        'check_info', 'version', 'check_fail_phase',
                        'check_fail_reason', 'check_perf_result',
                        'check_job_exitcode',
                        'check_build_locally', 'check_build_time_limit',
                        'check_descr', 'check_env_vars',
                        'check_exclusive_access', 'check_executable',
                        'check_executable_opts', 'check_extra_resources',
                        'check_keep_files', 'check_local', 'check_maintainers',
                        'check_maintainers', 'check_max_pending_time',
                        'check_modules', 'check_num_cpus_per_task',
                        'check_num_gpus_per_node', 'check_num_tasks',
                        'check_num_tasks_per_core', 'check_num_tasks_per_node',
                        'check_num_tasks_per_socket', 'check_postbuild_cmds',
                        'check_postrun_cmds', 'check_prebuild_cmds',
                        'check_prefix', 'check_prerun_cmds',
                        'check_readonly_files', 'check_short_name',
                        'check_sourcepath', 'check_sourcesdir',
                        'check_stagedir', 'check_strict_check', 'check_tags',
                        'check_time_limit', 'check_use_multithreading',
                        'check_valid_prog_environs', 'check_valid_systems',
                        'check_variables'
                    ],
                    'debug': False
                },
                # }}}
            ]
        }
    ]  # }}} logging
    # }}}  # logging

}  # site_configuration
