./scripts/reset_docker_logs.sh

./scripts/red/create_network.sh

./scripts/blue/create_network.sh

./scripts/red/add_ala.sh

./scripts/blue/add_ala.sh

./scripts/red/add_ola.sh

./scripts/blue/add_ola.sh

./scripts/red/add_kasia.sh

./scripts/blue/add_kasia.sh

read -n 1

./scripts/red/remove_ola.sh

./scripts/blue/remove_ola.sh

./scripts/red/remove_ala.sh

./scripts/blue/remove_ala.sh

./scripts/red/remove_kasia.sh

./scripts/blue/remove_kasia.sh

