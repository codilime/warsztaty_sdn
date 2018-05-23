curl -X POST http://172.20.128.10:8090/remove/logical_port --data '{"net_id": "red", "container": {"id": "sdn_agent_ala_1", "ip":"172.20.128.1"}}' -H "Content-Type: application/json"
