#!/bin/bash

# CYLC USERGUIDE EXAMPLE SYSTEM.
# Task B: a sea state model.

# Depends on surface wind forecast, and own restart file.
# Generates two restart files, valid for the next two cycles.

# run length 60 minutes, scaled

# START MESSAGE
cylc message --started

ACCEL=$(( 3600 / 10 )) # 10 s => 1 hour
SLEEP=$(( 20 * 60 / ACCEL )) 

# CHECK PREREQUISITES
ONE=$TMPDIR/surface-winds-${CYLC_TIME}.nc       # surface winds
TWO=$TMPDIR/${CYLC_TASK}-${CYLC_TIME}.restart   # restart file
for PRE in $ONE $TWO; do
    if [[ ! -f $PRE ]]; then
        # FAILURE MESSAGE
        cylc message -p CRITICAL "file note found: $PRE"
        cylc message --failed
        exit 1
    fi 
done

# EXECUTE THE MODEL ...

# create a restart file for the next cycle
sleep $SLEEP   # 20 min
touch $TMPDIR/${CYLC_TASK}-${NEXT_CYLC_TIME}.restart
cylc message "$CYLC_TASK restart files ready for $NEXT_CYLC_TIME"

# create a restart file for the next next cycle
sleep $SLEEP   # 40 min
touch $TMPDIR/${CYLC_TASK}-${NEXT_NEXT_CYLC_TIME}.restart
cylc message "$CYLC_TASK restart files ready for $NEXT_NEXT_CYLC_TIME"

# create sea state forecast output
sleep $SLEEP   # 60 min
touch $TMPDIR/sea-state-${CYLC_TIME}.nc
cylc message "sea state fields ready for $CYLC_TIME"

# SUCCESS MESSAGE
cylc message --succeeded
