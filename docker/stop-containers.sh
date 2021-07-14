#!/usr/bin/env bash

source "docker-tools.sh"

ALL_CONTAINERS=${ALL_CONTAINERS:-$(find . -maxdepth 1 ! -path . -type d | cut -c3-)}

# @purpose: TODO
stopContainers() {
  all=()

  if [[ $- == *i* ]]; then
    for container in ${ALL_CONTAINERS}; do
      read -r -n 1 -p "Stop container ${container} (y/[n]): " ANS
      test -n "${ANS}" && echo ''
      if [[ "${ANS}" == 'y' || "${ANS}" == 'Y' ]]; then
        all+=("${container}")
      fi
    done
    echo ''
  else
    all=("${ALL_CONTAINERS[*]}")
  fi

  for container in ${all[*]}; do
    status=$(getStatus "${container}")
    if [ "${status}" = "\"running\"" ]; then
      echo -e "\033[0;34m⠿ Stopping container ${container} \033[0;0;0m"
      pushd "${container}" &>/dev/null || exit 1
      docker compose rm --stop --force
      assertStatus "${container}" "exited"
      echo ''
      popd &>/dev/null || exit 1
    else
      echo -e "\033[0;34m⠿ Container \"${container}\" is not up\033[0;0;0m"
    fi
  done
}

echo "Stopping docker containers ${ALL_CONTAINERS}"
stopContainers
echo ''
