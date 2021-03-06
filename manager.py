  
from CarRentBlockChain import create_app
from CarRentBlockChain.extensions import db
from CarRentBlockChain.blueprints.public.models import User
from CarRentBlockChain.privkeyutils.privkeyutils import create_address_by_privkey, create_random_address

from flask_script import Manager, Server, Shell
import click
app = create_app()

banner = r"""
 __ __ __       ______       ________      ______       ______       ___   __       _________   ________      _________   __  __
/_//_//_/\     /_____/\     /_______/\    /_____/\     /_____/\     /__/\ /__/\    /________/\ /_______/\    /________/\ /_/\/_/\
\:\\:\\:\ \    \::::_\/_    \__.::._\/    \:::_ \ \    \::::_\/_    \::\_\\  \ \   \__.::.__\/ \__.::._\/    \__.::.__\/ \ \ \ \ \
 \:\\:\\:\ \    \:\/___/\      \::\ \      \:\ \ \ \    \:\/___/\    \:. `-\  \ \     \::\ \      \::\ \        \::\ \    \:\_\ \ \
  \:\\:\\:\ \    \::___\/_     _\::\ \__    \:\ \ \ \    \::___\/_    \:. _    \ \     \::\ \     _\::\ \__      \::\ \    \::::_\/
   \:\\:\\:\ \    \:\____/\   /__\::\__/\    \:\/.:| |    \:\____/\    \. \`-\  \ \     \::\ \   /__\::\__/\      \::\ \     \::\ \
    \_______\/     \_____\/   \________\/     \____/_/     \_____\/     \__\/ \__\/      \__\/   \________\/       \__\/      \__\/

"""

manager = Manager(app)


def make_shell_context():
    return {
        "app": app,
    }

manager.add_command("runserver", Server(host="0.0.0.0", port=5000, use_debugger=False))
manager.add_command("shell", Shell(banner=banner, make_context=make_shell_context))

@manager.command
def reset_local_db():
    """Reset local databases."""
    click.confirm('This operation will delete the local database, do you want to continue?', abort=True)
    db.drop_all(bind=None)
    click.echo('Drop local tables.')
    db.create_all(bind=None)
    click.echo('Reset local database.')

@manager.command
def reset_server_db():
    """Reset server databases."""
    click.confirm('This operation will delete the server database, do you want to continue?', abort=True)
    db.drop_all(bind="userserver")
    click.echo('Drop local tables.')
    db.create_all(bind="userserver")
    click.echo('Success create server databases.')
    click.echo('Reset server database.')

    admin_privkey = "0x8ef2fa4907d75fa653cede21fa0a75d62add49e4db46044dd3954dda14fcdfa6"
    addr_msg = create_address_by_privkey(admin_privkey)
    admin = User(username="admin", email="admin@admin.com", is_admin=True, active=True, privkey=addr_msg["privateKeyHex"][2:], privatekey_hex=addr_msg["privateKeyHex"],
                    privatekey_int=addr_msg["privateKeyInt"], publickey_hex=addr_msg["publicKeyHex"],
                    publickey_int=addr_msg["publicKeyInt"], address=addr_msg["address"])
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')


@manager.command
def reset_db():
    """Reset all databases."""
    click.confirm('This operation will delete all database, do you want to continue?', abort=True)
    db.drop_all()
    click.echo('Drop all tables.')
    db.create_all()
    click.echo('Reset all database.')
    admin_privkey = "0x8ef2fa4907d75fa653cede21fa0a75d62add49e4db46044dd3954dda14fcdfa6"


    addr_msg = create_address_by_privkey(admin_privkey)
    admin = User(username="admin", email="admin@admin.com", is_admin=True, active=True, privkey=addr_msg["privateKeyHex"][2:], privatekey_hex=addr_msg["privateKeyHex"],
                    privatekey_int=addr_msg["privateKeyInt"], publickey_hex=addr_msg["publicKeyHex"],
                    publickey_int=addr_msg["publicKeyInt"], address=addr_msg["address"])

    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')



@manager.command
def init_local_db():
    """Initialized local databases."""
    db.create_all(bind=None)
    click.echo('Initialized local database.')


@manager.command
def init_server_db():
    """Initialized server databases."""
    db.create_all(bind="userserver")
    click.echo('Initialized server database.')

    admin_privkey = "0x8ef2fa4907d75fa653cede21fa0a75d62add49e4db46044dd3954dda14fcdfa6"

    addr_msg = create_address_by_privkey(admin_privkey)
    admin = User(username="admin", email="admin@admin.com", is_admin=True, active=True, privkey=addr_msg["privateKeyHex"][2:], privatekey_hex=addr_msg["privateKeyHex"],
                    privatekey_int=addr_msg["privateKeyInt"], publickey_hex=addr_msg["publicKeyHex"],
                    publickey_int=addr_msg["publicKeyInt"], address=addr_msg["address"])
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')

@manager.command
def init_db():
    """Initialized all databases."""
    db.create_all()
    click.echo('Initialized all database.')

    admin_privkey = "0x8ef2fa4907d75fa653cede21fa0a75d62add49e4db46044dd3954dda14fcdfa6"

    addr_msg = create_address_by_privkey(admin_privkey)
    admin = User(username="admin", email="admin@admin.com", is_admin=True, active=True, privkey=addr_msg["privateKeyHex"][2:], privatekey_hex=addr_msg["privateKeyHex"],
                    privatekey_int=addr_msg["privateKeyInt"], publickey_hex=addr_msg["publicKeyHex"],
                    publickey_int=addr_msg["publicKeyInt"], address=addr_msg["address"])
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')

@manager.command
def set_user(username, email, password, active=True):
    """Add A New User."""
    if User.query.filter(User.username==username).first() and User.query.filter(User.email==email).first() and active:
        user = User.query.filter(User.username==username).first()
        user.active = True
        click.echo('Success Update A New User to Active')
    else:

        addr_msg = create_random_address()
        admin = User(username=username, email=email, active=active, id=None, privkey=addr_msg["privateKeyHex"][2:],
                     privatekey_hex=addr_msg["privateKeyHex"],
                     privatekey_int=addr_msg["privateKeyInt"], publickey_hex=addr_msg["publicKeyHex"],
                     publickey_int=addr_msg["publicKeyInt"], address=addr_msg["address"])
        user = User(username=username, email=email, active=active, id=None)
        # add a User(active = False)
        user.set_password(password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit(user)
        click.echo("Success Add A New Active User.")

if __name__ == "__main__":
    manager.run()
