#!/usr/bin/env bash

source "docker-tools-inc.sh"

pushd 'composes/' &> /dev/null || exit 1
ALL_CONTAINERS=${ALL_CONTAINERS:-$(find . -maxdepth 1 ! -path . -type d | cut -c3-)}
popd &> /dev/null || exit 1

# @purpose: Start all docker-compose.yml
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

  [[ "${#all[@]}" -gt 0 ]] && timeout $$ 180

  for container in ${all[*]}; do
    status=$(getHealth "${container}")
    if [[ "${status}" == "\"healthy\"" ]]; then
      echo -e "\033[0;93m⠿ Container \"${container}\" is already up\033[0;0;0m"
    else
      echo -e "\033[0;34m⠿ Container ${container} is ${status}"
      echo -e "⠿ Starting container ${container} \033[0;0;0m"
      pushd "composes/${container}" &>/dev/null || exit 1
      if docker compose up --force-recreate --build --remove-orphans --detach; then
        waitHealthy "${container}"
        echo ''
      else
        echo -e "\033[0;31m⠿ Docker (docker compose up) command failed! \033[0;0;0m\n"
      fi
      popd &>/dev/null || exit 1
    fi
  done
}

echo ''
startContainers
