export default {
  title: 'Networks',
  url: '/networks',
  schema: {
    type: 'object',
    properties: {
      id: {
        type: 'string',
        title: 'Network ID',
      },
      ip: {
        type: 'string',
        title: 'IP address'
      },
    },
    required: [
      'id',
      'ip'
    ]
  },
};
