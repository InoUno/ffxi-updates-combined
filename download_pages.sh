#!/usr/bin/bash

wget --page-requisites --convert-links  --execute robots=off --adjust-extension --directory-prefix downloads --user-agent=Mozilla --wait=0.2 --input-file relevant_links.txt
