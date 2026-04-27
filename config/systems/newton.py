# https://reframe-hpc.readthedocs.io/en/latest/config_reference.html

import os


site_configuration = {

#{{{ systems
# ./R -c checks/prgenv/mpi_cpi.py -l --system newton:skylake-t32 --prgenv PrgEnv-gnu
    'systems': [
        {
            #{{{ skylake
            'name': 'newton',
            #'name': 'Newton skylake',
            'descr': 'https://pmcs2i.ec-lyon.fr/documentation/resources/newton.html',
            #'hostnames': ['haswell', 'skylake', 'cascade', 'genoa'],
            #'hostnames': ['prepost-haswell', 'prepost-skylake', 'prepost-cascade', 'prepost-genoa'],
            'hostnames': ['prepost-skylake'],
            # max_local_jobs
            'modules_system': 'tmod4',
            #'modules'
            #env_vars
            #variables
            #prefix
            #stagedir
            #outputdir
            'resourcesdir': '/store/pmcs2i/',
            #sched_options
            'partitions': [
#{{{ partition:skylake-t32-[01-14] + 190GB
                {
                    'name': 'skylake-t32',
                    'descr': 'skylake-t32-[01-14]',
                    'scheduler': 'slurm',
                    #sched_options
                    'launcher': 'srun',
                    #'access'
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    #"container_platforms": 
                    #modules
                    #env_vars
                    #variables
                    'time_limit': '10m',
                    'max_jobs': 4,
                    #'prepare_cmds':
                    #processor
                    #devices
                    'features': ['cpu', 'remote', 'scontrol'],
                    #extras
                    #resources
                },
#}}}
#{{{ partition:skylake-f32-[01-06] + 384GB
                {
                    'name': 'skylake-f32',
                    'descr': 'skylake-f32-[01-06]',
                    'scheduler': 'slurm',
                    #sched_options
                    'launcher': 'srun',
                    #'access'
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    #"container_platforms": 
                    #modules
                    #env_vars
                    #variables
                    'time_limit': '10m',
                    'max_jobs': 4,
                    #'prepare_cmds':
                    #processor
                    #devices
                    #features
                    #extras
                    #resources
                },
#}}}
#{{{ partition:login
                {
                    'name': 'login',
                    'descr': 'Login nodes',
                    'scheduler': 'local',
                    #sched_options
                    'launcher': 'local',
                    #'access'
                    'environs': ['builtin', 'PrgEnv-gnu', 'PrgEnv-intel'],
                    #"container_platforms": 
                    #modules
                    #env_vars
                    #variables
                    'time_limit': '10m',
                    'max_jobs': 4,
                    #'prepare_cmds':
                    #processor
                    #devices
                    'features': ['cpu', 'remote', 'scontrol'],
                    #extras
                    #resources
                }
#}}}
            ]  # partitions
            #}}}
        }  # systems
    ],     # systems
#}}}
#{{{ environments
    'environments': [
        {
            'name': 'PrgEnv-gnu',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpif90',
            #'target_systems': [''],
            'features': [
                'serial', 'openmp', 'mpi', 'alloc_speed', 'hdf5'
            ],
            'modules': ['foss/2025b']
        },
        {
            'name': 'PrgEnv-intel',
            'cc': 'mpiicx',
            'cxx': 'mpiicpx',
            'ftn': 'mpiifort',
            'features': [
                'serial', 'openmp', 'mpi', 'alloc_speed', 'hdf5'
            ],
            'modules': ['intel/2025a']
        }
    ]
#}}} environments

}  # site_configuration
