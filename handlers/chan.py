'''
Points users to important websites.
'''
class Handler:
    def __init__(self, brain):
        self.brain = brain; # Brain is not used in this example, but it is useful if you want i.e the name of the bot

    def canHandle(self, msg):
        if (msg.command == "PRIVMSG"):
            if(msg.msg == "#4chan"):
                msg.text = "Here you go, fam: https://www.4chan.org/int/balt";
                return True;
            if(msg.msg == "#8chan"):
                msg.text = "Here you go, fam: https://8ch.net/balt";
                return True;
            if(msg.msg == "#shitpost"):
                msg.text = "Here you go, fam: http://zmpng.duckdns.org/balt.html";
                return True;
        return False;

    def handle(self, msg, resp):
        resp.send(msg.text, msg.re());
