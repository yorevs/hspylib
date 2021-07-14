#!/usr/bin/env bash

source "docker-tools.sh"

ALL_CONTAINERS=${ALL_CONTAINERS:-$(find . -maxdepth 1 ! -path . -type d | cut -c3-)}

# @purpose: Start all docker containers
# -param $1: if the execution is on an interactive console or not
startContainers() {
  all=()

  for container in ${ALL_CONTAINERS}; do
    read -r -n 1 -p "Start container ${container} (y/[n]): " ANS
    test -n "${ANS}" && echo ''
    if [[ "${ANS}" == 'y' || "${ANS}" == 'Y' ]]; then
      all+=("${container}")
    fi
  done
  echo ''

  for container in ${all[*]}; do
    status=$(getStatus "${container}")
    if [ "${status}" = "\"running\"" ]; then
      echo -e "\033[0;34m⠿ Container \"${container}\" is already up\033[0;0;0m"
    else
      echo -e "\033[0;34m⠿ Starting container ${container} \033[0;0;0m"
      pushd "${container}" &>/dev/null || exit 1
      docker compose up --force-recreate --build --remove-orphans --detach
      waitHealthy "${container}"
      popd &>/dev/null || exit 1
    fi
  done
}

echo ''
startContainers
