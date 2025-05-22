# Complete Docker Guide: PostgreSQL pgvector & Ollama Management

This comprehensive guide provides detailed instructions for managing PostgreSQL with pgvector and Ollama language models using Docker Desktop on Windows with PowerShell commands.

## Table of Contents

1. [Prerequisites & System Requirements](#prerequisites--system-requirements)
2. [PostgreSQL pgvector Setup](#postgresql-pgvector-setup)
3. [Ollama Docker Setup](#ollama-docker-setup)
4. [PostgreSQL Management Operations](#postgresql-management-operations)
5. [Ollama Management Operations](#ollama-management-operations)
6. [Advanced Configuration & Integration](#advanced-configuration--integration)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Complete Cleanup Procedures](#complete-cleanup-procedures)
9. [Best Practices & Resources](#best-practices--resources)

---

## Prerequisites & System Requirements

### Common Requirements

| Component                      | Description                     | Notes                                        |
| ------------------------------ | ------------------------------- | -------------------------------------------- |
| **Docker Desktop for Windows** | Installed and running           | Required for both PostgreSQL and Ollama      |
| **Windows PowerShell**         | Command execution environment   | All commands designed for PowerShell         |
| **Internet Connection**        | Active connection for downloads | Required for Docker images and models        |
| **Sufficient Disk Space**      | 50GB+ recommended               | PostgreSQL data + Ollama models can be large |

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

## Advanced Configuration & Integration

### Running Both Services Together

Both PostgreSQL and Ollama can run simultaneously:

```powershell
# Start PostgreSQL
docker start postgres

# Start Ollama
docker start ollama

# Verify both are running
docker ps
```

### Port Configuration

| Service        | Default Port | Alternative Port Command                   |
| -------------- | ------------ | ------------------------------------------ |
| **PostgreSQL** | 5432         | `-p 5433:5432` (maps to host port 5433)    |
| **Ollama**     | 11434        | `-p 11435:11434` (maps to host port 11435) |

### Docker Compose Configuration

Create `docker-compose.yml` for managing both services:

```yaml
version: "3.8"
services:
  postgres:
    image: pgvector/pgvector
    container_name: postgres
    environment:
      POSTGRES_PASSWORD: yoursecurepassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_pgvector_data:/var/lib/postgresql/data
    restart: unless-stopped

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

volumes:
  postgres_pgvector_data:
  ollama:
```

**Usage:**

```powershell
# Start both services
docker-compose up -d

# Stop both services
docker-compose down

# View logs
docker-compose logs
```

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

# Inspect specific container
docker inspect postgres
docker inspect ollama

# Check volume details
docker volume inspect postgres_pgvector_data
docker volume inspect ollama

# Monitor real-time logs
docker logs -f postgres
docker logs -f ollama
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
| **Both**       | Regular container restarts  | Prevent memory leaks             |

### Security Best Practices

1. **Strong Passwords**: Use complex passwords for PostgreSQL
2. **Network Security**: Limit port access with firewalls
3. **Regular Updates**: Keep Docker images updated
4. **Access Control**: Restrict database and API access
5. **Monitoring**: Regular log review for security events

### Resource Management

| Resource     | PostgreSQL | Ollama    | Combined   |
| ------------ | ---------- | --------- | ---------- |
| **RAM**      | 2-4GB      | 4-16GB    | 8-20GB     |
| **Disk**     | 10-50GB    | 20-200GB  | 50-250GB   |
| **CPU**      | 2-4 cores  | 4-8 cores | 6-12 cores |
| **GPU VRAM** | N/A        | 4-24GB    | 4-24GB     |

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
```

### Useful Resources

#### Official Documentation

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgvector GitHub Repository](https://github.com/pgvector/pgvector)
- [Ollama Official Documentation](https://ollama.com/)
- [Docker Documentation](https://docs.docker.com/)

#### APIs and Integration

- [PostgreSQL JDBC Drivers](https://jdbc.postgresql.org/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [pgvector Python Client](https://github.com/pgvector/pgvector-python)

#### Community Resources

- [Ollama Model Library](https://ollama.com/library)
- [PostgreSQL Community](https://www.postgresql.org/community/)
- [Docker Hub - pgvector](https://hub.docker.com/r/pgvector/pgvector)
- [Docker Hub - Ollama](https://hub.docker.com/r/ollama/ollama)

---

**Note:** This guide assumes basic familiarity with Docker, PostgreSQL, and command-line operations. For beginners, consider reviewing the official tutorials for each technology before proceeding with advanced configurations.
