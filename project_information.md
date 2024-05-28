# DATA472 Individual Project
** Dimitrii Ustinov **
** dus15 **

## 1. Deployment
### 1. Clone this repository into your folder on local machine

```
cd PATH-YOUR-LOCAL-DIRECTORY
git clone https://github.com/dimitrii-ustinov/data472.git
```

### 2. Create a AWS EC2 for AuthServer instance

Follow the instructions from Paul Benden, access on LEARN (University of Canterbury internal page, only for students) in the AWS Resources chapter of this course.   

Additionally, basic information how to create and tune your EC2 instance you can find on the official AWS website here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html


### 3. AWS setup on EC2 (AuthServer)

1. To work with EC2 instance you need to connect to this virtual environment. You can do it using `ssh` or use AWS web interface to click the `Connect` button on the top right corner of EC2 instance page and select the tab `EC2 Instance Connect` by default, you will be able to connect to the instance without any further setup.

2. Copy the local folder on your machine to EC2 home directory running the command below on your local machine in terminal

```
cd <PATH-YOUR-LOCAL-DIRECTORY>data472
scp -i <PATH-TO-YOUR-PEM-KEY-ON-LOCAL-MACHINE> -r data472 ubuntu@<EC2-PUBLIC-IP-ADDRESS>:/home/ubuntu/
```


### 4. Setup Flask app environment on EC2 (AuthServer)

1. Using bash on EC2 create the `venv` folder in the `data472` folder and activate this environment using the following commands:
2. Enter to the folder `data472` using the command `cd data472`

```bash
sudo apt-get update
sudo apt install python3-virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```

3. Install the required packages using the command: 

```bash
pip install requirements.txt
```

4. Finally, your app folder should be like the following:

```
data472/
.
├── README.md
├── app.py
├── data_contract.md
├── project_information.md
├── README.md
├── requirements.txt
├── test_api.ipynb
└── venv
    ├── bin
    ├── lib
    └── pyvenv.cfg
```


### 5. Setup Gunicorn environment on EC2

1. Copy a `app.service` file from `data472` to the `/etc/systemd/system/` folder using the command 

```bash
sudo mv app.service /etc/systemd/system/
```

Note: If your EC2 instance image is not ubuntu, you should replace the `ubuntu` with the correct user name in the `app.service` file.

2. Enable the service by running the following command:

```bash
sudo systemctl start app
sudo systemctl enable app
```

### 6. Setup Nginx environment on EC2 

1. Install nginx by running the following command:

```bash
sudo apt-get update
sudo apt-get install nginx
```

2. Start Nginx:

```bash
sudo systemctl start nginx
```

3. Enable Nginx reverse proxy by updating a file named `default` in the `/etc/nginx/sites-available/` folder. You should replace the IP address in the file with your `EC2-PUBLIC-IP-ADDRESS` IP address.

```bash
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name <EC2-PUBLIC-IP-ADDRESS>;

        location / {
                proxy_pass         http://127.0.0.1:8000/;
                proxy_redirect     off;

                proxy_set_header   Host                 $host;
                proxy_set_header   X-Real-IP            $remote_addr;
                proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Proto    $scheme;
        }
}
```

4. Restart Nginx by running the following command:

```bash
sudo systemctl restart nginx
```

Now the web application will be available at the EC2 public IP address from the browser. `http://<EC2-PUBLIC-IP-ADDRESS>`


## Further development
This project is finished as is. However, it can benefit from further development:
1. The key was exposed in the code when querying the API. It should be hidden as an environmental variable.
2. As the dataset is relatively small and receives infrequent updates, It is not stored in a database and redirected to the Central Collection Team (CCT) after preprocessing directly.
Creation of RDS can help securing the retrieved information in case of crash on the side of outer source API.
3. There is no unique identifier in the dataset. Creation of a hashed column that could become a unique identifier can help filtering out old data and send only updated data to the CCT.
