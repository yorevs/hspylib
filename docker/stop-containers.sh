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
      echo -e "${BLUE}⠿ Stopping container ${container} \${NC}"
      pushd "composes/${container}" &>/dev/null || exit 1
      if docker compose rm --stop --force; then
        assertStatus "${container}" "exited"
        echo ''
      else
        echo -e "${RED}⠿ Docker (docker compose rm) command failed! \${NC}\n"
      fi
      popd &>/dev/null || exit 1
    else
      echo -e "${BLUE}⠿ Container \"${container}\" is not up\${NC}"
    fi
  done
}

echo ''
stopContainers
