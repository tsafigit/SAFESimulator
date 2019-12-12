Misc configuration details


	• VirtualBox
	• Ubuntu iso file: ubuntu-18.04.3-desktop-amd64
	• Networking between host and guest:
		○ Host only adapter
	• JIRA
		○ Sudo /opt/atlassian/jira/bin/start-jira.sh -fg
	• Access JIRA
		○ IP:8080
	• Run "settime" remotely
		○ Install ssh on the guest
		○ Sudo visudo
			§ Add line to use no passwd for the user:
			§ nelkag ALL = NOPASSWD: ALL
		○ ssh nelkag@192.168.56.101 "cd /home/nelkag/Simulator/misc; python /home/nelkag/Simulator/misc/settime.py"


Running tests from command line

	• python -m tests.testTeamSprint
	• python -m unittest discover tests


