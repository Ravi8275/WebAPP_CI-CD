set -eo pipefail

#update all the installed packages
sudo yum update -y


#installing the required
sudo yum install -y wget gnupg python3 gcc 
#providing the repository to download postgres
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
#sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG
#to download the gpg key which is used to signpostgres package
curl -O https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
file RPM-GPG-KEY-PGDG
sudo rpm --import RPM-GPG-KEY-PGDG
#gpg --import RPM-GPG-KEY-PGDG


# Removing all installed GPG keys
sudo rpm -e --allmatches gpg-pubkey

sudo yum update -y

sudo mv /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial.bad




sudo yum -y module disable postgresql
#sudo yum clean metadata
#sudo yum makecache

sudo yum clean all
sudo yum clean metadata
sudo dnf clean all

# Running yum update to fetch new GPG keys
sudo yum update -y

# Restoring original GPG key filenames
sudo mv /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial.bad /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial

# Downloading and installing perl-IPC-Run manually
yum search perl-IPC-Run
sudo yum install -y perl-IPC-Run
sudo yum install -y postgresql14-server postgresql14-devel --nobest --skip-broken
#starting the postgres
sudo systemctl enable --now postgresql-14
sudo systemctl restart postgresql-14
sudo yum update -y

#exporting variables
export POSTGRES_USER=${POSTGRES_USER}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
export POSTGRES_DB=${POSTGRES_DB}
export POSTGRES_PORT=${POSTGRES_PORT}
export POSTGRES_HOST=${POSTGRES_HOST}

#creating postgres user
#connecting to the postgres
sudo su - postgres
#database creation
psql -c "CREATE DATABASE ${POSTGRES_DB};"
#user creation
psql -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
#Grant permissions to the user
psql -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"
sudo systemctl restart postgresql

#Requirements installation
cd /home/admin/WebAPP_CI-CD
sudo python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install -r "$(pwd)/requirements.txt"

#Webapp system services
sudo cp Packer/Webapp.services /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable Webapp.services
sudo systemctl start Webapp.services