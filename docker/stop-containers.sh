#!/usr/bin/env bash

source "docker-tools-inc.sh"

pushd 'composes/' &> /dev/null || exit 1
ALL_CONTAINERS=${ALL_CONTAINERS:-$(find . -maxdepth 1 ! -path . -type d | cut -c3-)}
popd &> /dev/null || exit 1

# @purpose: Stop all docker-compose.yml
# -param $1: if the execution is on an interactive console or not
stopContainers() {
  all=()

  for container in ${ALL_CONTAINERS}; do
    read -r -n 1 -p "Stop container ${container} (y/[n]): " ANS
    test -n "${ANS}" && echo ''
    if [[ "${ANS}" == 'y' || "${ANS}" == 'Y' ]]; then
      all+=("${container}")
    fi
  done
  echo ''

  [[ "${#all[@]}" -gt 0 ]] && timeout $$ 90

  for container in ${all[*]}; do
    status=$(getStatus "${container}")
    if [ "${status}" = "\"running\"" ]; then
      echo -e "\033[0;34m⠿ Stopping container ${container} \033[0;0;0m"
      pushd "composes/${container}" &>/dev/null || exit 1
      if docker compose rm --stop --force; then
        assertStatus "${container}" "exited"
        echo ''
      else
        echo -e "\033[0;31m⠿ Docker (docker compose rm) command failed! \033[0;0;0m\n"
      fi
      popd &>/dev/null || exit 1
    else
      echo -e "\033[0;34m⠿ Container \"${container}\" is not up\033[0;0;0m"
    fi
  done
}

echo ''
stopContainers
