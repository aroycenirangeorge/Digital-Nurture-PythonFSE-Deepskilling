# Course Management System — Microservice Decomposition Analysis

## Bounded Context Decomposition Mappings

| Service Name | Primary Core Responsibility | Endpoints Owned | Data Infrastructure Domain |
| :--- | :--- | :--- | :--- |
| **Course Service** | Handles course catalogs and departmental groupings. | `POST /api/v1/courses/`<br>`GET /api/v1/courses/`<br>`GET /api/v1/courses/{id}` | `courses.db` (SQLite) |
| **Student Service** | Handles student profiling data and course registrations. | `POST /api/v1/students/`<br>`GET /api/v1/students/{id}`<br>`POST /api/v1/enrollments/` | `students.db` (SQLite) |
| **Auth Service** | Manages credentials, tokens, and identity validations. | `POST /api/v1/auth/register`<br>`POST /api/v1/auth/login` | `auth.db` (SQLite) |
| **Notification Service**| Manages transactional emails and outbound background task operations. | Internal Message Queue Consumers / Event Hooks | Stateless / Event Log Data Store |

### The Core Microservice Constraint Rule
Each microservice completely owns its database ecosystem. No service is permitted to perform cross-database queries or directly connect to another service's data store. Inter-service communications must pass through network APIs or message brokers.


