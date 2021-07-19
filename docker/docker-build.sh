#!/usr/bin/env bash

USAGE="
    Usage: build.bash <container-name>

      Arguments
        - container-name  : The docker container directory name (dirname). Must contain a Dockerfile inside.
"

if [[ $# -lt 1 || "${1}" == -h || "${1}" == --help ]]; then
  echo "${USAGE}"
else
  echo -n 'Changing directory => '
  pushd 'images' || exit 1
  container_dirs="$(find . -type d -mindepth 1 | tr '\n' ' ')"
  container_dirs="${container_dirs//\.\//}"
  for next_container in "${@}"; do
    if [[ "${container_dirs}" == *"${next_container}"* ]]; then
      if ! [[ -d "${next_container}/" && -f "${next_container}/Dockerfile" ]]; then
        echo -e "${RED}Unable to find directory: ${next_container}/${NC}"
        exit 1
      fi
      echo ''
      echo -e "${PURPLE}Building ${BLUE}[${next_container}] ... ${NC}"
      echo ''
      [[ -d "${next_container}/" ]] && docker build -t "yorevs/hhs-${next_container}" "${next_container}/"
    else
      echo "${RED}Invalid container type: \"${next_container}\". Please use one of [${container_dirs}] ! ${NC}"
    fi
  done
  echo -n 'Changing directory => '
  popd && echo '' || exit 1
fi
