#!/bin/bash
# scripts/schedule-sweep.sh
# Helper script to set up scheduled sweeps using cron or PM2

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

show_help() {
    cat << EOF
AetherCrown20 Sweep Scheduler

Usage: ./scripts/schedule-sweep.sh [OPTIONS]

Options:
    --cron          Set up cron job for daily sweeps
    --pm2           Set up PM2 for continuous monitoring
    --systemd       Generate systemd service file
    --help          Show this help message

Examples:
    # Set up daily cron job at 2 AM
    ./scripts/schedule-sweep.sh --cron

    # Set up PM2 monitoring
    ./scripts/schedule-sweep.sh --pm2

    # Generate systemd service file
    ./scripts/schedule-sweep.sh --systemd

EOF
}

setup_cron() {
    echo "Setting up cron job for daily sweeps..."
    
    CRON_COMMAND="0 2 * * * cd $PROJECT_DIR && npm run sweep >> /tmp/aether-sweep.log 2>&1"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "aether-sweep"; then
        echo "⚠️  Cron job already exists. Remove it first if you want to update."
        return 1
    fi
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -
    
    echo "✅ Cron job added successfully!"
    echo "   Schedule: Daily at 2 AM"
    echo "   Log file: /tmp/aether-sweep.log"
    echo ""
    echo "To view cron jobs: crontab -l"
    echo "To remove: crontab -e (and delete the line)"
}

setup_pm2() {
    echo "Setting up PM2 for continuous monitoring..."
    
    # Check if PM2 is installed
    if ! command -v pm2 &> /dev/null; then
        echo "PM2 not found. Installing globally..."
        npm install -g pm2
    fi
    
    cd "$PROJECT_DIR"
    
    # Stop existing process if any
    pm2 delete aether-sweep 2>/dev/null || true
    
    # Start as cron job (daily at 2 AM)
    pm2 start ai-agent-sweep.js \
        --name aether-sweep \
        --cron "0 2 * * *" \
        --no-autorestart
    
    # Save PM2 process list
    pm2 save
    
    # Setup PM2 startup script
    pm2 startup || echo "⚠️  Run the command above to enable PM2 on system startup"
    
    echo "✅ PM2 setup complete!"
    echo "   View logs: pm2 logs aether-sweep"
    echo "   View status: pm2 status"
    echo "   Stop: pm2 stop aether-sweep"
}

setup_systemd() {
    echo "Generating systemd service file..."
    
    SERVICE_FILE="$PROJECT_DIR/aether-sweep.service"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=AetherCrown20 AI Agent Sweep
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/node $PROJECT_DIR/ai-agent-sweep.js
StandardOutput=append:/var/log/aether-sweep.log
StandardError=append:/var/log/aether-sweep.error.log

# Load environment variables
EnvironmentFile=$PROJECT_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

    TIMER_FILE="$PROJECT_DIR/aether-sweep.timer"
    
    cat > "$TIMER_FILE" << EOF
[Unit]
Description=AetherCrown20 AI Agent Sweep Timer
Requires=aether-sweep.service

[Timer]
# Run daily at 2 AM
OnCalendar=daily
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

    echo "✅ Systemd files generated!"
    echo ""
    echo "Service file: $SERVICE_FILE"
    echo "Timer file: $TIMER_FILE"
    echo ""
    echo "To install:"
    echo "  sudo cp $SERVICE_FILE /etc/systemd/system/"
    echo "  sudo cp $TIMER_FILE /etc/systemd/system/"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable aether-sweep.timer"
    echo "  sudo systemctl start aether-sweep.timer"
    echo ""
    echo "To check status:"
    echo "  sudo systemctl status aether-sweep.timer"
    echo "  sudo systemctl list-timers"
}

# Parse command line arguments
case "${1:-}" in
    --cron)
        setup_cron
        ;;
    --pm2)
        setup_pm2
        ;;
    --systemd)
        setup_systemd
        ;;
    --help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
