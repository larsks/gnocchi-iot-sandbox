#!/usr/bin/env python

import argparse
import csv
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

LOG = logging.getLogger(__name__)
logging.basicConfig(level='INFO')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--batchsize', '-b',
                   type=int,
                   default=1000)
    p.add_argument('input')
    return p.parse_args()


args = parse_args()

with open(args.input) as fd:
    reader = csv.reader(fd)

    cache = {}
    measures = {}
    measure_count = 0
    total_count  = 0
    for row in reader:
        timestamp = row[0]
        fields = json.loads(row[2])
        values = json.loads(row[3])

        macaddr = fields['sensor_id']

        if macaddr not in cache:
            r = requests.post(
                'http://localhost:8041/v1/search/resource/dhtsensor',
                headers={'content-type': 'application/json'},
                auth=HTTPBasicAuth('admin', ''),
                data=json.dumps({'=': {'macaddr': macaddr}}))
            r.raise_for_status()
            cache[macaddr] = r.json()[0]

        resource = cache[macaddr]

        if resource['id'] not in measures:
            measures = {resource['id']: {}}
        for name, value in values.items():
            name = 'sensor.dht.{}'.format(name)
            if name in resource['metrics']:
                if name not in measures[resource['id']]:
                    measures[resource['id']][name] = []

                measures[resource['id']][name].append({
                    'timestamp': timestamp,
                    'value': value,
                })

                measure_count += 1
                total_count += 1
                if measure_count % args.batchsize == 0:
                    LOG.info('sending %d metrics', measure_count)
                    r = requests.post(
                        'http://localhost:8041/v1/batch/resources/metrics/measures',
                        headers={'content-type': 'application/json'},
                        auth=HTTPBasicAuth('admin', ''),
                        data=json.dumps(measures))
                    r.raise_for_status()

                    measure_count = 0
                    measures = {}

    LOG.info('sending %d metrics', measure_count)
    r = requests.post(
        'http://localhost:8041/v1/batch/resources/metrics/measures',
        headers={'content-type': 'application/json'},
        auth=HTTPBasicAuth('admin', ''),
        data=json.dumps(measures))
    r.raise_for_status()
