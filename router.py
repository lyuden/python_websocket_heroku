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
    games = []

    def on_open(self):
        print "Some client connected!"

    def send_group_update(self):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps({'type': 'group_info',

                                       'free':[group for group in self.groups if not group in self.games ],
                                       'user_groups':  [group for group in self.groups if client in self.groups[group]]

                                                       }))

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)

        if message['type'] == 'auth':
            self.authorized_users[self.ws.handler.active_client] = message['login']


            self.groups[message['login']].append(self.ws.handler.active_client)
            self.send_group_update()
        elif not self.ws.handler.active_client in self.authorized_users:
            return
        elif message['type'] == 'message':
            self.broadcast(message)
        elif message['type'] == 'game_start':
            self.games.append(message['group'])
            self.send_group_update()
        elif message['type'] == 'game_stop':
           self.games.remove(message['group'])
           self.send_group_update()
        elif message['type'] == 'add_group':
            if len(self.groups[message['group']])< 4 and  not (message['group'] in self.games):
                self.groups[message['group']].append(self.ws.handler.active_client)
                self.send_group_update()
                print "Added user to group {}".format(message['group'])
            else:
                print "Failed to add user to group"


        elif message['type'] =='rm_group':
            self.groups[message['group']].remove(self.ws.handler.active_client)
            self.send_group_update()
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
