# humanist-django

~~This is the repository for the humanist project at [Kings Digital Lab](https://kdl.kcl.ac.uk)~~

~~This project uses the technologies outlined in our [Technology Stack](https://stackshare.io/kings-digital-lab/django) and is configured to use [Vagrant](https://www.vagrantup.com/) for local development and [Fabric](http://www.fabfile.org/) for deployment.~~

## Requirements
* Docker
* Docker Compose

## Getting Started

### Config

#### Docker network config

If we want Django to communicate with the host machine, e.g. for mails, we need to add the ip address of the local network interface in the docker compose configuration file.

To list the ip addresses of all local network interfaces ```ip addr show```

Limit to a specific interface (in this example eth0) ```ip addr show eth0```

#### Django config

Some Django settings may have to be overridden. To do this, create a ```local.py``` in ```./humanist/settings/```

Example configuration
```./humanist/settings/local.py```
```
from .base import *  # noqa
from .docker import * # noqa

LOGGING_LEVEL = logging.DEBUG

LOGGING['loggers']['humanist']['level'] = LOGGING_LEVEL

DEBUG = True

SECRET_KEY = 'changeme'
```

Override Django base settings as needed in this file.
Try to not override any of the docker related settings.

### Run docker compose

Simply run ```docker-compose up```

### Create an admin account

First, find the name of the docker compose container in the docker compose log.
Should be something like ```humanist-django_web_1```

Access the container console using:
```docker exec -it humanist-django_web_1 /bin/bash```

Inside of the container run the following script:
```./manage.py createsuperuser```

### Run management commands

First, find the name of the docker compose container in the docker compose log.
Should be something like ```humanist-django_web_1```

Access the container console using:
```docker exec -it humanist-django_web_1 /bin/bash```

Inside of the container run the following script:
```./manage.py command```

To see a list of all management commands run the following:
```./manage.py```

