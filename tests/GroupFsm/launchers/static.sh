APP_FOLDER="/home/riaps/projects/RIAPS/riaps-pycom/tests/GroupFsm"
RIAPS_FILE="group.riaps"
DEPL_FILE="group.depl"
APP_NAME="GroupFSM"
CTRL_FILE="test.rc"

NODES="$(grep -oP 'on\s*\(\K[^)]+' $DEPL_FILE)"
FORMATTED_NODES=$(echo "$NODES" | tr '\n' ' ')

rm $CTRL_FILE

printf "# RIAPS Control command file\n" >> $CTRL_FILE
printf "e Testing $APP_NAME\n" >> $CTRL_FILE
printf "j $FORMATTED_NODES\n" >> $CTRL_FILE
printf "f $APP_FOLDER\n" >> $CTRL_FILE
printf "m $RIAPS_FILE\n" >> $CTRL_FILE
printf "d $DEPL_FILE\n" >> $CTRL_FILE
printf "i $APP_NAME\n" >> $CTRL_FILE
printf "l $APP_NAME\n" >> $CTRL_FILE
printf "w 30\n" >> $CTRL_FILE
printf "h $APP_NAME\n" >> $CTRL_FILE
printf "r $APP_NAME\n" >> $CTRL_FILE
printf "q\n" >> $CTRL_FILE

riaps_ctrl $CTRL_FILE