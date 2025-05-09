# Architecture

## Package diagram

The application's layered architecture has three main layers that are the UI layer, the Services layer and the Repositories layer. The relations between the layers are shown in the pacakge diagram. The UI components use the Services and the Services use Repositories. Each layer depends only on the layer below it.

<img src="./images/achitecture_package_diagram.png" width="400" alt="Package diagram">

The UI layer contains all of the user interface components. The Services layer contains the business logic and acts as a middleware between UI and data storage. The Repositories layer handles the data storage and retrieval and communicates with the database.

## User Interface

The user interface has four different views. The views are handled by separate classes in the UI layer:

- Login view (LoginView)
- Registration view (RegistrationView)
- Logged in view (LoggedInView)
- Team view (TeamView)
- Game view (GameView)

The UI follows a single-view-at-a-time principle so only one view is visible at once. When the application is started, the Login view appears. From there the user has to first go to the Registration view from where they can create a new user and the log in. The logged in view appears after a successful login. The logged in view includes features: creating new teams, displaying user's teams as clickable buttons and logging out. When a team is clicked, the Team view opens. The Team view includes features: adding players to teams, displaying team roster, starting new games, showing game history and returning to the logged in page. The Game view shows the players that are included in the team.

## Main Functionalities

### Sequence diagram: creating a new user

When user inputs unused username and password and clicks "Register", the control of the application proceeds as follows:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant UserService
  participant UserRepository
  participant paavo
  User->>UI: click "Create new user" button
  UI->>UserService: create_user("paavo", "kissa123")
  UserService->>UserRepository: find_by_username("paavo")
  UserRepository-->>UserService: None
  UserService->>paavo: User("paavo", "kissa123")
  UserService->>UserRepository: create(paavo)
  UserRepository-->>UserService: user
  UserService-->>UI: user
  UI->>UI: show_login_view()
```

### Sequence diagram: logging in

When user inputs their username and password and clicks "Login", the control of the application proceeds as follows:

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant UserService
    participant UserRepository
    User->>UI: click "Login" button
    UI->>UserService: login("paavo", "kissa123")
    UserService->>UserRepository: find_by_username("paavo")
    UserRepository-->>UserService: user
    UserService-->>UI: True
    UI->>UI: show_logged_in_view()
```

The sequence starts when user clicks the login button. The UI calls UserService's login method with the given credentials. UserService asks UserRepository to find the user by username. If user exists and password matches, UserService returns True to UI, which then switches to the logged in view.

### Sequence diagram: adding pass statistics

When a user adds a pass statistic during a game, the control of the application proceeds as follows:

```mermaid
sequenceDiagram
    actor User
    participant GameView
    participant TeamService
    participant StatisticsRepository
    User->>GameView: click pass score button
    GameView->>TeamService: add_pass_stat(game_id, player_id, score)
    TeamService->>StatisticsRepository: add_pass_stat(game_id, player_id, score)
    StatisticsRepository-->>TeamService: None
    TeamService->>StatisticsRepository: get_pass_stats_for_game(game_id)
    StatisticsRepository-->>TeamService: stats
    TeamService-->>GameView: True
    GameView->>GameView: update_statistics_display()
```

### Sequence diagram: ending a game

When user ends a game, the control of the application proceeds as follows:

```mermaid
sequenceDiagram
    actor User
    participant GameView
    participant TeamService
    participant GameRepository
    User->>GameView: click "End Game" button
    GameView->>TeamService: end_game(game_id)
    TeamService->>GameRepository: update_game_status(game_id, "ended")
    GameRepository-->>TeamService: None
    TeamService-->>GameView: True
    GameView->>GameView: hide_scoring_buttons()
```

### Sequence diagram: viewing game statistics

When user opens a game view, the control of the application proceeds as follows:

```mermaid
sequenceDiagram
    actor User
    participant TeamView
    participant GameView
    participant TeamService
    participant StatisticsRepository
    User->>TeamView: click game
    TeamView->>GameView: show_game_view(game, team)
    GameView->>TeamService: get_pass_average(game_id)
    TeamService->>StatisticsRepository: get_pass_stats_for_game(game_id)
    StatisticsRepository-->>TeamService: stats
    TeamService-->>GameView: average
    GameView->>TeamService: get_team_serve_average(game_id)
    TeamService->>StatisticsRepository: get_game_serve_statistics(game_id)
    StatisticsRepository-->>TeamService: stats
    TeamService-->>GameView: average
    GameView->>GameView: display_statistics()
```
