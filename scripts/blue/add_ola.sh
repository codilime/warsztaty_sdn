curl -X POST http://172.20.128.10:8090/create/logical_port --data '{"net_id": "blue", "container": {"id": "sdn_agent_ola_1", "ip":"172.20.128.2"}}' -H "Content-Type: application/json"
