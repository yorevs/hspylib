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
      echo -e "${YELLOW}⠿ Container \"${container}\" is already up${NC}"
    else
      echo -e "${BLUE}⠿ Container ${container} is ${status}"
      echo -e "⠿ Starting container ${container} ${NC}"
      pushd "composes/${container}" &>/dev/null || exit 1
      if docker compose up --force-recreate --build --remove-orphans --detach; then
        waitHealthy "${container}"
        echo ''
      else
        echo -e "${RED}⠿ Docker (docker compose up) command failed! ${NC}\n"
      fi
      popd &>/dev/null || exit 1
    fi
  done
}

echo ''
startContainers
