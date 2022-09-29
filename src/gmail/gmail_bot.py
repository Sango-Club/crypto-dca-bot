import yagmail

class GmailBot:
    def __init__(self, api_email, oauth_file):
        self.__yag = yagmail.SMTP(api_email, oauth2_file=oauth_file)
    
    def send_mail(self, to, subject, contents):
        if self.__yag.send(to=to, subject=subject, contents=contents):
            return True
        
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Emails people.')
    parser.add_argument('--receiver', metavar='t', type=str, help='receiver email')
    parser.add_argument('--sender', metavar='f', type=str, help='sender email')
    parser.add_argument('--oauthfile', metavar='of', type=str, help='gmail oauth file')

    args = parser.parse_args()

    bot = GmailBot(args.sender, args.oauthfile)
    bot.send_mail(args.receiver, subject="Foobar", contents="Hello world")