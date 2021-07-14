# @purpose: Inspect a container using the specified json format
# -param $1: the docker container name
# -param $2: the json field to inspect
inspectContainer() {
  docker container inspect --format "{{json $2 }}" "$1" 2> /dev/null
}

# @purpose: Get the docker container health
# -param $1: the docker container name
getHealth() {
  inspectContainer "$1" '.State.Health.Status'
}

# @purpose: Get the docker container status
# -param $1: the docker container name
getStatus() {
  inspectContainer "$1" '.State.Status'
}

# @purpose: Wait for a docker container to start and become healthy; fail otherwise
# -param $1: the docker container name
waitHealthy() {
  local status
  status=$(getHealth "$1")
  echo -en '\033[0;34m ⠿ Waiting container to become healthy '
  while [ "${status}" != "\"healthy\"" ]; do
    if [[ "${status}" == "\"unhealthy\"" ]]; then
      echo -e '\033[0;31m⠿ [Failed]\033[0;0;0m\n'
      return 1
    fi
    status=$(getHealth "$1")
    echo -n "."
    sleep 1
  done
  echo -e '[  OK  ]\033[0;0;0m\n'

  return 0
}

# @purpose: Assert a docker container status. If the status is different exit with error code.
# -param $1: the docker container name
# -param $2: the expected status
assertStatus() {
  status=$(getStatus "$1")
  if [[ "${status}" != "\"$2\"" ]]; then
      echo -e "\033[0;31m⠿ Status assertion failed. Expecting ${2} but got ${status}\033[0;0;0m\n"
      exit 1
  fi
}
