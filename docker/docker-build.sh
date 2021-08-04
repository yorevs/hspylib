#!/usr/bin/env bash

source "docker-tools-inc.sh"

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
      echo -e "Building docker image: ${GREEN}[${next_container}] ${NC} ... "
      echo ''
      if [[ -d "${next_container}/" ]]; then
        if docker build -t "yorevs/hhs-${next_container}:latest" "${next_container}/"; then
          if docker image push "yorevs/hhs-${next_container}:latest"; then
            echo -e "${GREEN}Successfully built and pushed docker image: \"yorevs/hhs-${next_container}:latest\" ! ${NC}"
          else
            echo -e "${RED}Failed to push docker image: \"yorevs/hhs-${next_container}:latest\" ! ${NC}"
          fi
        else
          echo -e "${RED}Failed to build docker image: \"yorevs/hhs-${next_container}\" ! ${NC}"
        fi
      fi
    else
      echo -e "${RED}Invalid container type: \"${next_container}\". Please use one of [${container_dirs}] ! ${NC}"
    fi
  done
  popd && echo '' || exit 1
fi
