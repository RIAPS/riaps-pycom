APP_FOLDER="/home/riaps/projects/RIAPS/riaps-pycom/tests/GroupFsm"
RIAPS_FILE="group.riaps"
DEPL_FILE="group.depl"
APP_NAME="GroupFSM"
CTRL_FILE="test.rc"

NODES="$(grep -oP 'on\s*\(\K[^)]+' $DEPL_FILE)"

FORMATTED_NODES=$(echo "$NODES" | tr '\n' ' ')

echo $FORMATTED_NODES

# Define the tmux session name
SESSION_NAME="riaps_ctrl"
LOG_SERVER="log_server"

# Start a new tmux session in the background
tmux new-session -d -s $SESSION_NAME
tmux new-session -d -s $LOG_SERVER

# Send commands to the log server session
tmux send-keys -t $SESSION_NAME 'rm server_logs/*; riaps_logger -a -p -d file' C-m

# Send commands to riaps ctrl session
tmux send-keys -t $SESSION_NAME 'riaps_ctrl -' C-m
tmux send-keys -t $SESSION_NAME "e Testing $APP_NAME" C-m

tmux send-keys -t $SESSION_NAME "j $FORMATTED_NODES" C-m
tmux send-keys -t $SESSION_NAME "f $APP_FOLDER" C-m
tmux send-keys -t $SESSION_NAME "m $RIAPS_FILE" C-m
tmux send-keys -t $SESSION_NAME "d $DEPL_FILE" C-m
tmux send-keys -t $SESSION_NAME "i $APP_NAME" C-m
tmux send-keys -t $SESSION_NAME "l $APP_NAME" C-m

# APP STOPPING LOGIC
echo "Press any key to stop the app..."
# -s: Do not echo input coming from a terminal
# -n 1: Read one character
read -s -n 1
echo "You pressed a key! Stopping..."
tmux send-keys -t $SESSION_NAME "h $APP_NAME" C-m
tmux send-keys -t $SESSION_NAME "r $APP_NAME" C-m
tmux send-keys -t $SESSION_NAME "q" C-m

echo "Press any key to exit tmux..."
read -s -n 1
tmux send-keys -t $SESSION_NAME "exit" C-m
tmux send-keys -t $LOG_SERVER "exit" C-m
# Kill the tmux session to ensure it is properly terminated
tmux kill-session -t $SESSION_NAME
echo "You pressed a key! Exiting..."
