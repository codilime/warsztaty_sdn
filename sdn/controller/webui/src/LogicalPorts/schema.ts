export default {
  title: 'LogicalPorts',
  url: '/logical_ports',
  schema: {
    type: 'object',
    properties: {
      container: {
        type: 'object',
        properties: {
          id: {
            type: 'string',
            title: 'Container ID'
          }
        },
        required: [
          'id'
        ]
      },
      net_id: {
        type: 'string',
        title: 'Network ID'
      },
    },
    required: [
      'id',
      'container_id',
      'net_id'
    ]
  },
};
