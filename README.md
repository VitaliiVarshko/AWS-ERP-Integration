# AWS ERP Integration Demo

A practical ERP integration project demonstrating how a backend application can be deployed on AWS and integrated with a relational database, object storage, IAM and monitoring services.

The project was created as a hands-on portfolio project with a focus on **ERP integration, system administration, cloud infrastructure and operational troubleshooting**.

## Architecture

```text
      Web Browser
          |
          | HTTP
          v
+-----------------------+
|       AWS EC2         |
|                       |
|  FastAPI REST API     |
|  Python               |
|  systemd              |
+----------+------------+
           |
       +---+---+
       |       |
       v       v
+----------+  +----------+
|   RDS    |  |    S3    |
|PostgreSQL|  |Documents |
+----------+  +----------+
       \       /
        \     /
         v   v
    +-------------+
    | CloudWatch  |
    | Logs +      |
    | Metrics     |
    +-------------+
```

## Business Scenario

The application represents a simplified ERP order-processing system.

An employee can create an order containing:

- order number
- customer
- product
- quantity

The order is stored in **PostgreSQL on Amazon RDS**.

The application can then generate a JSON document from the order and store it in **Amazon S3**.

This demonstrates a typical integration pattern where:

- transactional business data is stored in a relational database;
- documents and files are stored separately in object storage;
- an application layer connects the different systems;
- operational information is collected centrally for monitoring.

## AWS Components

| Component | Purpose |
|---|---|
| Amazon EC2 | Hosts the FastAPI application |
| Amazon RDS PostgreSQL | Stores ERP business data |
| Amazon S3 | Stores generated order documents |
| AWS IAM | Controls application access to AWS resources |
| Amazon CloudWatch | Application logs and system metrics |
| Security Groups | Controls network access |
| systemd | Runs and restarts the application as a Linux service |

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- boto3

### Infrastructure

- Amazon EC2
- Amazon RDS
- Amazon S3
- AWS IAM
- Amazon CloudWatch
- Linux systemd

### Development

- Git
- GitHub
- VS Code
- REST API
- HTML / JavaScript

## Application Flow

### 1. Create an ERP order

The user enters an order in the web interface.

The browser sends:

```http
POST /orders
```

Example payload:

```json
{
  "order_number": "ORD-AWS-001",
  "customer": "AWS Test GmbH",
  "items": [
    {
      "product": "Laptop Dell",
      "quantity": 3
    },
    {
      "product": "Monitor Dell",
      "quantity": 2
    }
  ]
}
```

### 2. Store the order in PostgreSQL

FastAPI receives the request and creates:

- one record in `orders`;
- one or more records in `order_items`.

The relationship between an order and its items is handled by SQLAlchemy.

### 3. Export the order to S3

The application can create a JSON document for an order.

The endpoint is:

```http
POST /orders/{order_id}/document
```

The resulting object is stored in S3, for example:

```text
orders/ORD-AWS-001.json
```

### 4. Monitor the application

The application writes operational and business events to logs.

Examples:

```text
Order created: ORD-AWS-005, customer: Interview Demo GmbH
```

```text
Document uploaded to S3: orders/ORD-AWS-005.json
```

The logs are collected by the CloudWatch Agent.

CloudWatch also collects system metrics such as:

- memory utilization;
- disk utilization.

## Security

The application does **not** contain AWS access keys.

The EC2 instance uses an **IAM Role**:

```text
ERP-Integration-EC2-S3-Role
```

The role grants the application the permissions required to work with the S3 bucket.

This demonstrates the principle of using temporary AWS credentials provided through IAM instead of storing long-lived access keys in application configuration.

The RDS database is not publicly accessible.

Network access is controlled through AWS Security Groups.

Sensitive configuration such as the database connection string is stored in a local `.env` file and is excluded from Git.

Example:

```text
.env
```

is ignored by Git.

A template can be provided through:

```text
.env.example
```

without containing real credentials.

## REST API

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Create Order

```http
POST /orders
```

### Get Orders

```http
GET /orders
```

### Get One Order

```http
GET /orders/{order_id}
```

### Export Order to S3

```http
POST /orders/{order_id}/document
```

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the database connection using an environment variable:

```text
DATABASE_URL=...
```

Start the application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The FastAPI documentation is then available at:

```text
/docs
```

## Linux Service

On the AWS EC2 server the application is managed by systemd.

Service:

```text
erp-integration.service
```

Useful commands:

```bash
sudo systemctl status erp-integration
```

```bash
sudo systemctl restart erp-integration
```

```bash
sudo systemctl is-active erp-integration
```

This allows the application to:

- start automatically;
- restart after failure;
- run independently of an SSH session.

## Monitoring and Logging

Application logs are written to:

```text
/var/log/erp-integration/application.log
```

The CloudWatch Agent forwards the logs to:

```text
/aws/ec2/erp-integration/system
```

The project therefore provides both:

- technical HTTP logs;
- business-level application logs.

This makes it possible to distinguish between:

```text
HTTP request failed
```

and:

```text
Order creation failed
```

or:

```text
Document upload failed
```

## Troubleshooting Example

A controlled failure scenario was used to test operational troubleshooting.

The database configuration was temporarily changed to an invalid database host.

The application then failed during startup because SQLAlchemy could not establish the database connection.

The problem could be diagnosed using:

```bash
sudo systemctl status erp-integration
```

and application logs:

```text
/var/log/erp-integration/application.log
```

The same application error was also visible in CloudWatch Logs.

After restoring the correct configuration and restarting the service, the application returned to a healthy state.

This demonstrates a typical troubleshooting workflow:

```text
Symptom
   |
Check systemd
   |
Check application logs
   |
Identify database connection failure
   |
Correct configuration
   |
Restart service
   |
Verify /health
```

## Project Goals

The project demonstrates practical experience with:

- deploying a backend application to AWS;
- Linux server administration;
- systemd service management;
- PostgreSQL on Amazon RDS;
- object storage with Amazon S3;
- IAM roles and permissions;
- AWS Security Groups;
- CloudWatch monitoring;
- application logging;
- REST API design;
- ERP-style data modelling;
- troubleshooting infrastructure and application failures.

## Why This Project

The project is intentionally small.

The goal is not to build a complete ERP system, but to demonstrate how an existing ERP-related application can be integrated with cloud infrastructure and operated in a controlled environment.

The focus is on the combination of:

**Business Process + Backend + Database + Cloud Infrastructure + Operations**

which is particularly relevant for ERP Application Engineering and IT System Administration.

## Future Improvements

Possible extensions include:

- HTTPS with Nginx;
- automated deployment;
- CI/CD with GitHub Actions;
- asynchronous processing;
- S3 event-driven integration;
- CloudWatch alarms;
- infrastructure as code;
- additional ERP integration endpoints;
- authentication and authorization;
- automated tests.

## Author

**Vitalii Varshko**

Software Developer / ERP Integration / AI & Automation

20+ years of experience in software development, ERP integration, backend development and business process automation.
