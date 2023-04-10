#!/usr/bin/env bash

# shellcheck disable=SC1091
source "docker-tools-inc.sh"

pushd 'composes/' &> /dev/null || exit 1
COMPOSES=${COMPOSES:-$(find . -maxdepth 1 ! -path . -type d | cut -c3-)}
popd &> /dev/null || exit 1
[[ "${#COMPOSES[@]}" -eq 0 ]] && exit 0

DOCKER_FLAGS=('--force-recreate' '--build' '--remove-orphans' '--detach')

# @purpose: Start all docker-compose.yml
# -param $1: if the execution is on an interactive console or not
startContainers() {
  local all=() container

  for container in ${COMPOSES}; do
    read -r -n 1 -p "Start container ${container} (y/[n]): " ANS
    test -n "${ANS}" && echo ''
    if [[ "${ANS}" == 'y' || "${ANS}" == 'Y' ]]; then
      all+=("${container}")
    fi
  done
  echo ''

  for container in ${all[*]}; do
    status=$(getHealth "${container}")
    if [[ "${status}" == "\"healthy\"" ]]; then
      echo -e "${YELLOW}⠿ Container \"${container}\" is already up${NC}"
    else
      echo -e "${BLUE}⠿ Container ${container} is ${status}"
      echo -e "⠿ Starting container ${container} ${NC}"
      pushd "composes/${container}" &>/dev/null || exit 1
      if docker compose up ${DOCKER_FLAGS[*]}; then
        echo ''
      else
        echo -e "${RED}⠿ Docker (docker compose up) command failed! ${NC}\n"
      fi
      popd &>/dev/null || exit 1
    fi
  done

  all=($(docker ps --format '{{.Names}}'))
  count=${#all[@]}
  [[ "${count}" -gt 0 ]] && timeout $$ $((count * 60))
  waitHealthy "${all[@]}"
}

echo ''
startContainers
