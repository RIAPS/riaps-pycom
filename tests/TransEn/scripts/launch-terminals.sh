xterm -geometry 93x31+700+100 -hold -e ssh bbb-ff98.local & 
xterm -geometry 93x31+700+600 -hold -e ssh bbb-53b9.local &
#xterm -hold -e ssh bbb-1f82.local &
#xterm -hold -e ssh bbb-d5b5.local &
xterm -hold -e rpyc_registry.py &
sleep 1
xterm -geometry 93x31+100+350 -hold -e riaps_ctrl &
sleep 1
xterm -hold -e 'cd ~/riaps-svn/samples/grunner-project/ && python3 riaps_grunner.py' &

#ssh -t bbb-d5b5.local 'sudo systemctl stop ntp.service; sudo ntpdate 192.168.0.108' 
ssh -t bbb-53b9.local 'sudo systemctl stop ntp.service; sudo ntpdate 192.168.0.108' 
#ssh -t bbb-1f82.local 'sudo systemctl stop ntp.service; sudo ntpdate 192.168.0.108' 
ssh -t bbb-ff98.local 'sudo systemctl stop ntp.service; sudo ntpdate 192.168.0.108' 

ssh -t bbb-ff98.local 'tmux new -d -s deplo'
ssh -t bbb-ff98.local 'tmux send -t deplo.0 riaps_deplo ENTER'
#ssh -t bbb-d5b5.local 'tmux attach -t deplo'
ssh -t bbb-53b9.local 'tmux new -d -s deplo'
ssh -t bbb-53b9.local 'tmux send -t deplo.0 riaps_deplo ENTER'
#ssh -t bbb-53b9.local 'tmux attach -t deplo'
