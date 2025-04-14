# Architecture

## Package diagram

![Package diagram](./images/achitecture_package_diagram.png)

## Sequence diagram: creating a new user

When user inputs unused username and password and clicks "Create", the control of the application proceeds as follows:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant UserService
  participant UserRepository
  participant paavo
  User->>UI: click "Create user" button
  UI->>UserService: create_user("paavo", "kissa123")
  UserService->>UserRepository: find_by_username("paavo")
  UserRepository-->>UserService: None
  UserService->>paavo: User("paavo", "kissa123")
  UserService->>UserRepository: create(paavo)
  UserRepository-->>UserService: user
  UserService-->>UI: user
  UI->>UI: show_login_view()
```
