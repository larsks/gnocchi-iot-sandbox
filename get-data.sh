#!/bin/sh

psql -U postgres -h stats.house sensors <<EOF
\copy (select * from sensor_dht order by measured_at asc) to data.csv with csv
EOF
