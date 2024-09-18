#!/usr/bin/env bash

# shellcheck disable=SC1091
source "docker-tools-inc.sh"

CONTAINERS_DIR=${CONTAINERS_DIR:-./composes}
pushd "${CONTAINERS_DIR}" &> /dev/null || exit 1
# shellcheck disable=SC2206
COMPOSES=(${1:-$(find . -maxdepth 1 ! -path . -type d | cut -c3-)})
popd &> /dev/null || exit 1
[[ "${#COMPOSES[@]}" -eq 0 ]] && exit 0

DOCKER_FLAGS=('--force-recreate' '--build' '--remove-orphans' '--detach')

# @purpose: Start all docker-compose.yml
# -param $1: if the execution is on an interactive console or not
startContainers() {
  local all=() container

  if [[ ${#COMPOSES[@]} -gt 1 ]]; then
    for container in "${COMPOSES[@]}"; do
      read -r -n 1 -p "Start container ${container} (y/[n]): " ANS
      test -n "${ANS}" && echo ''
      if [[ "${ANS}" =~ ^[yY]$ ]]; then
        all+=("${container}")
      fi
    done
  else
    all+=("${COMPOSES[0]}")
  fi
  echo ''

  for container in "${all[@]}"; do
    status=$(getHealth "${container}")
    if [[ "${status}" == "\"healthy\"" ]]; then
      echo -e "${YELLOW}⠿ Container \"${container}\" is already up${NC}"
    else
      echo -e "${BLUE}⠿ Container ${container} is ${status:-down}"
      echo -e "⠿ Starting container ${container} ${NC}"
      pushd "${CONTAINERS_DIR}/${container}" &>/dev/null || exit 1
      if docker compose up "${DOCKER_FLAGS[@]}"; then
        echo ''
      else
        echo -e "${RED}⠿ Docker (docker compose up) command failed! ${NC}\n"
      fi
      popd &>/dev/null || exit 1
    fi
  done

  # shellcheck disable=SC2207
  all=($(docker ps --format '{{.Names}}'))
  count=${#all[@]}
  [[ "${count}" -gt 0 ]] && timeout $$ $((count * 120))
  waitHealthy "${all[@]}"
}

echo ''
startContainers
