#!/usr/bin/env bash

# VT-100 Terminal colors
NC=${NC:-'\033[0;0;0m'}
RED=${RED:-'\033[0;31m'}
GREEN=${GREEN:-'\033[0;32m'}
BLUE=${BLUE:-'\033[0;34m'}
YELLOW=${YELLOW:-'\033[0;93m'}

# @purpose: Start a timer. After the specified timeout, the process specified is killed.
# -param $1: the PID of the process
# -param $2: the timeout in seconds
timeout() {
  pid="${1}"
  timeout="${2}"
  echo -e "${BLUE}⠿ Timeout activated -> pid=${pid}, timeout=${timeout}s $(date)\n ${NC}"
  (
    ((t = timeout))
    while ((t > 0)); do
      sleep 1
      kill -0 "${pid}" || exit 0
      ((t -= 1))
    done
    echo -e "\n${RED}⠿ Timed out! Killing pid=${pid} ${NC} $(date)\n"
    kill -s SIGTERM "${pid}" && kill -0 "${pid}" || exit 0
    sleep 1
    kill -s SIGKILL "${pid}"
  ) 2>/dev/null &
}

# @purpose: Inspect a container using the specified json format
# -param $1: the docker container name
# -param $2: the json field to inspect
inspectContainer() {
  status=$(docker container inspect --format "{{json ${2} }}" "${1}" 2> /dev/null)
  ret=$!
  echo "${status}"
  return $ret
}

# @purpose: Get the docker container health
# -param $1: the docker container name
getHealth() {
  inspectContainer "${1}" '.State.Health.Status'
}

# @purpose: Get the docker container status
# -param $1: the docker container name
getStatus() {
  inspectContainer "${1}" '.State.Status'
}

# @purpose: Wait for a docker container to start and become healthy; fail otherwise
# -param $1: the container names to wait to be healthy
waitHealthy() {
  local status all=() done=()
  all=("$@")
  echo -en "${BLUE}⠿ Waiting all containers [$(echo " ${all[*]}" | awk '{gsub(/ /,"\n  |- ")}1')\n] to become healthy "
  while [ ${#all[@]} -gt ${#done[@]} ]; do
    for nextContainer in "${all[@]}"; do
      status=$(getHealth "${nextContainer}")
      [[ "${status}" == "\"healthy\"" ]] && done+=("${nextContainer}")
    done
    sleep 1 && echo -n "."
  done
  echo -e "${GREEN} ⠿ OK ⠿${NC}\n"
  return 0
}

# @purpose: Assert a docker container status. If the status is different exit with error code.
# -param $1: the docker container name
# -param $2: the expected status
assertStatus() {
  status=$(getStatus "$1")
  if [[ "${status}" != "\"$2\"" ]]; then
    echo -e "${RED}⠿ Status assertion failed. Expecting ${2} but got ${status}${NC}\n"
    exit 1
  fi
}

# @purpose: Quit and exhibits an exit message if specified.
# @param $1 [Req] : The exit return code.
# @param $2 [Opt] : The exit message to be displayed.
quit() {
  test "$1" != '0' -a "$1" != '1' && echo -e "${RED}"
  test -n "$2" -a "$2" != "" && echo -e "${2}"
  test "$1" != '0' -a "$1" != '1' && echo -e "${NC}"
  echo ''
  exit "$1"
}
