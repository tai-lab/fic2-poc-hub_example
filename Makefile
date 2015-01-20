all:
	echo 'WIP'

build_quickhub:
	docker build --rm=true -t 'foobar-site:latest' .

launch_quickhub:
	docker run -it --rm=true --name='site' -e '5000' -v "$(pwd):/usr/src/app" 'foobar-site:latest' /bin/bash

launch_nginx:
	docker run -it --rm=true --link="site:site" -p '443:443' 'foobar-site-nginx:latest'

launch_bower:
	docker run -it --rm=true -u "$(id -u)" -v "$(pwd):/root" 'foobar-site-bower:latest' /bin/bash