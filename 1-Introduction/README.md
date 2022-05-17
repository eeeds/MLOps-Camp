## I'll use EC2 to run my web server
## Create and instance of EC2
## Conect it with the command
```
ssh -i ~/.ssh/aws-key-pair.pem name@ip
```
## Download Anaconda and install it in your EC2 instance
Go to [Anaconda](https://www.anaconda.com/products/distribution)
Copy the link to the executable file
Then run the following command in your EC2 instance
```
wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
```
Then run:
```
bash Anaconda3-5.0.1-Linux-x86_64.sh
```
## Install Docker
```
sudo apt-get update
```
```
sudo apt install docker.io
```

## Create the soft folder
```
mkdir ~/soft
```
## Install docker-compose
## Go to GitHub and download the latest version of docker-compose
## Run the following command:
```
wget https://github.com/docker/compose/releases/download/v2.5.1/docker-compose-linux-x86_64
```
## Make it executable
```
chmod +x docker-compose
```
## Modify the path variable to include the docker-compose file (modify .bashrc)
```
export PATH="${HOME}/soft:${PATH}"
```
## Execute .bashrc
```
source ~/.bashrc
```
## Make sure that variables are set
## Run the following command to check if everything is set
```
which docker-compose
```
## Test docker running the following command
```
sudo docker run hello-world
```
## Add the user to the docker group
```
sudo usermod -aG docker $USER
```
## Clone the main repository of the course
```
git clone https://github.com/DataTalksClub/mlops-zoomcamp.git
```
## Pair a port with the EC2 instance
## Then creates the file duration-prediction.ipynb