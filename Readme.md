# Easy Share

A complete advanced FTP server for file sharing and downloading, built with modern web technologies.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

- [Git Commands](#git-commands)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🌟 Overview

Easy Share is a comprehensive file sharing solution that provides secure, fast, and reliable file transfer capabilities. Built with Django and Django REST Framework, it offers both web interface and API endpoints for seamless integration.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Secure File Upload/Download** | Advanced security measures for safe file transfers |
| **User Authentication** | Role-based access control system |
| **File Management** | Organize, rename, and delete files with ease |
| **API Integration** | RESTful APIs for third-party integrations |
| **Responsive Design** | Works seamlessly across all devices |
| **Progress Tracking** | Real-time upload/download progress indicators |
| **File Versioning** | Keep track of file versions and changes |
| **Bulk Operations** | Upload and download multiple files simultaneously |

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Frontend** | HTML5, CSS3, JavaScript, Tailwind CSS |
| **Backend** | Django, Django REST Framework (DRF) |
| **Database** | PostgreSQL |
| **File Storage** | Local/Cloud storage support |
| **Authentication** | Django's built-in authentication system |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL 12 or higher
- Git
- Node.js and npm (for Tailwind CSS compilation)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ompandey07/pioneer_cloud_share.git
cd pioneer_cloud_share
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE easy_share_db;
CREATE USER easy_share_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE easy_share_db TO easy_share_user;
```

### 5. Environment Configuration

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://easy_share_user:your_password@localhost:5432/easy_share_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## ⚙️ Configuration

### Database Configuration

Update your `settings.py` with proper database configurations:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easy_share_db',
        'USER': 'easy_share_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### File Upload Settings

Configure file upload settings in `settings.py`:

```python
# File upload settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024   # 100MB
```

## 📖 Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Login with the provided credentials:
   - **Email**: `admin@pioneersoftware.com`
   - **Password**: `Pioneer@Nepal`
3. Upload files using the drag-and-drop interface
4. Manage files through the dashboard
5. Share files with generated links

### Admin Panel

Access the admin panel at `http://localhost:8000/admin/` with superuser credentials to:
- Manage users and permissions
- Monitor file uploads
- Configure system settings

## 📝 Git Commands

### Basic Workflow

```bash
# Clone the repository
git clone https://github.com/ompandey07/pioneer_cloud_share.git

# Navigate to project directory
cd pioneer_cloud_share

# Check current status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your descriptive commit message"

# Push to remote repository
git push origin main

# Pull latest changes
git pull origin main
```

### Branch Management

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# List all branches
git branch -a

# Switch between branches
git checkout main
git checkout feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

### Useful Git Commands

```bash
# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash changes
git stash
git stash pop

# View differences
git diff
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🧪 Testing

Run tests with:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test app_name

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report
```

## 🚀 Deployment

### Production Setup

1. Set `DEBUG=False` in production
2. Configure proper database settings
3. Set up static file serving
4. Configure HTTPS
5. Set up proper logging

### Docker Deployment

```bash
# Build Docker image
docker build -t easy-share .

# Run container
docker run -p 8000:8000 easy-share
```

## 🔧 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check PostgreSQL service
sudo service postgresql status

# Restart PostgreSQL
sudo service postgresql restart
```

**Migration Issues**
```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial
```

**Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --clear
```

## 📄 License

This project is proprietary software developed by Pioneer Software Solutions Pvt Ltd. All rights reserved.

## 👤 Contact

**Developer**: Om Pandey  
**Company**: Pioneer Software Solutions Pvt Ltd  
**Founder**: Finix Dev  
**GitHub**: [@ompandey07](https://github.com/ompandey07)  
**Repository**: [pioneer_cloud_share](https://github.com/ompandey07/pioneer_cloud_share)

---

**Copyright © 2024 Pioneer Software Solutions Pvt Ltd. All rights reserved.**

For support and inquiries, please contact our development team or create an issue in the GitHub repository.