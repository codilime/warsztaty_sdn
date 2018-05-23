#!/bin/bash
docker ps | grep ssh | awk '{print $1}' | xargs -l docker inspect | grep '"IPAddress":' | grep -v '""'