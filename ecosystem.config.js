// PM2 Ecosystem Configuration
// Manages all AI Employee processes

module.exports = {
  apps: [
    {
      name: 'orchestrator',
      script: 'python',
      args: 'src/orchestrator.py vault/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production'
      },
      error_file: 'vault/Logs/orchestrator-error.log',
      out_file: 'vault/Logs/orchestrator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'gmail-watcher',
      script: 'python',
      args: 'src/watchers/gmail_watcher.py vault/ credentials.json',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      error_file: 'vault/Logs/gmail-watcher-error.log',
      out_file: 'vault/Logs/gmail-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'filesystem-watcher',
      script: 'python',
      args: 'src/watchers/filesystem_watcher.py vault/ vault/Drop/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'vault/Logs/filesystem-watcher-error.log',
      out_file: 'vault/Logs/filesystem-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'whatsapp-watcher',
      script: 'python',
      args: 'src/watchers/whatsapp_watcher.py vault/ .whatsapp_session/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      error_file: 'vault/Logs/whatsapp-watcher-error.log',
      out_file: 'vault/Logs/whatsapp-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'linkedin-watcher',
      script: 'python',
      args: 'src/watchers/linkedin_watcher.py vault/ .linkedin_session/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      error_file: 'vault/Logs/linkedin-watcher-error.log',
      out_file: 'vault/Logs/linkedin-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'facebook-watcher',
      script: 'python',
      args: 'src/watchers/facebook_watcher.py vault/ .facebook_session/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      error_file: 'vault/Logs/facebook-watcher-error.log',
      out_file: 'vault/Logs/facebook-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'instagram-watcher',
      script: 'python',
      args: 'src/watchers/instagram_watcher.py vault/ .instagram_session/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      error_file: 'vault/Logs/instagram-watcher-error.log',
      out_file: 'vault/Logs/instagram-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'twitter-watcher',
      script: 'python',
      args: 'src/watchers/twitter_watcher.py vault/ .twitter_session/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      error_file: 'vault/Logs/twitter-watcher-error.log',
      out_file: 'vault/Logs/twitter-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'process-monitor',
      script: 'python',
      args: 'src/process_monitor.py vault/',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'vault/Logs/process-monitor-error.log',
      out_file: 'vault/Logs/process-monitor-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'linkedin-poster',
      script: 'python',
      args: 'src/linkedin_poster.py vault/ .linkedin_session/',
      interpreter: 'none',
      autorestart: false,
      cron_restart: '0 9 * * *',
      watch: false,
      error_file: 'vault/Logs/linkedin-poster-error.log',
      out_file: 'vault/Logs/linkedin-poster-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    }
  ]
};
