import nox


locations = "src", "tests", "noxfile.py"


@nox.session(python="3.8.13")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
    session.run("isort", "--profile", "black", "src")


@nox.session(python=["3.8.13"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-bugbear", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python=["3.8.13"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "-cov")
