#!/bin/bash

set -e


it_has_installed_proxytunnel() {
  test -x /usr/bin/proxytunnel
}

it_cleans_up_installation_artifacts() {
  test ! -d /root/proxytunnel
}

it_has_installed_proxytunnel
it_cleans_up_installation_artifacts

echo -e "image tests passed!"
echo -e "--------------------------------------------"
