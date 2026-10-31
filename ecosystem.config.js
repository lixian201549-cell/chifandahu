const path = require('path');

module.exports = {
  apps: [
    {
      name: 'platform-service',
      script: 'serve_tunnel.py',
      interpreter: 'python3',
      cwd: __dirname,
      autorestart: true,
      watch: ['backend_server.py', 'serve_tunnel.py'],
      ignore_watch: [
        'node_env',
        'data',
        'dist',
        'scratch',
        '*.log',
        '*.txt',
        '*.db*'
      ],
      max_memory_restart: '500M'
    },
    {
      name: 'platform-auto-compiler',
      script: 'auto_compiler.py',
      interpreter: 'python3',
      cwd: __dirname,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M'
    }
  ]
};
