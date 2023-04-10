#!/usr/bin/env bash

# shellcheck disable=SC1091
source "docker-tools-inc.sh"

RUNNING_CONTAINERS=$(docker ps --format '{{.Names}}' | tr '\n' ' ')
[[ "${#RUNNING_CONTAINERS[@]}" -eq 0 ]] && exit 0

# @purpose: Stop all docker-compose.yml
# -param $1: if the execution is on an interactive console or not
stopContainers() {
  local all=() container count

  for container in ${RUNNING_CONTAINERS}; do
    read -r -n 1 -p "Stop container ${container} (y/[n]): " ANS
    test -n "${ANS}" && echo ''
    if [[ "${ANS}" == 'y' || "${ANS}" == 'Y' ]]; then
      all+=("${container}")
    fi
  done
  echo ''

  count=${#all[@]}
  [[ "${count}" -gt 0 ]] && timeout $$ $((count * 30))

  for container in "${all[@]}"; do
    status=$(getStatus "${container}")
    if [[ "${status}" == "\"running\"" ]]; then
      echo -en "${BLUE}⠿ Stopping container ${container} ${NC}"
      id=$(docker ps -aqf "name=${container}")
      if docker stop "${id}" &>/dev/null; then
        assertStatus "${container}" "exited"
        if docker rm "${id}" &>/dev/null; then echo -e "${GREEN}⠿ OK ⠿"; else echo "${RED}⠿ FAILED ⠿"; fi
      else
        echo -e ' ⠿ FAILED ⠿'
      fi
    else
      echo -e "${ORANGE}⠿ Container \"${container}\" is not up"
    fi
  done
  echo -e "${NC}"
}

stopContainers
