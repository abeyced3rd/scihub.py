# SciHub Web App - Deployment Guide

This guide covers multiple ways to deploy the SciHub Web Application.

## Quick Start (Local Development)

### Option 1: Using the Start Script (Recommended for beginners)

```bash
chmod +x start.sh
./start.sh
```

The application will start on `http://localhost:5000`

### Option 2: Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create downloads folder
mkdir -p downloads

# Run the app
python run.py
```

---

## Docker Deployment (Recommended for production)

### Prerequisites
- Docker installed on your system
- Docker Compose (optional, for easier management)

### Using Docker Compose (Easiest)

```bash
# Build and run the container
docker-compose up

# In the background
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f
```

The application will be available at `http://localhost:5000`

Downloaded papers will be stored in `./downloads/` on your host machine.

### Using Docker CLI

```bash
# Build the image
docker build -t scihub-web .

# Run the container
docker run -p 5000:5000 -v $(pwd)/downloads:/app/downloads scihub-web

# Run in background
docker run -d -p 5000:5000 -v $(pwd)/downloads:/app/downloads --name scihub-web scihub-web

# Stop the container
docker stop scihub-web

# View logs
docker logs scihub-web
```

---

## Cloud Deployment

### Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Procfile**
   ```bash
   echo "web: python run.py" > Procfile
   ```

4. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

5. **Access your app**
   ```
   https://your-app-name.herokuapp.com
   ```

### AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB application**
   ```bash
   eb init -p python-3.11 scihub-web
   ```

3. **Create environment and deploy**
   ```bash
   eb create production
   eb deploy
   ```

4. **Open your app**
   ```bash
   eb open
   ```

### Google Cloud Run

1. **Build and push Docker image**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/scihub-web
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy scihub-web \
     --image gcr.io/YOUR-PROJECT-ID/scihub-web \
     --platform managed \
     --region us-central1
   ```

### DigitalOcean App Platform

1. **Connect your GitHub repository**
2. **Go to App Platform** → **Create App**
3. **Set build command**: `pip install -r requirements.txt`
4. **Set run command**: `python run.py`
5. **Deploy**

---

## Production Configuration

### Using Gunicorn (Recommended for Production)

Instead of using Flask's development server, use Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Update `Procfile` for Heroku:
```
web: gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

Create a `.env` file:
```
FLASK_ENV=production
DEBUG=False
```

### Reverse Proxy with Nginx

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/TLS with Let's Encrypt

```bash
# Using Certbot
sudo certbot certonly --nginx -d your-domain.com
```

Update Nginx configuration for HTTPS:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Linux Server Setup (VPS/Dedicated Server)

### Ubuntu/Debian

1. **Update system**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python and dependencies**
   ```bash
   sudo apt install python3.11 python3.11-venv python3-pip nginx -y
   ```

3. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scihub.py.git
   cd scihub.py
   ```

4. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

5. **Install requirements**
   ```bash
   pip install -r requirements.txt gunicorn
   ```

6. **Create systemd service file**
   ```bash
   sudo nano /etc/systemd/system/scihub.service
   ```

   Add the following:
   ```ini
   [Unit]
   Description=SciHub Web Application
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/home/youruser/scihub.py
   ExecStart=/home/youruser/scihub.py/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Enable and start service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable scihub
   sudo systemctl start scihub
   ```

8. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/scihub
   ```

   Add the configuration from the Nginx section above.

9. **Enable Nginx site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/scihub /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## Monitoring and Maintenance

### Check Application Status

```bash
# Docker
docker ps
docker logs scihub-web

# Systemd
sudo systemctl status scihub
sudo journalctl -u scihub -f
```

### Backup Downloads

```bash
# Backup downloads folder
tar -czf scihub-backup-$(date +%Y%m%d).tar.gz downloads/

# Restore from backup
tar -xzf scihub-backup-20240101.tar.gz
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt

# Restart application
docker-compose restart
# or
sudo systemctl restart scihub
```

---

## Performance Optimization

### Increase Worker Count

For Gunicorn, increase workers based on CPU cores:
```bash
gunicorn -w $(nproc) -b 0.0.0.0:5000 app:app
```

### Enable Caching

Add to `app.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Database for Downloads Metadata

Consider using SQLite or PostgreSQL to track downloads instead of just listing files.

---

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Connection Timeout
- Check firewall settings
- Verify server is running
- Check network connectivity
- Review application logs

### High Memory Usage
- Reduce number of Gunicorn workers
- Enable file size limits in Flask
- Monitor with `docker stats`

---

## Security Checklist

- [ ] Run behind HTTPS
- [ ] Use strong firewall rules
- [ ] Keep dependencies updated
- [ ] Set proper file permissions
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted origins
- [ ] Implement rate limiting
- [ ] Regular backups
- [ ] Monitor logs for suspicious activity

---

## Support & Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

Happy deploying! 🚀
