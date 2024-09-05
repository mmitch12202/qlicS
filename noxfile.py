"""Nox sessions."""
import nox
from nox.sessions import Session

locations = "src", "tests", "noxfile.py", "docs/conf.py"

@nox.session(python="3.9.13")
def black(session):
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
    session.run("isort", "--profile", "black", "src")


@nox.session(python=["3.9.13"])
def lint(session):
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=["3.9.13"])
def tests(session):
    """Run the test suite."""
    session.run("poetry", "install", external=True)
    session.run("pytest", "-cov")

@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
