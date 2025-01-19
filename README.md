# Planner-Backend

**Planner-Backend** is a robust backend application designed to manage and streamline planning and scheduling operations. Built with a focus on scalability and efficiency, it serves as the core engine for the Planner application suite.

## Project Overview

Planner-Backend is developed to handle complex scheduling tasks, providing a reliable and efficient backend service. The application is structured to support various planning functionalities, ensuring seamless integration with frontend interfaces.

## Key Features

- **Custom Authentication**: Implements a secure and customizable authentication system to manage user access and permissions.
- **User Management**: Provides comprehensive user management capabilities, including role-based access control.
- **Machine Scheduling**: Manages machine-related scheduling, ensuring optimal utilization and conflict-free operation.
- **Planning Module**: Facilitates detailed planning functionalities, allowing users to create, modify, and track plans effectively.
- **Reporting**: Generates insightful reports to assist in decision-making and operational assessments.

## Project Structure

The project is organized into the following modules:

- `custom_auth`: Handles authentication mechanisms and user verification processes.
- `custom_user`: Manages user profiles, roles, and permissions.
- `machine`: Oversees machine-related data and scheduling.
- `plan`: Contains the core planning logic and operations.
- `raport`: Responsible for generating and managing reports.

## Setup and Installation

To set up the project locally, follow these steps:

### Prerequisites

- Python 3.9+
- SQLite (or another preferred database)
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Szabson123/Planner-Backend.git
   cd Planner-Backend
