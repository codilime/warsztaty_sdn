./scripts/reset_docker_logs.sh

#docker network rm red

./scripts/red/create_network.sh

./scripts/red/add_ala.sh

./scripts/red/add_ola.sh

./scripts/red/add_kasia.sh

read -n 1

./scripts/red/remove_ala.sh

./scripts/red/remove_ola.sh

./scripts/red/remove_kasia.sh

#./scripts/red/add_kasia.sh

#./scripts/clean.sh

#./scripts/red/remove_kasia.sh

#docker logs sdn_controller_1


