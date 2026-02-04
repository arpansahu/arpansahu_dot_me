# Backend Services (Docker Containers)

- **PostgreSQL 16** with SSL/TLS (Let's Encrypt) - Port 9552 external
- **Redis 7** with TLS (Let's Encrypt) - Port 9551 external  
- **PgAdmin 4** - Web UI for PostgreSQL management
- **Portainer CE** - Docker/Kubernetes management
- **MinIO** - S3-compatible object storage (single bucket: arpansahu-one-bucket)
- **Harbor v2.11.0** - Container registry
- **Jenkins 2.541** - CI/CD automation (systemd service)

All services use Let's Encrypt wildcard SSL certificate for *.arpansahu.space via acme.sh with Namecheap DNS-01 validation.
