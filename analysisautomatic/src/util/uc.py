from dataclasses import dataclass, field

@dataclass
class UseCase:
    id: int
    name: str = ""
    description: str = ""
    actors: list = field(default_factory=list)
    preconditions: str = ""
    postconditions: list = field(default_factory=list)
    steps: list = field(default_factory=list)
    alternative: list = field(default_factory=list)
    quality_requirements: list = field(default_factory=list)

# Example usage
use_case_example = UseCase(
    id=1,
    name="User Login",
    description="Allows a user to log into the system",
    actors=["User"],
    preconditions="User must have a valid account",
    postconditions="User is logged into the system",
    steps=[
        "User navigates to the login page",
        "User enters username and password",
        "System validates credentials",
        "User is redirected to the dashboard"
    ]
)