# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 


# Below is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.


WORKBENCH LOGIN: 

*** Standard TCP/IP

Endpoint/Hostname: csc648.cqkov7pmg4ge.us-east-1.rds.amazonaws.com

Port: 3306 

UserName: admin

Password: sanfrancisco


Application Link: ec2-3-82-174-225.compute-1.amazonaws.com:80


1. Server URL or IP  
    The pubic IP is not static. Can be retrieved when instance is launched. 
2. SSH username  
    ubuntu
3. SSH password or key.
    <br> If a ssh key is used please upload the key to the credentials folder.  
    keypair_EC2_jeff0202.pem
4. Database URL or IP and port used.
    <br><strong> NOTE THIS DOES NOT MEAN YOUR DATABASE NEEDS A PUBLIC FACING PORT.</strong> But knowing the IP and port number will help with SSH tunneling into the database. The default port is more than sufficient for this class.  
    The pubic IP is not static.
5. Database username  
    cmcglothen@mail.sfsu.edu
6. Database password  
    Orange3953!
7. Database name (basically the name that contains all your tables)  
    csc648
8. Instructions on how to use the above information.  
    First, log into AWS dash board with account:cmcglothen@mail.sfsu.edu and pwd:Orange3953!  
    Seoncond, launch the instance and obtain the public IP  
    Last, ssh with keypair_EC2_jeff0202.pem, public IP and username:ubuntu  
# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.
