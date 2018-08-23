#!/usr/bin/env bash
function create_network {
  if [ "$#" -ne 2 ]; then
      echo "Usage: create_network <net_id> <ip>"
      echo 'Example: create_network "net_red" "192.168.0.0/24"'
  else
    curl -X POST 172.20.128.10:8090/create/network -H "Content-Type: application/json" -d '{"id": "'$1'", "ip": "'$2'"}'
  fi
}


function create_container {

  if [ "$#" -ne 1 ]; then
      echo "Usage: create_container <id>"
      echo 'Example: create_container "ala"'
  else
    curl -X POST 172.20.128.10:8090/create/container -H "Content-Type: application/json" -d '{"id": "'$1'"}'
  fi
}


function create_logical_port {
  if [ "$#" -ne 2 ]; then
      echo "Usage: create_logical_port <net_id> <container_id>"
      echo 'Example: create_logical_port "net_red" "ala"'
  else
    curl -X POST 172.20.128.10:8090/create/logical_port -H "Content-Type: application/json" -d '{"net_id": "'$1'", "container": {"id": "'$2'"}}'
  fi
}


function sdn_help {
  curl -X GET 172.20.128.10:8090/help
}


function containers {
  curl -X GET 172.20.128.10:8090/containers
}


function logical_ports {
  curl -X GET 172.20.128.10:8090/logical_ports
}


function networks {
  curl -X GET 172.20.128.10:8090/networks
}


function force_clean {
  curl -X POST 172.20.128.10:8090/force_clean
}


function sdn_post {
  if [ "$#" -ne 2 ]; then
      echo "Usage: sdn_post <path> <payload>"
      echo "Example: sdn_post \"create/container\" '{\"id\": \"ala\"}'"
  else
      curl -X POST 172.20.128.10:8090/$1 -H "Content-Type: application/json" -d $2
  fi
}


function sdn_get {
  if [ "$#" -ne 1 ]; then
      echo "Usage: sdn_get <path>"
      echo 'Example: sdn_get "help"'
  else
      curl -X GET 172.20.128.10:8090/$1
  fi
}


function sdn_functions {
  echo "Available functions:"
  echo "create_network"
  echo "create_container"
  echo "create_logical_port"
  echo "sdn_help"
  echo "containers"
  echo "logical_ports"
  echo "networks"
  echo "sdn_post"
  echo "sdn_get"
  echo "sdn_functions"
}
