CONTAINER_IDS="$(docker ps -a --no-trunc -q)"


for ID in $CONTAINER_IDS; do
	cp /dev/null "/var/lib/docker/containers/${ID}/${ID}-json.log"
	#echo "$ID"
done


echo "Docker logs resetted"
