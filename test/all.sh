#!/bin/bash

set -e

$(dirname $0)/image.sh
$(dirname $0)/check.sh
$(dirname $0)/get.sh
$(dirname $0)/put.sh

echo -e 'all tests passed!'
