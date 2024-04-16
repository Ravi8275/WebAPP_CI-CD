set -eo pipefail

#update all the installed packages
sudo yum update -y

#installing the required
sudo yum install -y wget gnupg python3 gcc
#providing the repository to download postgres
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
#to download the gpg key which is used to signpostgres package
curl -O https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG-14
sudo yum -y module disable postgresql

#sudo yum clean all
#sudo yum makecache
# curl -LO https://cpan.metacpan.org/authors/id/T/TO/TODDR/IPC-Run-20210523.0.tar.gz
#sudo yum install -y gcc make perl-CPAN perl-devel
#sudo cpan -f IPC::Run
sudo dnf install -y perl

# Downloading and installing perl-IPC-Run manually
curl -O http://rpmfind.net/linux/centos/8-stream/BaseOS/x86_64/os/Packages/perl-IPC-Run-0.99-1.el8.noarch.rpm
sudo cpan IPC::Run
# Installing PostgreSQL server and development package
sudo dnf install -y postgresql14-server postgresql14-devel --nobest --skip-broken
#starting the postgres
sudo systemctl enable --now postgresql-14

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

