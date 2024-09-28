# SmartDNS Manager

SmartDNS Manager is a web-based interface to manage your Smart DNS service using Docker, Nginx, and Flask. It allows non-technical users to easily add or remove domains for DNS resolution, reload DNSMasq, and manage settings through a simple UI.

## Features

- Add and remove domains to DNSMasq dynamically.
- Reload DNSMasq through the web interface.
- SSL support using Nginx as a reverse proxy.
- Authentication for secure access.
- Easy to deploy using Docker and Docker Compose.

## Requirements

- A Linux VPS
- A domain name
- Docker and Docker Compose

## Installation Instructions

### 1. Get a Linux VPS

Provision a Linux-based VPS (Ubuntu, Debian, etc.) from any hosting provider.

### 2. Get a Domain

Purchase a domain name and configure its DNS settings to point to your VPS IP.

### 3. Install Docker and Docker Compose

On your VPS, install Docker and Docker Compose:

### 4. Clone the Repository

```bash
git clone https://github.com/a-farahani/Smart-DNS-Manager.git
```

### 5. Configure Environment Files

Complete the `.env` files in the project root:

1. **.env**: Set the timezone.

   ```env
   TimeZone='Your/TimeZone'
   ```

2. **.env.nginx**: Configure the domain and SSL certificate files.

   ```env
   DOMAIN='your-domain.com'
   CERTIFICATE_FILENAME='fullchain.pem'
   PRIVATEKEY_FILENAME='privkey.pem'
   ```

3. **.env.web**: Set the Flask secret key, admin username, password, and VPS IP.

   ```env
   FLASK_SECRET_KEY='your-secret-key'
   FLASK_USERNAME='admin'
   FLASK_PASSWORD='password'
   MY_VPS_IP='your-vps-ip'
   ```

### 6. Set Up SSL Certificates

Place your SSL certificates in the ssl directory, replacing fullchain.pem and privkey.pem with your own.

### 7. Start the Project

```bash
docker compose build
docker compose up -d
```

### 8. Start the Project

Once the services are up, the application should be accessible at https://your-domain.com. You can log in using the credentials set in the .env.web file.

### Managing Domains

Once the application is running, you can manage the DNS records through the web interface.

1. **Access the Web Interface**: Open your browser and navigate to `https://your-domain.com`.

2. **Login**: Use the credentials defined in the `.env.web` file:
   - Username: `admin`
   - Password: `password`

3. **Add a Domain**:
   - Enter the domain name in the input field.
   - Click on the "Add Domain" button. This will add the domain to the `proxy.conf` file.

4. **Delete a Domain**:
   - Click the "Delete" button next to the domain you want to remove.
   - The domain will be removed from the `proxy.conf` file.

5. **Reload DNSMasq**:
   - Click the "Reload DNSMasq" button to apply the changes. This will restart the DNSMasq container.

### License

This project is licensed under the terms of the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
