set -eo pipefail

sudo yum update -y

sudo yum install -y wget gnupg python3 postgresql14-server postgresql14-devel
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo yum install -y postgresql14-server postgresql14-devel
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb

#postgres user and database setup
sudo systemctl enable --now postgresql-14
sudo -u postgres psql -c "CREATE DATABASE clientdatabase;"
sudo -u postgres psql -c "CREATE USER webappcicd WITH PASSWORD 'webappcicd';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE clientdatabase TO webappcicd;"
sudo sed -i 's/\(scram-sha-256\|ident\|peer\)/md5/g' /etc/postgresql/14/main/pg_hba.conf
sudo systemctl restart postgresql

export DATABASE_URL=postgresql://webappcicd:webappcicd@localhost:5432/clientdatabase

sudo -u postgres psql -d clientdatabase -c "
CREATE TABLE clients (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    second_name VARCHAR,
    account_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"

python3 -m pip install --upgrade pip
cd cd /Users/raviirt/Desktop/WebAPP_CI-CD
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install -r "$(pwd)/requirements.txt"

