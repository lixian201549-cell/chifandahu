const path = require('path');

module.exports = {
  apps: [
    {
      name: 'platform-backend',
      script: 'backend_server.py',
      interpreter: 'python3',
      cwd: __dirname,
      autorestart: true,
      watch: ['backend_server.py'],
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
      name: 'platform-tunnel',
      script: 'tunnel_only.py',
      interpreter: 'python3',
      cwd: __dirname,
      autorestart: true,
      watch: false,
      restart_delay: 3000,
      max_memory_restart: '200M'
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
