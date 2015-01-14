import json
import os

from gevent import monkey
monkey.patch_all()

from flask import Flask, app, render_template
from werkzeug.debug import DebuggedApplication

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from collections import defaultdict

flask_app = Flask(__name__)
flask_app.debug = True






class BackendApplication(WebSocketApplication):

    groups = defaultdict(list)
    authorized_users = {}

    def on_open(self):
        print "Some client connected!"

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)

        if message['type'] == 'auth':
            self.authorized_users[self.ws.handler.active_client] = message['login']

            self.ws.handler.active_client.ws.send(json.dumps({'free':
                                                           [group for group in self.groups if len(self.groups[group])==1 ], 'user_groups':
                                                           [group for group in self.groups if self.ws.handler.active_client in self.groups[group]]

                                                       }))
            self.groups[message['login']].append(self.ws.handler.active_client)
        elif not self.ws.handler.active_client in self.authorized_users:
            return
        elif message['type'] == 'message':
            self.broadcast(message)

        elif message['type'] == 'add_group':
            if len(self.groups[message['group']]) < 4:
                self.groups[message['group']].append(self.ws.handler.active_client)
                print "Added user to group {}".format(message['group'])
            else:
                print "Failed to add user to group"


        elif message['type'] =='rm_group':
            self.groups[message['group']].remove(self.ws.handler.active_client)
            print "Removed user from group {}".format(message['group'])
        else:
            raise "Unkown message type"


    def broadcast(self, message):
        if not self.ws.handler.active_client in self.groups[message['group']]:
            print "Sending messages to groups used doesn't belong not allowed"
            return

        for client in self.groups[message['group']]:
            if not client is self.ws.handler.active_client:
                        client.ws.send(json.dumps({
                            'type': 'message',
                            'data': message['data'],
                            'user': self.authorized_users[self.ws.handler.active_client]
                        }))

    def on_close(self, reason):
        print "Connection closed! "


@flask_app.route('/')
def index():
    return render_template('index.html')

WebSocketServer(
    ('0.0.0.0', int(os.environ.get('PORT', 8000))),

    Resource({
        '^/chat': BackendApplication,
        '^/.*': DebuggedApplication(flask_app)
    }),

    debug=False
).serve_forever()
