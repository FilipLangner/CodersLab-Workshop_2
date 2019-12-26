from models import Message, User, connect_to_db
import argparse

parser = argparse.ArgumentParser(description="Program used to send, save and list messages between users in the database")
parser.add_argument("-u", "--userlogin", required=True, help="the email address of the user as stored in the database. Used with -p.")
parser.add_argument("-p", "--password", required=True, help="the password of the user. Must be at least 8 characters long. Used with -u.")
parser.add_argument("-l", "--list", action="store_true", help="lists all the messages sent to the user")
parser.add_argument("-t", "--to", help="e-mail address of the user to whom the message is being sent. Use with -s")
parser.add_argument("-s", "--send", nargs='+', help="the message text that is to be sent. Use with -t")
args = parser.parse_args()
db_connection = connect_to_db()

if args.list == False and (args.to is None or args.send is None):
    print("You are missing the addressee or the message text. Try again.")
elif args.list == True and args.to is None and args.send is None:
    if User.verify(args.userlogin, args.password, db_connection) == False:
        print("Invalid credentials. Try again.")
    else:
        messages = Message.load_all_messages_for_user(args.userlogin, db_connection)
        for item in messages:
            sender = User.get_user(item.from_id, db_connection)
            print(f"{item.message_text}; from: {sender.email}; created on: {item.creation_date}")
elif args.list == False and args.to is not None and args.send is not None:
    all_emails = []
    all_users = User.get_all_users(db_connection)
    for user in all_users:
        all_emails.append(user.email)
    if User.verify(args.userlogin, args.password, db_connection) == False:
        print("Invalid credentials. Try again.")
    elif args.to not in all_emails:
        print("You are trying to send a message to a user that does not exist in the database. Check if the e-mail "
              "address is valid.")
    else:
        sender = User.get_user_by_email(args.userlogin, db_connection)
        receiver = User.get_user_by_email(args.to, db_connection)

        message = Message(None, sender.id, receiver.id, ' '.join(args.send), None)
        message.save_to_db(db_connection)
        print("Message sent.")
else:
    parser.print_help()