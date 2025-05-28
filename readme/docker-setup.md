# Complete Docker Guide: PostgreSQL pgvector, Ollama & Open WebUI Management

This comprehensive guide provides detailed instructions for managing PostgreSQL with pgvector, Ollama language models, and Open WebUI using Docker Desktop on Windows with PowerShell commands.

## Table of Contents

1. [Prerequisites & System Requirements](#prerequisites--system-requirements)
2. [PostgreSQL pgvector Setup](#postgresql-pgvector-setup)
3. [Ollama Docker Setup](#ollama-docker-setup)
4. [Open WebUI Setup](#open-webui-setup)
5. [PostgreSQL Management Operations](#postgresql-management-operations)
6. [Ollama Management Operations](#ollama-management-operations)
7. [Open WebUI Management Operations](#open-webui-management-operations)
8. [Advanced Configuration & Integration](#advanced-configuration--integration)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Complete Cleanup Procedures](#complete-cleanup-procedures)
11. [Best Practices & Resources](#best-practices--resources)

---

## Prerequisites & System Requirements

### Common Requirements

| Component                      | Description                     | Notes                                 |
| ------------------------------ | ------------------------------- | ------------------------------------- |
| **Docker Desktop for Windows** | Installed and running           | Required for all services             |
| **Windows PowerShell**         | Command execution environment   | All commands designed for PowerShell  |
| **Internet Connection**        | Active connection for downloads | Required for Docker images and models |
| **Sufficient Disk Space**      | 50GB+ recommended               | All services + models can be large    |

### PostgreSQL pgvector Requirements

| Resource              | Requirement    | Purpose                         |
| --------------------- | -------------- | ------------------------------- |
| **RAM**               | 4GB+ available | Database operations and queries |
| **Disk Space**        | 10GB+ free     | Database storage and backups    |
| **Port Availability** | Port 5432 free | PostgreSQL default port         |

### Ollama Specific Requirements

| Resource                     | Requirement                     | Purpose                       |
| ---------------------------- | ------------------------------- | ----------------------------- |
| **RAM**                      | 8GB+ available                  | Model loading and inference   |
| **GPU (Recommended)**        | NVIDIA GPU with current drivers | Accelerated model performance |
| **NVIDIA Container Toolkit** | For Linux users                 | GPU access in containers      |
| **Port Availability**        | Port 11434 free                 | Ollama API server             |

### Open WebUI Requirements

| Resource              | Requirement    | Purpose                            |
| --------------------- | -------------- | ---------------------------------- |
| **RAM**               | 2GB+ available | Web interface and user sessions    |
| **Disk Space**        | 5GB+ free      | User data and conversation history |
| **Port Availability** | Port 3001 free | Web interface access               |
| **GPU (Optional)**    | NVIDIA GPU     | Enhanced UI performance            |

---

## PostgreSQL pgvector Setup

### Step 1: Clean Up Previous PostgreSQL Installation (If Needed)

**Warning:** These commands will permanently delete data. Backup important data first.

| Step                       | Command (PowerShell)                               | Explanation                             |
| -------------------------- | -------------------------------------------------- | --------------------------------------- |
| **1. List All Containers** | `docker ps -a`                                     | Identify existing PostgreSQL containers |
| **2. Stop Container**      | `docker stop [container_name_or_id]`               | Stop the target PostgreSQL container    |
| **3. Remove Container**    | `docker rm [container_name_or_id]`                 | Remove the stopped container            |
| **4. List Images**         | `docker images`                                    | Identify PostgreSQL images              |
| **5. Remove Image**        | `docker rmi [image_name]:[tag]`                    | Remove PostgreSQL image                 |
| **6. List Volumes**        | `docker volume ls`                                 | Identify associated volumes             |
| **7. Remove Volumes**      | `docker volume rm [volume_name_1] [volume_name_2]` | Delete data volumes                     |

#### System Cleanup Options

| Cleanup Type      | Command                                                 | Description                                           |
| ----------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| **Comprehensive** | `docker system prune -a --volumes`                      | ⚠️ Removes all unused containers, images, and volumes |
| **Conservative**  | `docker system prune` followed by `docker volume prune` | Selective cleanup in two steps                        |

### Step 2: Install and Run pgvector

| Step                       | Command (PowerShell)                                                                                                                                        | Explanation                                             |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **1. Pull pgvector Image** | `docker pull pgvector/pgvector:0.8.0-pg17`                                                                                                                  | Download the pgvector-enabled PostgreSQL image          |
| **2. Run Container**       | `docker run -d --name postgres -e POSTGRES_PASSWORD=yoursecurepassword -p 5432:5432 -v pgvector_data:/var/lib/postgresql/data pgvector/pgvector:0.8.0-pg17` | **Replace `yoursecurepassword`** with a strong password |
| **3. Verify Status**       | `docker ps`                                                                                                                                                 | Confirm the container is running                        |
| **4. Check Logs**          | `docker logs postgres`                                                                                                                                      | Verify successful startup                               |

#### Container Parameters Explained

| Parameter                                            | Purpose              | Details                          |
| ---------------------------------------------------- | -------------------- | -------------------------------- |
| `-d`                                                 | Detached mode        | Runs container in background     |
| `--name postgres`                                    | Container naming     | Easy reference for commands      |
| `-e POSTGRES_PASSWORD=...`                           | Environment variable | Sets superuser password          |
| `-p 5432:5432`                                       | Port mapping         | Maps host port to container port |
| `-v postgres_pgvector_data:/var/lib/postgresql/data` | Volume mounting      | Persists database data           |

### Step 3: Connect and Enable pgvector Extension

**Connection Details:**

- **Host:** `localhost` or `127.0.0.1`
- **Port:** `5432`
- **Database:** `postgres`
- **User:** `postgres`
- **Password:** Your specified password

**Enable pgvector Extension:**

```sql
-- Connect to your database and run:
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation:
\dx
```

---

## Ollama Docker Setup

### Step 1: Download Ollama Image

```powershell
docker pull ollama/ollama
```

### Step 2: Run Ollama Container

#### With GPU Acceleration (Recommended)

```powershell
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

#### CPU Only (No GPU)

```powershell
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

#### Container Parameters Explained

| Parameter                 | Purpose          | Details                         |
| ------------------------- | ---------------- | ------------------------------- |
| `-d`                      | Detached mode    | Background execution            |
| `--gpus=all`              | GPU access       | Enables NVIDIA GPU acceleration |
| `-v ollama:/root/.ollama` | Volume mounting  | Persists models and config      |
| `-p 11434:11434`          | Port mapping     | API access port                 |
| `--name ollama`           | Container naming | Easy reference                  |

### Step 3: Run Your First Model

```powershell
docker exec -it ollama ollama run llama3.2:3b
```

**Note:** Verify model availability at [Ollama Library](https://ollama.com/library). Common alternatives: `llama3:8b`, `llama3:70b`

---

## Open WebUI Setup

### Step 1: Download Open WebUI Image

Choose between the standard and GPU-accelerated versions:

| Image Type          | Command (PowerShell)                             | Use Case                |
| ------------------- | ------------------------------------------------ | ----------------------- |
| **Standard**        | `docker pull ghcr.io/open-webui/open-webui:main` | CPU-only environments   |
| **GPU-Accelerated** | `docker pull ghcr.io/open-webui/open-webui:cuda` | NVIDIA GPU environments |

### Step 2: Run Open WebUI Container

#### With GPU Acceleration (Recommended)

```powershell
docker run -d -p 3001:8080 --gpus all -e WEBUI_AUTH=False -v webui:/app/backend/data --name webui ghcr.io/open-webui/open-webui:cuda
```

#### CPU Only Version

```powershell
docker run -d -p 3001:8080 -e WEBUI_AUTH=False -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

#### Container Parameters Explained

| Parameter                         | Purpose          | Details                                    |
| --------------------------------- | ---------------- | ------------------------------------------ |
| `-d`                              | Detached mode    | Background execution                       |
| `-p 3001:8080`                    | Port mapping     | Maps host port 3001 to container port 8080 |
| `--gpus all`                      | GPU access       | Enables NVIDIA GPU acceleration            |
| `-v open-webui:/app/backend/data` | Volume mounting  | Persists user data and settings            |
| `--name open-webui`               | Container naming | Easy reference for commands                |

### Step 3: Access Open WebUI

1. **Open Browser:** Navigate to `http://localhost:3001`
2. **Create Account:** Set up your first admin account
3. **Configure Ollama Connection:**
   - Go to Settings → Connections
   - Set Ollama API URL to `http://host.docker.internal:11434` (Windows) or `http://ollama:11434` (if using Docker network)

#### Initial Setup Checklist

| Step                     | Action                                     | Status |
| ------------------------ | ------------------------------------------ | ------ |
| **Access Web Interface** | Visit `http://localhost:3001`              | ⬜     |
| **Create Admin Account** | Set username and password                  | ⬜     |
| **Connect to Ollama**    | Configure API endpoint                     | ⬜     |
| **Test Model Access**    | Try a simple chat with downloaded model    | ⬜     |
| **Verify GPU Usage**     | Check NVIDIA-SMI if using GPU acceleration | ⬜     |

---

## PostgreSQL Management Operations

### Daily Operations

| Operation             | Command                                     | Description                |
| --------------------- | ------------------------------------------- | -------------------------- |
| **Stop Container**    | `docker stop postgres`                      | Stop PostgreSQL service    |
| **Start Container**   | `docker start postgres`                     | Start PostgreSQL service   |
| **Restart Container** | `docker restart postgres`                   | Restart PostgreSQL service |
| **View Logs**         | `docker logs postgres`                      | Check server logs          |
| **Access psql**       | `docker exec -it postgres psql -U postgres` | Direct database access     |
| **Container Shell**   | `docker exec -it postgres bash`             | Access container shell     |

### Database Operations

| Operation            | Command                                                      | Description         |
| -------------------- | ------------------------------------------------------------ | ------------------- |
| **Create Database**  | `docker exec -it postgres createdb -U postgres mydb`         | Create new database |
| **Drop Database**    | `docker exec -it postgres dropdb -U postgres mydb`           | Delete database     |
| **Backup Database**  | `docker exec postgres pg_dump -U postgres mydb > backup.sql` | Export database     |
| **Restore Database** | `docker exec -i postgres psql -U postgres mydb < backup.sql` | Import database     |

### Volume Management

| Operation          | Command                                                                                                                      | Description          |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **Inspect Volume** | `docker volume inspect postgres_pgvector_data`                                                                               | View volume details  |
| **List Volumes**   | `docker volume ls`                                                                                                           | Show all volumes     |
| **Backup Volume**  | `docker run --rm -v postgres_pgvector_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .` | Create volume backup |

---

## Ollama Management Operations

### Model Management

| Operation           | Command                                              | Description            |
| ------------------- | ---------------------------------------------------- | ---------------------- |
| **List Models**     | `docker exec ollama ollama list`                     | Show downloaded models |
| **Download Model**  | `docker exec ollama ollama pull <model_name:tag>`    | Download new model     |
| **Remove Model**    | `docker exec ollama ollama rm <model_name:tag>`      | Delete model           |
| **Show Model Info** | `docker exec ollama ollama show <model_name:tag>`    | Model details          |
| **Run Interactive** | `docker exec -it ollama ollama run <model_name:tag>` | Start chat session     |

### Container Operations

| Operation             | Command                 | Description            |
| --------------------- | ----------------------- | ---------------------- |
| **Stop Container**    | `docker stop ollama`    | Stop Ollama service    |
| **Start Container**   | `docker start ollama`   | Start Ollama service   |
| **Restart Container** | `docker restart ollama` | Restart Ollama service |
| **View Logs**         | `docker logs ollama`    | Check server logs      |
| **Monitor Resources** | `docker stats ollama`   | Resource usage         |

### API Operations

| Operation               | Example Command                                                                                                     | Description          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **List Models via API** | `curl http://localhost:11434/api/tags`                                                                              | Get available models |
| **Generate Text**       | `curl http://localhost:11434/api/generate -d '{"model": "llama3:8b", "prompt": "Hello", "stream": false}'`          | Text generation      |
| **Chat Completion**     | `curl http://localhost:11434/api/chat -d '{"model": "llama3:8b", "messages": [{"role": "user", "content": "Hi"}]}'` | Chat interaction     |

---

## Open WebUI Management Operations

### Container Operations

| Operation             | Command                     | Description                |
| --------------------- | --------------------------- | -------------------------- |
| **Stop Container**    | `docker stop open-webui`    | Stop Open WebUI service    |
| **Start Container**   | `docker start open-webui`   | Start Open WebUI service   |
| **Restart Container** | `docker restart open-webui` | Restart Open WebUI service |
| **View Logs**         | `docker logs open-webui`    | Check application logs     |
| **Monitor Resources** | `docker stats open-webui`   | Resource usage monitoring  |

### User Management

| Operation              | Access Method                   | Description               |
| ---------------------- | ------------------------------- | ------------------------- |
| **Admin Panel**        | Settings → Admin Panel          | User management interface |
| **Create User**        | Admin Panel → Users → Add User  | Add new user accounts     |
| **Reset Password**     | Admin Panel → Users → Edit User | Reset user passwords      |
| **View User Activity** | Admin Panel → Users → Activity  | Monitor user sessions     |
| **Export User Data**   | Admin Panel → Settings → Export | Backup user conversations |

### Configuration Management

| Configuration          | Location               | Description                    |
| ---------------------- | ---------------------- | ------------------------------ |
| **Model Connections**  | Settings → Connections | Configure AI model endpoints   |
| **Interface Settings** | Settings → Interface   | Customize UI appearance        |
| **Security Settings**  | Settings → Security    | Authentication and permissions |
| **Chat Settings**      | Settings → Chat        | Default chat behavior          |
| **Model Parameters**   | Settings → Models      | Default model configurations   |

### Data Management

| Operation            | Command/Method                                                                                                    | Description                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| **Backup User Data** | `docker run --rm -v open-webui:/data -v ${PWD}:/backup alpine tar czf /backup/openwebui_backup.tar.gz -C /data .` | Create complete data backup  |
| **Export Chats**     | Settings → Chats → Export All                                                                                     | Export conversation history  |
| **Import Chats**     | Settings → Chats → Import                                                                                         | Import conversation history  |
| **Reset Data**       | `docker volume rm open-webui` (after stopping container)                                                          | ⚠️ **Deletes all user data** |

---

## Advanced Configuration & Integration

### Running All Three Services Together

All services can run simultaneously in a complete AI stack:

```powershell
# Start PostgreSQL
docker start postgres

# Start Ollama
docker start ollama

# Start Open WebUI
docker start open-webui

# Verify all services are running
docker ps
```

### Port Configuration

| Service        | Default Port | Alternative Port Command                   |
| -------------- | ------------ | ------------------------------------------ |
| **PostgreSQL** | 5432         | `-p 5433:5432` (maps to host port 5433)    |
| **Ollama**     | 11434        | `-p 11435:11434` (maps to host port 11435) |
| **Open WebUI** | 3001         | `-p 3002:8080` (maps to host port 3002)    |

### Docker Compose Configuration

Create `docker-compose.yml` for managing all three services:

```yaml
version: "3.8"
services:
  postgres:
    image: pgvector/pgvector:0.8.0-pg17
    container_name: postgres
    environment:
      POSTGRES_PASSWORD: yoursecurepassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_pgvector_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - ai-stack

  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped
    networks:
      - ai-stack

  open-webui:
    image: ghcr.io/open-webui/open-webui:cuda
    container_name: open-webui
    ports:
      - "3001:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped
    networks:
      - ai-stack

volumes:
  postgres_pgvector_data:
  ollama:
  open-webui:

networks:
  ai-stack:
    driver: bridge
```

**Usage:**

```powershell
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs open-webui
```

### Integration Scenarios

#### Scenario 1: AI-Powered Application with Vector Database

**Use Case:** Building applications that combine LLM capabilities with vector similarity search

**Architecture:**

- **PostgreSQL + pgvector:** Store and search document embeddings
- **Ollama:** Generate embeddings and provide LLM capabilities
- **Open WebUI:** User interface for testing and interaction

#### Scenario 2: Complete AI Development Environment

**Use Case:** Development environment for AI applications with web interface

**Benefits:**

- Unified interface for model testing
- Persistent storage for conversations and data
- GPU acceleration across all AI workloads
- Easy model switching and comparison

---

## Troubleshooting Guide

### Common PostgreSQL Issues

| Problem                 | Symptoms                     | Solution                                                              |
| ----------------------- | ---------------------------- | --------------------------------------------------------------------- |
| **Connection Refused**  | Can't connect to database    | Check if container is running: `docker ps`                            |
| **Port Already in Use** | Port 5432 binding fails      | Use different port: `-p 5433:5432`                                    |
| **Permission Denied**   | Authentication failures      | Verify password and user credentials                                  |
| **Data Loss**           | Database empty after restart | Check volume mounting: `docker volume inspect postgres_pgvector_data` |

### Common Ollama Issues

| Problem                | Symptoms                | Solution                                                          |
| ---------------------- | ----------------------- | ----------------------------------------------------------------- |
| **Model Not Found**    | "model not found" error | Verify model name at [Ollama Library](https://ollama.com/library) |
| **Slow Performance**   | High response times     | Enable GPU acceleration or use smaller models                     |
| **CUDA Out of Memory** | GPU memory errors       | Use smaller models or increase GPU memory                         |
| **API Not Responding** | Connection timeouts     | Check container status and port mapping                           |

### Common Open WebUI Issues

| Problem                    | Symptoms                       | Solution                                               |
| -------------------------- | ------------------------------ | ------------------------------------------------------ |
| **Can't Access Interface** | Browser shows connection error | Verify container is running and port 3001 is available |
| **No Models Available**    | Empty model list in UI         | Check Ollama connection in Settings → Connections      |
| **Slow Response Times**    | UI feels sluggish              | Enable GPU acceleration and check system resources     |
| **Login Issues**           | Can't create account or login  | Check logs: `docker logs open-webui`                   |
| **Connection to Ollama**   | Models not responding          | Verify Ollama API URL is correct in settings           |

### Integration Issues

| Problem                        | Symptoms                      | Solution                                    |
| ------------------------------ | ----------------------------- | ------------------------------------------- |
| **Services Can't Communicate** | Open WebUI can't reach Ollama | Use Docker network or host.docker.internal  |
| **Port Conflicts**             | Services fail to start        | Change port mappings to avoid conflicts     |
| **GPU Not Detected**           | No GPU acceleration           | Check NVIDIA drivers and Docker GPU support |
| **Volume Permission Issues**   | Data not persisting           | Check volume mounts and permissions         |

### General Docker Issues

| Problem                    | Symptoms          | Solution                               |
| -------------------------- | ----------------- | -------------------------------------- |
| **Docker Not Running**     | Command failures  | Start Docker Desktop                   |
| **Insufficient Resources** | Container crashes | Allocate more RAM/disk space           |
| **Network Issues**         | Download failures | Check internet connection and firewall |
| **Permission Errors**      | Access denied     | Run PowerShell as Administrator        |

### Debugging Commands

```powershell
# Check Docker system status
docker system info

# Check available resources
docker system df

# View all containers
docker ps -a

# Inspect specific containers
docker inspect postgres
docker inspect ollama
docker inspect open-webui

# Check volume details
docker volume inspect postgres_pgvector_data
docker volume inspect ollama
docker volume inspect open-webui

# Monitor real-time logs
docker logs -f postgres
docker logs -f ollama
docker logs -f open-webui

# Check network connectivity
docker network ls
docker network inspect bridge
```

---

## Complete Cleanup Procedures

### PostgreSQL pgvector Cleanup

| Step                    | Command                                   | Description                      |
| ----------------------- | ----------------------------------------- | -------------------------------- |
| **1. Stop Container**   | `docker stop postgres`                    | Stop the running container       |
| **2. Remove Container** | `docker rm postgres`                      | Delete the container             |
| **3. Remove Volume**    | `docker volume rm postgres_pgvector_data` | ⚠️ **Deletes all database data** |
| **4. Remove Image**     | `docker rmi pgvector/pgvector`            | Remove the image                 |

### Ollama Cleanup

| Step                    | Command                    | Description                          |
| ----------------------- | -------------------------- | ------------------------------------ |
| **1. Stop Container**   | `docker stop ollama`       | Stop the running container           |
| **2. Remove Container** | `docker rm ollama`         | Delete the container                 |
| **3. Remove Volume**    | `docker volume rm ollama`  | ⚠️ **Deletes all models and config** |
| **4. Remove Image**     | `docker rmi ollama/ollama` | Remove the image                     |

### Open WebUI Cleanup

| Step                    | Command                                    | Description                            |
| ----------------------- | ------------------------------------------ | -------------------------------------- |
| **1. Stop Container**   | `docker stop open-webui`                   | Stop the running container             |
| **2. Remove Container** | `docker rm open-webui`                     | Delete the container                   |
| **3. Remove Volume**    | `docker volume rm open-webui`              | ⚠️ **Deletes all user data and chats** |
| **4. Remove Image**     | `docker rmi ghcr.io/open-webui/open-webui` | Remove the image                       |

### Complete System Cleanup

**⚠️ Extreme Caution:** This removes ALL Docker data

```powershell
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all volumes
docker volume prune --force

# Remove all images
docker image prune -a --force

# Complete system cleanup
docker system prune -a --volumes --force
```

---

## Best Practices & Resources

### Performance Optimization

| Service        | Optimization                | Benefit                          |
| -------------- | --------------------------- | -------------------------------- |
| **PostgreSQL** | Use named volumes for data  | Faster I/O and data persistence  |
| **PostgreSQL** | Configure shared_buffers    | Better memory utilization        |
| **Ollama**     | Enable GPU acceleration     | 10-100x faster inference         |
| **Ollama**     | Use appropriate model sizes | Balance performance vs. accuracy |
| **Open WebUI** | Enable GPU acceleration     | Smoother UI and faster responses |
| **All**        | Regular container restarts  | Prevent memory leaks             |

### Security Best Practices

1. **Strong Passwords**: Use complex passwords for PostgreSQL and Open WebUI admin accounts
2. **Network Security**: Limit port access with firewalls and consider reverse proxy setup
3. **Regular Updates**: Keep Docker images updated for security patches
4. **Access Control**: Restrict database and API access, use Open WebUI user management
5. **Monitoring**: Regular log review for security events across all services
6. **SSL/TLS**: Consider implementing HTTPS for Open WebUI in production environments

### Resource Management

| Resource     | PostgreSQL | Ollama    | Open WebUI | Combined   |
| ------------ | ---------- | --------- | ---------- | ---------- |
| **RAM**      | 2-4GB      | 4-16GB    | 1-2GB      | 8-22GB     |
| **Disk**     | 10-50GB    | 20-200GB  | 5-20GB     | 50-270GB   |
| **CPU**      | 2-4 cores  | 4-8 cores | 1-2 cores  | 6-14 cores |
| **GPU VRAM** | N/A        | 4-24GB    | 1-4GB      | 4-24GB     |

### Backup Strategies

**PostgreSQL Backups:**

```powershell
# Create backup
docker exec postgres pg_dump -U postgres -d mydb > backup_$(Get-Date -Format "yyyyMMdd").sql

# Automated backup script
docker exec postgres pg_dumpall -U postgres > full_backup_$(Get-Date -Format "yyyyMMdd").sql
```

**Volume Backups:**

```powershell
# Backup PostgreSQL volume
docker run --rm -v postgres_pgvector_data:/data -v ${PWD}:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .

# Backup Ollama volume
docker run --rm -v ollama:/data -v ${PWD}:/backup alpine tar czf /backup/ollama_backup.tar.gz -C /data .

# Backup Open WebUI volume
docker run --rm -v open-webui:/data -v ${PWD}:/backup alpine tar czf /backup/openwebui_backup.tar.gz -C /data .
```

**Complete Backup Script:**

```powershell
# Create backup directory
$backupDir = "backups\$(Get-Date -Format 'yyyyMMdd')"
New-Item -ItemType Directory -Path $backupDir -Force

# Backup all volumes
docker run --rm -v postgres_pgvector_data:/data -v ${PWD}/${backupDir}:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
docker run --rm -v ollama:/data -v ${PWD}/${backupDir}:/backup alpine tar czf /backup/ollama_backup.tar.gz -C /data .
docker run --rm -v open-webui:/data -v ${PWD}/${backupDir}:/backup alpine tar czf /backup/openwebui_backup.tar.gz -C /data .

Write-Host "Backup completed in $backupDir"
```

### Useful Resources

#### Official Documentation

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgvector GitHub Repository](https://github.com/pgvector/pgvector)
- [Ollama Official Documentation](https://ollama.com/)
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Docker Documentation](https://docs.docker.com/)

#### APIs and Integration

- [PostgreSQL JDBC Drivers](https://jdbc.postgresql.org/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Open WebUI API Documentation](https://docs.openwebui.com/api/)
- [pgvector Python Client](https://github.com/pgvector/pgvector-python)

#### Community Resources

- [Ollama Model Library](https://ollama.com/library)
- [Open WebUI GitHub Repository](https://github.com/open-webui/open-webui)
- [PostgreSQL Community](https://www.postgresql.org/community/)
- [Docker Hub - pgvector](https://hub.docker.com/r/pgvector/pgvector)
- [Docker Hub - Ollama](https://hub.docker.com/r/ollama/ollama)
- [GitHub Container Registry - Open WebUI](https://github.com/open-webui/open-webui/pkgs/container/open-webui)

#### Development Integration Examples

**Python Integration:**

```python
# Example: Connecting to all services from Python
import psycopg2
import requests
import openai

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="yoursecurepassword"
)

# Ollama API connection
ollama_response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3:8b", "prompt": "Hello, world!", "stream": False}
)

# Open WebUI API connection (if API is enabled)
webui_headers = {"Authorization": "Bearer your_api_token"}
webui_response = requests.get(
    "http://localhost:3001/api/v1/models",
    headers=webui_headers
)
```

**JavaScript/Node.js Integration:**

```javascript
const { Client } = require("pg");
const axios = require("axios");

// PostgreSQL connection
const pgClient = new Client({
  host: "localhost",
  port: 5432,
  database: "postgres",
  user: "postgres",
  password: "yoursecurepassword",
});

// Ollama API call
async function callOllama(prompt) {
  const response = await axios.post("http://localhost:11434/api/generate", {
    model: "llama3:8b",
    prompt: prompt,
    stream: false,
  });
  return response.data.response;
}

// Vector similarity search with pgvector
async function vectorSearch(embedding) {
  const query = `
    SELECT content, embedding <-> $1 as distance 
    FROM documents 
    ORDER BY embedding <-> $1 
    LIMIT 5;
  `;
  const result = await pgClient.query(query, [embedding]);
  return result.rows;
}
```

#### Model Recommendations by Use Case

| Use Case               | Recommended Ollama Model | RAM Required | GPU VRAM | Notes                            |
| ---------------------- | ------------------------ | ------------ | -------- | -------------------------------- |
| **Code Generation**    | `codellama:13b`          | 16GB         | 8GB      | Specialized for programming      |
| **General Chat**       | `llama3.2:3b`            | 8GB          | 4GB      | Fast responses, good quality     |
| **Complex Reasoning**  | `llama3:70b`             | 64GB         | 40GB     | Best quality, resource intensive |
| **Document Analysis**  | `llama3:8b`              | 16GB         | 8GB      | Good balance of speed/quality    |
| **Creative Writing**   | `llama3.1:8b`            | 16GB         | 8GB      | Enhanced creative capabilities   |
| **Multilingual Tasks** | `aya:8b`                 | 16GB         | 8GB      | Supports 100+ languages          |

#### Monitoring and Maintenance

**System Monitoring Script:**

```powershell
# System health check script
function Check-DockerServices {
    Write-Host "=== Docker Services Health Check ===" -ForegroundColor Green

    # Check if Docker is running
    $dockerRunning = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
    if ($dockerRunning) {
        Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
    } else {
        Write-Host "✗ Docker Desktop is not running" -ForegroundColor Red
        return
    }

    # Check each service
    $services = @("postgres", "ollama", "open-webui")

    foreach ($service in $services) {
        $container = docker ps --filter "name=$service" --format "table {{.Names}}\t{{.Status}}" | Select-Object -Skip 1
        if ($container) {
            Write-Host "✓ $service is running: $container" -ForegroundColor Green
        } else {
            Write-Host "✗ $service is not running" -ForegroundColor Red
        }
    }

    # Check disk usage
    Write-Host "`n=== Disk Usage ===" -ForegroundColor Yellow
    docker system df

    # Check resource usage
    Write-Host "`n=== Resource Usage ===" -ForegroundColor Yellow
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
}

# Run the health check
Check-DockerServices
```

**Automated Maintenance Script:**

```powershell
# Maintenance script for Docker AI stack
function Invoke-DockerMaintenance {
    param(
        [switch]$CleanLogs,
        [switch]$UpdateImages,
        [switch]$BackupData,
        [string]$BackupPath = ".\backups"
    )

    Write-Host "=== Docker AI Stack Maintenance ===" -ForegroundColor Cyan

    if ($CleanLogs) {
        Write-Host "Cleaning container logs..." -ForegroundColor Yellow
        docker system prune -f
        Write-Host "Logs cleaned." -ForegroundColor Green
    }

    if ($UpdateImages) {
        Write-Host "Updating Docker images..." -ForegroundColor Yellow
        docker pull pgvector/pgvector:0.8.0-pg17
        docker pull ollama/ollama
        docker pull ghcr.io/open-webui/open-webui:cuda
        Write-Host "Images updated." -ForegroundColor Green
    }

    if ($BackupData) {
        Write-Host "Creating backups..." -ForegroundColor Yellow
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupDir = Join-Path $BackupPath $timestamp
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

        # Backup volumes
        docker run --rm -v postgres_pgvector_data:/data -v "${backupDir}:/backup" alpine tar czf /backup/postgres_backup.tar.gz -C /data .
        docker run --rm -v ollama:/data -v "${backupDir}:/backup" alpine tar czf /backup/ollama_backup.tar.gz -C /data .
        docker run --rm -v open-webui:/data -v "${backupDir}:/backup" alpine tar czf /backup/openwebui_backup.tar.gz -C /data .

        Write-Host "Backups created in: $backupDir" -ForegroundColor Green
    }

    Write-Host "Maintenance completed!" -ForegroundColor Cyan
}

# Example usage:
# Invoke-DockerMaintenance -CleanLogs -BackupData
```

#### Production Deployment Considerations

**Environment Variables for Production:**

```yaml
# Production docker-compose.yml additions
services:
  postgres:
    environment:
      - POSTGRES_DB=${DB_NAME:-ai_production}
      - POSTGRES_USER=${DB_USER:-aiuser}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-aiuser}"]
      interval: 30s
      timeout: 10s
      retries: 3

  ollama:
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_ORIGINS=https://yourdomain.com
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

  open-webui:
    environment:
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
      - WEBUI_JWT_SECRET_KEY=${WEBUI_JWT_SECRET_KEY}
      - OLLAMA_BASE_URL=http://ollama:11434
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Reverse Proxy Configuration (Nginx):**

```nginx
# nginx.conf for production deployment
upstream open-webui {
    server localhost:3001;
}

upstream ollama-api {
    server localhost:11434;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    # Open WebUI
    location / {
        proxy_pass http://open-webui;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Ollama API (if needed)
    location /ollama/ {
        proxy_pass http://ollama-api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

**Note:** This comprehensive guide assumes basic familiarity with Docker, PostgreSQL, and command-line operations. For beginners, consider reviewing the official tutorials for each technology before proceeding with advanced configurations. The addition of Open WebUI creates a complete AI development and deployment stack suitable for both development and production environments.
