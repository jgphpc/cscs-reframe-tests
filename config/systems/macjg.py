import json
import os
from reframe.core.logging import _format_time_rfc3339


# {{{ ELASTIC
def _format_httpjson(record, extras, ignore_keys):
    """
    https://github.com/eth-cscs/cscs-reframe-tests/pull/380
    """
    data = {}
    for attr, val in record.__dict__.items():
        if attr in ignore_keys or attr.startswith('_'):
            continue

        if attr == 'check_perf_value' and val is not None:
            data[attr] = float(val)
        elif attr == 'check_perf_ref' and val is not None:
            data[attr] = float(val)
        else:
            data[attr] = val

    data.update(extras)
    data['@timestamp'] = _format_time_rfc3339(record.created, r'%FT%T%:z')
    # data['@timestamp'] = data['check_job_completion_time']
    # data['@timestamp'] = data['check_job_completion_time_unix']
    # data['@timestamp'] = datetime.fromtimestamp(time.time()).astimezone()

    return json.dumps(data)
# }}}


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
    'systems': [
        {
            'name': 'JG-M2-CSCS',
            'descr': 'My laptop',
            'hostnames': ['JG-M2-CSCS'],
            'modules_system': 'nomod',
            # 'resourcesdir':
            #     '/capstor/store/cscs/cscs/public/reframe/resources',
            'max_local_jobs': 20,
            'partitions': [
                {
                    'name': 'login',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'time_limit': '10m',
                    'environs': [
                        'gnu',
                    ],
                    'descr': 'Login nodes',
                    'max_jobs': 20
                }
            ]
        },
    ],
    'environments': [
        {
            'name': 'gnu',
            'cc': '/opt/homebrew/bin/gcc-15',
            'cxx': '/opt/homebrew/bin/g++-15',
            'ftn': '/opt/homebrew/bin/gfortran-15'
            # 'features': ['openmp'],
            # 'extras': {'ompflag': '-fopenmp'}
        },
    ],
    'logging': [
        {
            'perflog_multiline': True,  # <---
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],

            'handlers_perflog': [
# 
#             # {{{ perflogs
#                 {
#                     'type': 'filelog',
#                     'prefix': '%(check_system)s/%(check_partition)s',
#                     'level': 'info',
#                     'format': (
#                         '%(check_job_completion_time)s|reframe %(version)s|'
#                         '%(check_info)s|jobid=%(check_jobid)s|'
#                         '%(check_perf_var)s=%(check_perf_value)s|'
#                         'ref=%(check_perf_ref)s '
#                         '(l=%(check_perf_lower_thres)s, '
#                         'u=%(check_perf_upper_thres)s)|'
#                         '%(check_perf_unit)s'
#                     ),
#                     'append': True
#                 },
#                 # }}}
                # {{{ ELASTIC
                {
                    'type': 'httpjson',
                    # We are setting this from the environment
                    # to avoid polluting the logs from tests in the
                    # login nodes
                    # 'http://httpjson-server:12345/rfm'),
                    # 'url': 'https://localhost:9200/rfm-v2/_doc',
                    'url': os.getenv('RFM_HTTPJSON_URL_ELASTIC',
                                     'http://dummy:1234/rfm'),
                    # -> could not initialize the httpjson handler;ignoring ...
                    'level': 'info',
                    'extras': {
# CSCS                         'data_stream': {
# CSCS                             'type': 'logs',
# CSCS                             'dataset': 'performance_values',
# CSCS                             'namespace': 'reframe'
# CSCS                         },
                        'rfm_ci_pipeline': os.getenv('CI_PIPELINE_URL', '#'),
                        'rfm_ci_project':
                            os.getenv('CI_PROJECT_PATH', 'Unknown CI Project')
                    },
                    'json_formatter': _format_httpjson,
                    'ignore_keys': ['check_perfvalues'],
                    'debug': False
                },
                # }}}
                # {{{ VICTORIAMETRICS
                {
                    'type': 'httpjson',
                    #xnode: export RFM_HTTPJSON_URL_VMETRICS='http://127.0.0.1:8428/insert/0/prometheus/api/v1/import'
                    #1node: export RFM_HTTPJSON_URL_VMETRICS='http://127.0.0.1:8428/api/v1/import'
                    #cscs: export RFM_HTTPJSON_URL_VMETRICS='http://vminsert.o11y.cscs.ch:8480/insert/0/prometheus/api/v1/import'
                    'url': os.getenv('RFM_HTTPJSON_URL_VMETRICS',
                                     'http://dummy:1234/rfm'),
                    # -> could not initialize the httpjson handler;ignoring ...
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
                    'ignore_keys': ['check_perfvalues'],
                    # 'debug': True
                },
                # }}}
            ]
        }
    ],
}
