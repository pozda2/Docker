from flask.cli import FlaskGroup

from app import app, db, Image

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Image(
        url_image="https://images.unsplash.com/photo-1533450718592-29d45635f0a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8anBnfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60"))
    db.session.add(Image(
        url_image="https://images.unsplash.com/photo-1646418579944-397ac052b78a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTl8fGpwZ3xlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60"))
    db.session.add(Image(
        url_image="https://images.unsplash.com/photo-1485529910432-783b455774fa?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fGpwZ3xlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60"))
    db.session.add(Image(
        url_image="https://images.unsplash.com/photo-1616951116286-109a1039275d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8anBnfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60"))
    db.session.commit()


if __name__ == "__main__":
    cli()
