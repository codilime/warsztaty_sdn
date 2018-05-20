./scripts/reset_docker_logs.sh

#docker network rm red

./scripts/red/create_network.sh

./scripts/red/add_ala.sh

./scripts/red/add_ola.sh

./scripts/red/add_kasia.sh

./scripts/red/remove_ala.sh

./scripts/red/remove_ola.sh

./scripts/red/remove_kasia.sh
