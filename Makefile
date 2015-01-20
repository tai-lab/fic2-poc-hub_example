all:
	echo 'WIP'

build_quickhub:
	docker build --rm=true -t 'fic2-hub:latest' .

launch_quickhub:
	docker run -it --rm=true --name='hub' -e '5000' -v "$(pwd):/usr/src/app" 'fic2-hub:latest' /bin/bash

launch_nginx:
	docker run -it --rm=true --link="hub:hub" -p '443:443' 'fic2-hub-nginx:latest'

launch_bower:
	docker run -it --rm=true -u "$(id -u)" -v "$(pwd):/root" 'fic2-hub-bower:latest'