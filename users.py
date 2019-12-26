from models import User, connect_to_db
import argparse

parser = argparse.ArgumentParser(description="Program used to add, edit, delete and list the users in the database")
parser.add_argument("-u", "--userlogin", required=True, help="the email address of the user as stored in the database. Used with -p.")
parser.add_argument("-p", "--password", required=True, help="the password of the user. Must be at least 8 characters long. Used with -u.")
parser.add_argument("-n", "--new-pass",
                    help="new password. Must be at least 8 characters long. Use with -e.")
parser.add_argument("-l", "--list", action="store_true", help="list of all users in the database")
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--delete", action="store_true", help="delete the user. -u and -p need to be provided also.")
group.add_argument("-e", "--edit", action="store_true", help="edit the user's password. Specifying new password "
                    "via the optional argument -n is required. -u and -p need to be provided also.")
args = parser.parse_args()
db_connection = connect_to_db()
if args.delete == False and args.edit == False and args.new_pass is None and args.list == False:
    all_emails = []
    all_users = User.get_all_users(db_connection)
    for user in all_users:
        all_emails.append(user.email)
    if args.userlogin in all_emails:
        print("User with this e-mail already exists. Use -e argument to edit, or -d to delete the user")
    elif len(args.password) < 8:
        print("Password must be at least 8 characters long. Try again")
    else:
        username = args.userlogin.split('@')[0]
        user = User(None, username, args.userlogin, args.password)
        user.save_to_db(db_connection)
        print("User added successfully")
elif args.delete == False and args.edit == True and args.new_pass is not None and args.list == False:
    if User.verify(args.userlogin, args.password, db_connection) == False:
        print("Invalid credentials. Try again.")
    elif len(args.new_pass) < 8:
        print("Password must be at least 8 characters long. Try again")
    else:
        user = User.get_user_by_email(args.userlogin, db_connection)
        user.change_password(args.new_pass, db_connection)
        print("Password changed successfully")
elif args.delete == True and args.edit == False and args.new_pass is None and args.list == False:
    if User.verify(args.userlogin, args.password, db_connection) == False:
        print("Invalid credentials. Try again.")
    else:
        User.delete(args.userlogin, db_connection)
        print("User deleted successfully")
elif args.delete == False and args.edit == False and args.new_pass is None and args.list == True:
    if User.verify(args.userlogin, args.password, db_connection) == False:
        print("Invalid credentials. Try again.")
    else:
        all_users = User.get_all_users(db_connection)
        for user in all_users:
            print(user.email)
else:
    parser.print_help()


